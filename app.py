import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title="HELIX AI",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Helix AI")
st.write("Welcome to Unwinding complexity. Inspired by the era of Tesla.")

# Initialize chat history using the plural key 'messages'
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar configurations
with st.sidebar:
    st.header("Model Configuration")
    
    # Select from Gemini model suite
    selected_model = st.selectbox(
        "Choose Gemini Engine",
        options=[
            "gemini-3.7-flash",        # Latest fast reasoning & coding workhorse
            "gemini-3.1-pro-preview",  # Frontier flagship for complex reasoning
            "gemini-3.5-flash-lite"    # Ultra-low latency / lightweight
        ],
        index=0
    )
    
    system_role = st.text_input(label="System Role", value="You are Helix AI, a helpful, precise assistant.")

# Ensure the system prompt is always active at index 0
if not st.session_state.messages:
    st.session_state.messages.append(SystemMessage(content=system_role))
elif isinstance(st.session_state.messages[0], SystemMessage):
    st.session_state.messages[0] = SystemMessage(content=system_role)

# Display existing conversation history (excluding SystemMessage)
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# Handle user input via Streamlit chat input component
if user_prompt := st.chat_input("Ask Helix AI something..."):
    # Append human input
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    with st.chat_message("user"):
        st.write(user_prompt)

    # Initialize Gemini model
    chat = ChatGoogleGenerativeAI(
        model=selected_model,
        temperature=0.5
    )

    # Stream model response in real time
    with st.chat_message("assistant"):
        with st.spinner("Helix AI is thinking..."):
            response = chat.invoke(st.session_state.messages)
            st.write(response.content)
            st.session_state.messages.append(AIMessage(content=response.content))