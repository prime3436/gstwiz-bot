"""
GSTWiz — Main Streamlit Application
AI-Powered GST & Tax Compliance Chatbot
"""

import os
import streamlit as st
from dotenv import load_dotenv
from helper import create_vector_db, get_qa_chain

load_dotenv()

st.set_page_config(
    page_title="GSTWiz | GST Compliance Bot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; font-family: 'Inter', sans-serif; }
html, body, .stApp { background: #0B1120 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2rem !important; max-width: 100% !important; }

/* ── FORCE ALL TEXT WHITE/VISIBLE ──────────────────────────────────── */
p, span, div, li, a, label,
h1, h2, h3, h4, h5, h6,
.stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown b,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] b,
[data-testid="stMarkdownContainer"] strong {
    color: #E2E8F0 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] b,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #CBD5E1 !important;
}

[data-testid="stSpinner"] p { color: #eab308 !important; }
.stSuccess p  { color: #14532d !important; }
.stError p    { color: #7f1d1d !important; }
.stWarning p  { color: #78350f !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0B1120; }
::-webkit-scrollbar-thumb { background: rgba(234,179,8,.4); border-radius: 99px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0D1526 !important;
    border-right: 1px solid rgba(234,179,8,.12);
    min-width: 260px !important; max-width: 280px !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg,#111827 0%,#1a2744 60%,#0f2040 100%);
    border: 1px solid rgba(234,179,8,.2); border-radius: 16px;
    padding: 22px 30px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 18px;
}
.hero-icon { font-size: 2.8rem; }
.hero-title {
    font-size: 1.9rem; font-weight: 800; margin: 0 0 4px;
    background: linear-gradient(90deg,#eab308,#fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { color: #94A3B8 !important; font-size: .87rem; margin: 0; }
.hero-pill {
    margin-left: auto; background: rgba(234,179,8,.08);
    border: 1px solid rgba(234,179,8,.3); border-radius: 20px;
    padding: 6px 16px; font-size: .74rem; font-weight: 700;
    color: #eab308 !important; white-space: nowrap;
}

/* ── Sidebar logo ── */
.sb-logo {
    text-align: center; padding: 16px 0 14px;
    border-bottom: 1px solid rgba(234,179,8,.1); margin-bottom: 14px;
}
.sb-logo .icon { font-size: 2.2rem; }
.sb-logo h2 {
    font-size: 1.4rem; font-weight: 800; margin: 4px 0 2px;
    background: linear-gradient(90deg,#eab308,#fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sb-logo .sub { font-size: .73rem; color: #64748B !important; margin: 0; }

/* ── Status pills ── */
.pill { display: inline-block; border-radius: 99px; padding: 4px 13px; font-size: .74rem; font-weight: 600; }
.pill-on  { background: rgba(34,197,94,.1);  border: 1px solid rgba(34,197,94,.35);  color: #4ade80 !important; }
.pill-off { background: rgba(239,68,68,.08); border: 1px solid rgba(239,68,68,.28); color: #f87171 !important; }

/* ── Sidebar quick-question buttons — HIGH CONTRAST ── */
div[data-testid="stSidebar"] .stButton > button {
    background: #1E2D4A !important;
    border: 1px solid rgba(234,179,8,.35) !important;
    color: #FFFFFF !important;
    font-size: .8rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    border-radius: 9px !important;
    padding: 9px 13px !important;
    width: 100% !important;
    margin: 3px 0 !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.45 !important;
    transition: all .18s !important;
}
div[data-testid="stSidebar"] .stButton > button p,
div[data-testid="stSidebar"] .stButton > button span {
    color: #FFFFFF !important;
    font-weight: 500 !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: #2A3F63 !important;
    border-color: #eab308 !important;
    color: #FEF08A !important;
    transform: translateX(3px) !important;
}
div[data-testid="stSidebar"] .stButton > button:hover p,
div[data-testid="stSidebar"] .stButton > button:hover span {
    color: #FEF08A !important;
}

/* ── Build / Load / Clear action buttons ── */
.btn-build button {
    background: linear-gradient(135deg,#eab308,#f59e0b) !important;
    color: #000 !important; font-weight: 700 !important;
    border: none !important; border-radius: 9px !important; font-size: .82rem !important;
}
.btn-load button {
    background: rgba(99,102,241,.18) !important;
    border: 1px solid rgba(99,102,241,.45) !important;
    color: #C7D2FE !important; font-weight: 600 !important;
    border-radius: 9px !important; font-size: .82rem !important;
}
.btn-clear button {
    background: rgba(239,68,68,.09) !important;
    border: 1px solid rgba(239,68,68,.28) !important;
    color: #FCA5A5 !important; border-radius: 9px !important; font-size: .78rem !important;
}

/* ── Stat cards ── */
.stat {
    background: rgba(17,24,39,.9); border: 1px solid rgba(234,179,8,.13);
    border-radius: 10px; padding: 10px 6px; text-align: center; margin: 3px 0;
}
.stat-n { font-size: 1.2rem; font-weight: 800; color: #eab308 !important; }
.stat-l { font-size: .68rem; color: #64748B !important; margin-top: 2px; }

/* ── Disclaimer ── */
.disc {
    background: rgba(234,179,8,.04); border: 1px solid rgba(234,179,8,.15);
    border-radius: 9px; padding: 9px 12px; font-size: .71rem;
    color: #94A3B8 !important; margin-top: 12px; line-height: 1.5;
}
.disc b { color: #fbbf24 !important; }

/* ── Divider ── */
.div { border-top: 1px solid rgba(234,179,8,.1); margin: 12px 0; }

/* ── Warning banner ── */
.warn {
    background: rgba(234,179,8,.06); border: 1px solid rgba(234,179,8,.2);
    border-radius: 10px; padding: 10px 16px; margin-bottom: 14px;
    font-size: .83rem; color: #FCD34D !important;
}
.warn b { color: #FEF08A !important; }

/* ── Error box (scrollable, contained) ── */
.err-box {
    background: rgba(239,68,68,.08); border: 1px solid rgba(239,68,68,.25);
    border-radius: 10px; padding: 10px 14px; margin: 8px 0;
    font-size: .74rem; color: #FCA5A5 !important; word-break: break-word;
    max-height: 160px; overflow-y: auto; line-height: 1.5;
}

/* ── Chat messages ── */
.msg { display: flex; margin: 12px 0; animation: fadeUp .3s ease; }
.msg.user { justify-content: flex-end; }
.msg.bot  { justify-content: flex-start; align-items: flex-start; gap: 10px; }

.av {
    width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg,#eab308,#f59e0b);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; box-shadow: 0 0 10px rgba(234,179,8,.3); margin-top: 2px;
}

.bub-u {
    background: linear-gradient(135deg,#1d4ed8,#1e3a8a);
    color: #F8FAFC !important; padding: 12px 17px;
    border-radius: 18px 18px 4px 18px; max-width: 76%;
    font-size: .89rem; line-height: 1.6;
    box-shadow: 0 2px 10px rgba(29,78,216,.3); word-wrap: break-word;
}

.bub-b {
    background: rgba(17,24,39,.95); border: 1px solid rgba(234,179,8,.15);
    color: #E2E8F0 !important; padding: 14px 18px;
    border-radius: 4px 18px 18px 18px; max-width: 80%;
    font-size: .89rem; line-height: 1.75;
    box-shadow: 0 2px 14px rgba(0,0,0,.4); word-wrap: break-word;
}
.bub-b b, .bub-b strong { color: #FCD34D !important; }
.bub-b ul { padding-left: 1.1rem; margin: 6px 0; }
.bub-b li { margin: 3px 0; color: #CBD5E1 !important; }
.bub-b p  { color: #E2E8F0 !important; margin: 4px 0; }

/* ── Source references ── */
.src {
    background: rgba(11,17,32,.9); border-left: 3px solid rgba(234,179,8,.5);
    border-radius: 0 8px 8px 0; padding: 8px 12px; margin: 5px 0;
    font-size: .76rem; color: #94A3B8 !important; line-height: 1.6;
}
.src b { color: #CBD5E1 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(11,17,32,.6) !important;
    border: 1px solid rgba(234,179,8,.12) !important; border-radius: 9px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p {
    color: #94A3B8 !important; font-size: .78rem !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] { border-top: 1px solid rgba(234,179,8,.15) !important; background: transparent !important; }
[data-testid="stChatInputTextArea"] {
    background: rgba(13,21,38,.95) !important;
    border: 1px solid rgba(234,179,8,.3) !important;
    color: #F1F5F9 !important; border-radius: 12px !important; font-size: .93rem !important;
}
[data-testid="stChatInputTextArea"]::placeholder { color: #475569 !important; }
[data-testid="stChatInputTextArea"]:focus {
    border-color: #eab308 !important; box-shadow: 0 0 0 2px rgba(234,179,8,.15) !important;
}
[data-testid="stChatInputSubmitButton"] svg { fill: #eab308 !important; }

/* ── Animations ── */
@keyframes fadeUp { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
@keyframes pulse  { 0%,100% { opacity:.4; transform:scale(.8); } 50% { opacity:1; transform:scale(1); } }
.dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #eab308; animation: pulse 1.2s infinite ease-in-out; margin: 0 2px;
}
.dot:nth-child(2) { animation-delay: .2s; }
.dot:nth-child(3) { animation-delay: .4s; }
</style>
""", unsafe_allow_html=True)

FAISS_INDEX = "faiss_gst_index"
for k, v in [("chat", []), ("chain", None), ("q_count", 0), ("err", ""), ("db_ok", os.path.exists(FAISS_INDEX))]:
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="icon">💰</div>
        <h2>GSTWiz</h2>
        <p class="sub">AI Tax Compliance Bot</p>
    </div>""", unsafe_allow_html=True)

    if st.session_state.chain:
        st.markdown('<span class="pill pill-on">● Bot Active</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill pill-off">● Not Ready</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🗃️ Setup**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="btn-build">', unsafe_allow_html=True)
        if st.button("⚡ Build DB", use_container_width=True):
            st.session_state.err = ""
            with st.spinner("Building knowledge base…"):
                try:
                    create_vector_db()
                    st.session_state.db_ok = True
                    st.success("Done!")
                except Exception as e:
                    st.session_state.err = str(e)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="btn-load">', unsafe_allow_html=True)
        if st.button("🤖 Load Bot", use_container_width=True):
            st.session_state.err = ""
            if st.session_state.db_ok:
                with st.spinner("Loading…"):
                    try:
                        st.session_state.chain = get_qa_chain()
                    except Exception as e:
                        st.session_state.err = str(e)
            else:
                st.session_state.err = "⚡ Build DB first!"
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.err:
        st.markdown(f'<div class="err-box">⚠️ {st.session_state.err}</div>', unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    st.markdown("**⚡ Quick Questions**")
    quick_qs = [
        "What is GST registration threshold?",
        "Explain all GST tax slabs with examples",
        "How to file GSTR-3B return?",
        "What is Input Tax Credit (ITC)?",
        "Who qualifies for Composition Scheme?",
        "What are GST penalties for late filing?",
        "How does Reverse Charge Mechanism work?",
        "What is E-invoicing? Who needs it?",
        "When is E-way Bill required?",
        "How is GST handled on exports?",
        "What is GST on rent?",
        "GST rate on restaurant food?",
    ]
    for q in quick_qs:
        if st.button(q, key=f"q_{q}"):
            st.session_state["_pq"] = q

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat"><div class="stat-n">{st.session_state.q_count}</div><div class="stat-l">Queries</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat"><div class="stat-n">5</div><div class="stat-l">Tax Slabs</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat"><div class="stat-n">13+</div><div class="stat-l">Returns</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.session_state.q_count = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="disc">
        ⚠️ <b>Disclaimer:</b> GSTWiz provides general GST information only.
        Always consult a <b>Chartered Accountant</b> for specific advice.
        Official portal: <b>www.gst.gov.in</b>
    </div>""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-icon">💰</div>
    <div>
        <p class="hero-title">GSTWiz — AI Tax Compliance Bot</p>
        <p class="hero-sub">Instant answers on GST · Returns · ITC · E-invoicing · Penalties · Exports</p>
    </div>
    <div class="hero-pill">🇮🇳 India GST Expert</div>
</div>""", unsafe_allow_html=True)

if not st.session_state.db_ok:
    st.markdown('<div class="warn">⚠️ Knowledge base not built yet — click <b>⚡ Build DB</b> in the sidebar, then <b>🤖 Load Bot</b>.</div>', unsafe_allow_html=True)

if not st.session_state.chat:
    st.markdown("""
    <div class="msg bot">
        <div class="av">💰</div>
        <div class="bub-b">
            👋 <b>Hello! I'm GSTWiz</b> — your AI-powered GST &amp; Tax Compliance assistant.<br><br>
            I can help you with:<br>
            <ul>
                <li>📋 GST Registration rules &amp; thresholds</li>
                <li>📊 Tax rates &amp; slabs for any product/service</li>
                <li>🧾 Filing returns — GSTR-1, GSTR-3B, GSTR-9</li>
                <li>💳 Input Tax Credit (ITC) eligibility &amp; rules</li>
                <li>🏪 Composition Scheme benefits &amp; limits</li>
                <li>📱 E-invoicing &amp; E-way Bill requirements</li>
                <li>⚖️ Penalties, interest &amp; compliance calendar</li>
            </ul>
            Use the <b>quick questions</b> in the sidebar or type below! 💡
        </div>
    </div>""", unsafe_allow_html=True)
else:
    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg user"><div class="bub-u">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg bot"><div class="av">💰</div><div class="bub-b">{msg["content"]}</div></div>', unsafe_allow_html=True)
            if msg.get("sources"):
                with st.expander(f"📄 {len(msg['sources'])} source references"):
                    for i, s in enumerate(msg["sources"][:3], 1):
                        st.markdown(f'<div class="src"><b>Ref {i}:</b> {s[:280]}{"..." if len(s) > 280 else ""}</div>', unsafe_allow_html=True)

pending = st.session_state.pop("_pq", None)
user_input = st.chat_input(
    "Ask your GST question… e.g. 'What is the GST rate on restaurant food?'",
    disabled=not st.session_state.chain,
)
user_input = user_input or pending

if user_input:
    if not st.session_state.chain:
        st.error("❌ Please click ⚡ Build DB then 🤖 Load Bot in the sidebar first.")
    else:
        st.session_state.chat.append({"role": "user", "content": user_input})
        st.session_state.q_count += 1

        ph = st.empty()
        ph.markdown(
            '<div class="msg bot"><div class="av">💰</div>'
            '<div class="bub-b"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>',
            unsafe_allow_html=True,
        )

        try:
            result = st.session_state.chain({"query": user_input})
            answer  = result.get("result", "Sorry, I couldn't generate an answer.")
            sources = [d.page_content for d in result.get("source_documents", [])]
        except Exception as e:
            answer  = f"⚠️ Error: {e}"
            sources = []

        ph.empty()
        st.session_state.chat.append({"role": "bot", "content": answer, "sources": sources})
        st.rerun()
