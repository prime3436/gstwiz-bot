"""
GSTWiz - Helper Module
Written for LangChain 1.x using LCEL (LangChain Expression Language)
No HuggingFace / torchvision dependencies needed.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Stable imports for LangChain 1.x ─────────────────────────────────────────
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
DATA_FILE   = "gst_data.txt"
FAISS_INDEX = "faiss_gst_index"

PROMPT_TEMPLATE = """You are GSTWiz, an expert AI assistant specializing in Indian GST
and tax compliance. Use ONLY the context below to answer.
If the answer is not in the context, say:
"I don't have specific info on this. Please visit www.gst.gov.in or consult a CA."

Context:
{context}

Question: {question}

Give a clear, structured answer with bullet points where helpful.
Cite GST sections/notifications where relevant.

Answer:"""


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _get_api_key() -> str:
    key = os.environ.get("GOOGLE_API_KEY", "")
    if not key:
        raise EnvironmentError("GOOGLE_API_KEY not set. Add it to your .env file.")
    return key

def _get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


# ─────────────────────────────────────────────
# Build Vector Database
# ─────────────────────────────────────────────
def create_vector_db() -> FAISS:
    """Load gst_data.txt → chunk → embed → save FAISS index."""
    print("Loading GST knowledge base...")
    docs = TextLoader(DATA_FILE, encoding="utf-8").load()

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    ).split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Embedding with Google AI (text-embedding-004)...")
    db = FAISS.from_documents(chunks, _get_embeddings())
    db.save_local(FAISS_INDEX)
    print(f"FAISS index saved to '{FAISS_INDEX}/'")
    return db


# ─────────────────────────────────────────────
# Load QA Chain (LCEL style)
# ─────────────────────────────────────────────
def get_qa_chain():
    """Returns a callable LCEL chain: invoke({"query": "..."}) -> {"result": ..., "source_documents": [...]}"""
    print("Loading FAISS index...")
    db = FAISS.load_local(
        FAISS_INDEX,
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )
    retriever = db.as_retriever(search_kwargs={"k": 4})

    print("Initialising Gemini 1.5 Flash...")
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=_get_api_key(),
        temperature=0.1,
        max_output_tokens=1024,
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    # LCEL chain
    chain = (
        {
            "context":  retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Wrap to return same dict format as RetrievalQA for compatibility with main.py
    class WrappedChain:
        def __init__(self, chain, retriever):
            self._chain = chain
            self._retriever = retriever

        def __call__(self, inputs: dict) -> dict:
            query = inputs.get("query", "")
            result = self._chain.invoke(query)
            source_docs = self._retriever.invoke(query)
            return {"result": result, "source_documents": source_docs}

    print("GSTWiz is ready!")
    return WrappedChain(chain, retriever)


# ─────────────────────────────────────────────
# Smoke test: python helper.py
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  GSTWiz - Knowledge Base Builder")
    print("=" * 50)
    create_vector_db()
    chain = get_qa_chain()
    result = chain({"query": "What is the GST registration threshold for services?"})
    print(f"\nAnswer:\n{result['result']}")
