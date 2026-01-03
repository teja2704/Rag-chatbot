import streamlit as st
import requests

# ⚠️ CHANGE ONLY IF YOUR BACKEND PORT/ROUTE IS DIFFERENT
API_URL = "http://localhost:5000/chat"

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖"
)

st.title("🤖 RAG Chatbot")
st.write("Ask questions from the knowledge base")

# Store chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat history
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

# Input box
question = st.chat_input("Type your question here...")

if question:
    # Show user message
    st.session_state.chat.append(("user", question))
    with st.chat_message("user"):
        st.markdown(question)

    try:
        # Send request to backend
        response = requests.post(
            API_URL,
            json={"query": question},
            timeout=30
        )

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned")
        else:
            answer = "❌ Backend error"

    except Exception as e:
        answer = f"⚠️ Backend not reachable: {e}"

    # Show assistant reply
    st.session_state.chat.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)