import streamlit as st
import requests

# Backend API URL
API_URL = "http://localhost:5000/chat"

# Page setup
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
/* Page background */
body {
    background: linear-gradient(to right, #e0e7ff, #f0f2f6);
}

/* Header style */
h1 {
    color: #4f46e5;
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
}

/* Chat container */
.chat-container {
    max-width: 700px;
    margin: auto;
    padding: 10px;
    height: 65vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* Chat bubbles */
.chat-message {
    padding: 12px 16px;
    border-radius: 20px;
    max-width: 70%;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.4;
    animation: fadeIn 0.3s ease-in-out;
}

/* User messages */
.user-message {
    background-color: #4f46e5;
    color: white;
    margin-left: auto;
}

/* Assistant messages */
.assistant-message {
    background-color: #e0e7ff;
    color: #1e1e1e;
    margin-right: auto;
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Input box style */
.stTextInput>div>input {
    border-radius: 12px;
    border: 1px solid #ccc;
    padding: 10px;
}

/* Button style */
.stButton>button {
    background-color: #4f46e5;
    color: white;
    border-radius: 12px;
    padding: 8px 20px;
    font-weight: bold;
    transition: 0.2s;
}
.stButton>button:hover {
    background-color: #3730a3;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 RAG Chatbot")
st.markdown("<p style='text-align:center; font-size:16px;'>Ask questions from your knowledge base</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("💡 How to Use")
    st.markdown("""
    - Type your question below and press Enter  
    - Chat history will be saved during this session  
    - Ensure your backend is running at port 5000  
    - Enjoy AI-powered responses in real time!
    """)

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat container
chat_html = '<div class="chat-container">'
for role, msg in st.session_state.chat:
    if role == "user":
        chat_html += f'<div class="chat-message user-message">👤 {msg}</div>'
    else:
        chat_html += f'<div class="chat-message assistant-message">🤖 {msg}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Input
question = st.chat_input("Type your question here...")

if question:
    # Add user message
    st.session_state.chat.append(("user", question))
    
    # Show updated chat
    chat_html = '<div class="chat-container">'
    for role, msg in st.session_state.chat:
        if role == "user":
            chat_html += f'<div class="chat-message user-message">👤 {msg}</div>'
        else:
            chat_html += f'<div class="chat-message assistant-message">🤖 {msg}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Call backend
    try:
        response = requests.post(API_URL, json={"query": question}, timeout=30)
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned")
        else:
            answer = "❌ Backend error"
    except Exception as e:
        answer = f"⚠️ Backend not reachable: {e}"

    # Add assistant message
    st.session_state.chat.append(("assistant", answer))

    # Show updated chat with assistant
    chat_html = '<div class="chat-container">'
    for role, msg in st.session_state.chat:
        if role == "user":
            chat_html += f'<div class="chat-message user-message">👤 {msg}</div>'
        else:
            chat_html += f'<div class="chat-message assistant-message">🤖 {msg}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
