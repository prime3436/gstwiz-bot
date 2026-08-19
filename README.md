# 💰 GSTWiz — AI-Powered GST Compliance Chatbot

> An intelligent RAG (Retrieval-Augmented Generation) chatbot for Indian GST queries, built with LangChain, FAISS, HuggingFace Embeddings, and Google Gemini 1.5 Flash.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.61-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-1.x-green)
![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-orange?logo=google)

---

## 🚀 Features

- 🧠 **RAG Pipeline** — FAISS vector store + HuggingFace `all-MiniLM-L6-v2` embeddings
- ⚡ **Gemini 1.5 Flash** — Google's fast LLM for accurate answers
- 📚 **Comprehensive Knowledge Base** — 20+ sections covering all major GST topics
- 💬 **Chat Interface** — Beautiful dark-gold Streamlit UI with chat history
- 🔍 **Source References** — Shows relevant document chunks for each answer
- ⚡ **Quick Questions** — Pre-built queries for common GST topics

## 📋 Topics Covered

| Category | Topics |
|----------|--------|
| Registration | Thresholds, process, documents |
| Tax Slabs | 0%, 5%, 12%, 18%, 28% with examples |
| Returns | GSTR-1, GSTR-3B, GSTR-9, GSTR-9C |
| ITC | Eligibility, blocked credits, reversal |
| E-invoicing | Applicability, process, IRN generation |
| E-way Bill | When required, generation, validity |
| Composition Scheme | Limits, eligibility, rates |
| Exports | Zero-rated, LUT, refund process |
| Penalties | Late fees, interest, offences |
| RCM | Reverse Charge Mechanism rules |

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/prime3436/gstwiz-bot.git
cd gstwiz-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
# Get a free key at: https://aistudio.google.com/app/apikey
```

### 4. Run the app
```bash
streamlit run main.py --server.fileWatcherType none
```

### 5. First-time setup in the UI
1. Click **⚡ Build DB** — builds the FAISS vector index (first run downloads ~80MB model)
2. Click **🤖 Load Bot** — loads the Gemini QA chain
3. Start asking GST questions!

## 📁 Project Structure

```
gstwiz-bot/
├── main.py            # Streamlit UI — dark gold chat interface
├── helper.py          # RAG pipeline — FAISS + HuggingFace + Gemini
├── gst_data.txt       # Knowledge base — 20-section GST guide (~37KB)
├── requirements.txt   # Python dependencies
├── .env.example       # API key template
└── .gitignore
```

## 🏗️ Architecture

```
User Query
    │
    ▼
HuggingFace Embeddings (all-MiniLM-L6-v2)
    │
    ▼
FAISS Vector Search → Top-4 relevant chunks
    │
    ▼
LangChain LCEL Chain
    │
    ▼
Google Gemini 1.5 Flash → Answer
```

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| UI | Streamlit 1.61 |
| LLM | Google Gemini 1.5 Flash |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| Framework | LangChain 1.x (LCEL) |
| Language | Python 3.9+ |

## 🔑 Environment Variables

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 📝 License

MIT License — free to use and modify.

---

> ⚠️ **Disclaimer**: GSTWiz provides general GST information only. Always consult a Chartered Accountant for specific tax advice. Official portal: [www.gst.gov.in](https://www.gst.gov.in)

> 🎓 Built as part of IBM SkillsBuild Internship — AICTE EduNet
