import os

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv

# Load environment variables (.env file)
load_dotenv(find_dotenv(), override=True)

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="HELIX AI",
    page_icon="🧬",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Styling: dark glass UI + animated double‑helix mark
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(circle at 50% -10%, rgba(99,102,241,0.16), transparent 45%),
            radial-gradient(circle at 50% -20%, #1a103c, #090a0f 80%) !important;
        color: #f5f5fa !important;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stDecoration"], footer { display: none !important; }
    .block-container {
        padding: 3.5rem 1.5rem 6rem 1.5rem;
        max-width: 900px;
    }

    .helix-hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: clamp(4rem, 16vh, 9rem) 0 clamp(3rem, 10vh, 6rem);
        text-align: center;
    }
    .helix-logo-row {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .helix-mark {
        width: 3.5rem;
        height: 6rem;
        overflow: visible;
    }
    .helix-strand-base {
        fill: none;
        stroke: url(#helixGradient);
        stroke-linecap: round;
        stroke-width: 3.5;
        filter: drop-shadow(0 0 5px rgba(99,102,241,0.7));
    }
    .helix-title-wrap {
        position: relative;
        display: inline-block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2.5rem, 7vw, 5.5rem);
        font-weight: 700;
        line-height: 1;
        letter-spacing: 0;
    }
    .helix-title-base { color: rgba(255,255,255,0.16); }
    .helix-title-color {
        position: absolute;
        inset: 0;
        pointer-events: none;
        color: #d8d7ff;
        background: linear-gradient(90deg, #06b6d4, #818cf8, #c084fc);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        clip-path: inset(0 100% 0 0);
        animation: reveal-title 1.4s ease-out 0.2s forwards;
    }
    @keyframes reveal-title { to { clip-path: inset(0 0 0 0); } }
    .helix-subtitle {
        margin-top: 1.5rem;
        color: rgba(245,245,250,0.62);
        font-size: 0.95rem;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #a855f7, #6366f1);
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(20,16,45,0.95), rgba(9,10,15,0.98)) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * { color: #f1f1f7 !important; }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        color: #f5f5fa !important;
        -webkit-text-fill-color: #f5f5fa !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #f5f5fa !important;
        -webkit-text-fill-color: #f5f5fa !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #b8b5d3 !important;
    }
    section[data-testid="stSidebar"] input::placeholder {
        color: rgba(245,245,250,0.48) !important;
        -webkit-text-fill-color: rgba(245,245,250,0.48) !important;
    }

    .sidebar-brand {
        display: flex; align-items: center; gap: 0.6rem;
        padding: 0.4rem 0 1.2rem 0; margin-bottom: 1.2rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .sidebar-brand-mark {
        width: 30px; height: 30px; border-radius: 9px;
        background: linear-gradient(135deg, #f97362, #f59e0b 55%, #14b8a6);
        box-shadow: 0 0 18px rgba(249,115,98,0.35);
    }
    .sidebar-brand-text {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700; font-size: 1.05rem; letter-spacing: 0.2px;
    }

    .sidebar-section-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem; font-weight: 600;
        color: #a5a3c2 !important; text-transform: uppercase;
        letter-spacing: 1px; margin: 0.2rem 0 0.6rem 0;
    }

    /* Chat area */
    div[data-testid="stChatMessage"] {
        background: rgba(24,22,46,0.65) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 18px !important;
        padding: 0.35rem 0.4rem !important;
        margin-bottom: 0.9rem !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.28);
    }
    div[data-testid="stChatMessage"]:hover {
        border-color: rgba(168,85,247,0.35) !important;
    }

    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        border-left: 3px solid #06b6d4 !important;
    }
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        border-left: 3px solid #a855f7 !important;
    }

    div[data-testid="stChatInput"] {
        background: rgba(20,18,40,0.75) !important;
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        backdrop-filter: blur(12px);
    }
    div[data-testid="stChatInput"]:focus-within {
        border: 1px solid rgba(168,85,247,0.75) !important;
        box-shadow: 0 0 0 4px rgba(168,85,247,0.14), 0 10px 30px rgba(0,0,0,0.4);
    }

    .helix-footer {
        text-align: center; color: rgba(255,255,255,0.35);
        font-size: 0.78rem; letter-spacing: 0.4px; margin-top: 1.2rem;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #f7f4ee !important;
        color: #20242c !important;
    }
    header[data-testid="stHeader"] { background: #f7f4ee !important; }
    section[data-testid="stSidebar"] {
        background: #eeebe4 !important;
        border-right: 1px solid #d8d3ca;
    }
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #20242c !important;
        -webkit-text-fill-color: #20242c !important;
    }
    section[data-testid="stSidebar"] .sidebar-section-label {
        color: #5f5b55 !important;
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #fffdf9 !important;
        border-color: #c9c3b9 !important;
        color: #20242c !important;
        -webkit-text-fill-color: #20242c !important;
    }
    section[data-testid="stSidebar"] input::placeholder {
        color: #77736c !important;
        -webkit-text-fill-color: #77736c !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #20242c !important;
        -webkit-text-fill-color: #20242c !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #5f5b55 !important;
    }
    div[data-testid="stChatMessage"] {
        background: #fffdf9 !important;
        border-color: #ded8cf !important;
        color: #20242c !important;
        box-shadow: 0 8px 24px rgba(63,55,42,0.08);
    }
    div[data-testid="stChatInput"] {
        background: #fffdf9 !important;
        border-color: #c9c3b9 !important;
        color: #20242c !important;
        box-shadow: 0 10px 30px rgba(63,55,42,0.12);
    }
    div[data-testid="stChatInput"] textarea {
        color: #20242c !important;
        -webkit-text-fill-color: #20242c !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #77736c !important;
        -webkit-text-fill-color: #77736c !important;
    }

    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: min(78vw, 360px) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding: 1.25rem 1rem 2rem 1rem;
        }
        .sidebar-brand { margin-bottom: 1rem; }
        .sidebar-section-label { font-size: 0.7rem; }
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] [data-baseweb="select"] {
            font-size: 0.95rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero: animated double‑helix mark + colour‑reveal wordmark
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="helix-hero">
        <div class="helix-logo-row">
            <svg class="helix-mark" viewBox="0 0 50 140" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="helixGradient" x1="0%" y1="100%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#14b8a6"/>
                        <stop offset="55%" stop-color="#f59e0b"/>
                        <stop offset="100%" stop-color="#f97362"/>
                    </linearGradient>
                </defs>
                <path class="helix-strand-base" d="M12,0 C42,14 42,28 12,42 S-18,70 12,84 S42,112 12,126"/>
                <path class="helix-strand-base" d="M38,0 C8,14 8,28 38,42 S68,70 38,84 S8,112 38,126"/>
            </svg>
            <span class="helix-title-wrap">
                <span class="helix-title-base">HELIX AI</span>
                <span class="helix-title-color">HELIX AI</span>
            </span>
        </div>
        <div class="helix-subtitle">Unwinding complexity. Inspired by the era of Tesla.</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chat Logic
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark"></div>
            <div class="sidebar-brand-text">HELIX AI</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Engine</div>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        "Choose Gemini Model",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash-lite"],
        index=0
    )

    st.markdown('<div class="sidebar-section-label" style="margin-top:1.2rem;">Persona</div>', unsafe_allow_html=True)
    system_role = st.text_input(
        "System Prompt",
        value="You are Helix AI, an expert, high‑precision assistant built to simplify complex concepts."
    )

    st.markdown(
        '<div style="margin-top:1.5rem; font-size:0.72rem; color:rgba(255,255,255,0.35);">'
        'HELIX AI · powered by Gemini</div>',
        unsafe_allow_html=True
    )

# Maintain system prompt
if not st.session_state.messages:
    st.session_state.messages.append(SystemMessage(content=system_role))
elif isinstance(st.session_state.messages[0], SystemMessage):
    st.session_state.messages[0] = SystemMessage(content=system_role)

# Render chat history
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🧬"):
            st.write(msg.content)

# Handle chat input and streaming
if user_prompt := st.chat_input("Ask Helix AI anything..."):
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_prompt)

    with st.chat_message("assistant", avatar="🧬"):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            response_text = "Add GOOGLE_API_KEY or GEMINI_API_KEY to your .env file to enable Helix AI."
            st.error(response_text)
        else:
            try:
                model = ChatGoogleGenerativeAI(
                    model=selected_model,
                    temperature=0.2,
                    google_api_key=api_key,
                )
                response_text = st.write_stream(
                    chunk.content
                    for chunk in model.stream(st.session_state.messages)
                )
            except Exception as error:
                response_text = f"I couldn't complete that request: {error}"
                st.error(response_text)

        st.session_state.messages.append(AIMessage(content=response_text))