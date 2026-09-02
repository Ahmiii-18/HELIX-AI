import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables (.env file)
load_dotenv(find_dotenv(), override=True)

# ---------------------------------------------------------------------------
# Page Configuration (MUST BE THE FIRST STREAMLIT COMMAND)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="HELIX AI",
    page_icon="🧬",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Styling: Off-White System with Modest Palette (Slate, Muted Teal & Indigo)
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Main Application - Warm Off-White */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #f8f6f0 !important;
        color: #262c36 !important;
    }

    header[data-testid="stHeader"] { 
        background: #f8f6f0 !important; 
    }
    
    [data-testid="stDecoration"], footer { display: none !important; }

    .block-container {
        padding: 3rem 1.5rem 6rem 1.5rem;
        max-width: 900px;
    }

    /* Sidebar - Muted Sand */
    section[data-testid="stSidebar"] {
        background: #eeebe3 !important;
        border-right: 1px solid #dcd7ce !important;
    }

    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #262c36 !important;
        -webkit-text-fill-color: #262c36 !important;
    }

    section[data-testid="stSidebar"] .sidebar-section-label {
        color: #5c6270 !important;
    }

    /* Inputs & Select Boxes */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #d0c9bc !important;
        color: #262c36 !important;
        -webkit-text-fill-color: #262c36 !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] input::placeholder {
        color: #8c877d !important;
        -webkit-text-fill-color: #8c877d !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #262c36 !important;
        -webkit-text-fill-color: #262c36 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #5c6270 !important;
    }

    .sidebar-brand {
        display: flex; align-items: center; gap: 0.6rem;
        padding: 0.4rem 0 1.2rem 0; margin-bottom: 1.2rem;
        border-bottom: 1px solid #dcd7ce;
    }
    
    .sidebar-brand-mark {
        width: 30px; height: 30px; border-radius: 9px;
        background: linear-gradient(135deg, #2b5c6f, #4a6fa5);
        box-shadow: 0 2px 8px rgba(43, 92, 111, 0.2);
    }

    .sidebar-brand-text {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700; font-size: 1.05rem; letter-spacing: 0.2px;
        color: #262c36 !important;
    }

    .sidebar-section-label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem; font-weight: 600;
        color: #5c6270 !important; text-transform: uppercase;
        letter-spacing: 1px; margin: 0.2rem 0 0.6rem 0;
    }

    /* Hero Section Header */
    .helix-hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: clamp(2rem, 8vh, 4rem) 0 clamp(2rem, 6vh, 3rem);
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

    .helix-title-base { color: #dcd7ce; }

    /* Modest Title Gradient: Slate Teal to Deep Indigo */
    .helix-title-color {
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: linear-gradient(90deg, #2b5c6f 0%, #3b5998 50%, #5a4b81 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        clip-path: inset(0 100% 0 0);
        animation: reveal-title 1.4s ease-out 0.2s forwards;
    }

    @keyframes reveal-title { to { clip-path: inset(0 0 0 0); } }

    .helix-subtitle {
        margin-top: 1.2rem;
        color: #5c6270;
        font-size: 0.95rem;
    }

    /* Chat Messages */
    div[data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e2ddd3 !important;
        border-radius: 18px !important;
        padding: 0.5rem 0.8rem !important;
        margin-bottom: 0.9rem !important;
        color: #262c36 !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.02);
    }

    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        border-left: 3px solid #2b5c6f !important;
    }

    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        border-left: 3px solid #5a4b81 !important;
    }

    div[data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 1px solid #d0c9bc !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    }

    div[data-testid="stChatInput"] textarea {
        color: #262c36 !important;
        -webkit-text-fill-color: #262c36 !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8c877d !important;
        -webkit-text-fill-color: #8c877d !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb {
        background: #c5bfb4;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero Header with Modest SVG Helix Gradient
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="helix-hero">
        <div class="helix-logo-row">
            <svg class="helix-mark" viewBox="0 0 50 140" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="helixGradient" x1="0%" y1="100%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#2b5c6f"/>
                        <stop offset="50%" stop-color="#3b5998"/>
                        <stop offset="100%" stop-color="#5a4b81"/>
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

# Sidebar Controls
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark"></div>
            <div class="sidebar-brand-text">HELIX AI</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Engine</div>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        "Choose OpenAI Model",
        options=[
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-3.5-turbo"
        ],
        index=0
    )

    st.markdown('<div class="sidebar-section-label" style="margin-top:1.2rem;">Persona</div>', unsafe_allow_html=True)
    system_role = st.text_input(
        "System Prompt",
        value="You are Helix AI, an expert, high‑precision assistant built to simplify complex concepts."
    )

    st.markdown(
        '<div style="margin-top:1.5rem; font-size:0.72rem; color:#5c6270;">'
        'HELIX AI · powered by OpenAI</div>',
        unsafe_allow_html=True
    )

# Maintain system prompt
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": system_role})
else:
    st.session_state.messages[0] = {"role": "system", "content": system_role}

# Render chat history
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="🧬"):
            st.write(msg["content"])

# Handle chat input and streaming
if user_prompt := st.chat_input("Ask Helix AI anything..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_prompt)

    with st.chat_message("assistant", avatar="🧬"):
        # Retrieve OpenAI API Key
        api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            response_text = "Add OPENAI_API_KEY to your environment variables or secrets to enable Helix AI."
            st.error(response_text)
        else:
            try:
                client = OpenAI(api_key=api_key)
                
                # Stream completion from OpenAI directly
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages,
                    temperature=0.2,
                    stream=True
                )
                
                response_text = st.write_stream(
                    chunk.choices[0].delta.content or ""
                    for chunk in stream
                )
            except Exception as error:
                response_text = f"I couldn't complete that request: {error}"
                st.error(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})