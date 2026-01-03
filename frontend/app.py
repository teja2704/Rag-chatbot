import streamlit as st
import requests

API_URL = "http://localhost:5000/chat"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# --- CSS for bubble-style chat ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2, #f6d365);
    font-family: 'Segoe UI', sans-serif;
}

/* Chat window */
.chat-container {
    max-width: 700px;
    margin: auto;
    margin-top: 40px;
    padding: 10px;
    height: 70vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* Chat bubble base */
.bubble {
    padding: 12px 18px;
    border-radius: 25px;
    max-width: 70%;
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    animation: fadeIn 0.3s ease-in-out;
    word-wrap: break-word;
}

/* User bubble */
.user {
    background: linear-gradient(135deg, #ff758c, #ff7eb3);
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 0px; /* tail effect */
}

/* Assistant bubble */
.assistant {
    background: linear-gradient(135deg, #43e97b, #38f9d7);
    color: #1f2937;
    align-self: flex-start;
    border-bottom-left-radius: 0px; /* tail effect */
}

/* Tail for user bubble */
.user::after {
    content: "";
    position: absolute;
    bottom: 0;
    right: -8px;
    width: 0;
    height: 0;
    border-top: 12px solid #ff758c;
    border-left: 12px solid transparent;
}

/* Tail for assistant bubble */
.assistant::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: -8px;
    width: 0;
    height: 0;
    border-top: 12px solid #43e97b;
    border-right: 12px solid transparent;
}

/* Avatars */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

/* Fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Input */
.stTextInput>div>input {
    border-radius: 25px;
    border: none;
    padding: 14px;
    font-size: 16px;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #ff758c, #ff7eb3);
    color: white;
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align:center;font-size:50px;color:#4f46e5;'>🤖 RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:18px;color:#374151;'>Ask anything from your knowledge base</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("💡 How to Use")
    st.markdown("""
    - Type your question and press Enter  
    - Chat history is saved during this session  
    - Backend must be running at port 5000  
    """)

# --- Chat history ---
if "chat" not in st.session_state:
    st.session_state.chat = []

def display_chat():
    html = '<div class="chat-container">'
    for role, msg in st.session_state.chat:
        if role == "user":
            html += f'<div class="bubble user"><img class="avatar" src="https://cdn-icons-png.flaticon.com/512/147/147144.png">{msg}</div>'
        else:
            html += f'<div class="bubble assistant"><img class="avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png">{msg}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

display_chat()

# --- Input ---
question = st.chat_input("Type your question here...")

if question:
    st.session_state.chat.append(("user", question))
    display_chat()

    try:
        response = requests.post(API_URL, json={"query": question}, timeout=30)
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned")
        else:
            answer = "❌ Backend error"
    except Exception as e:
        answer = f"⚠️ Backend not reachable: {e}"

    st.session_state.chat.append(("assistant", answer))
    display_chat()
