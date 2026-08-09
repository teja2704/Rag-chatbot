import streamlit as st
import requests

# -------------------------------------------------
# Backend API
# -------------------------------------------------
API_URL = "http://localhost:5000/chat"

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2, #0f172a);
    font-family: 'Segoe UI', sans-serif;
}

/* Chat bubble base */
.bubble {
    padding: 14px 20px;
    border-radius: 22px;
    max-width: 75%;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
    animation: fadeIn 0.25s ease-in-out;
    word-wrap: break-word;
    white-space: pre-wrap;
}

/* User bubble */
.user {
    background: linear-gradient(135deg, #ff758c, #ff7eb3);
    color: white;
    margin-left: auto;
}

/* Assistant bubble */
.assistant {
    background: linear-gradient(135deg, #43e97b, #38f9d7);
    color: #1f2937;
    margin-right: auto;
}

/* Avatar */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

/* Fade animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Chat input */
.stChatInput textarea {
    border-radius: 25px !important;
    padding: 12px !important;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;color:#e5e7eb;'>🤖 RAG Chatbot</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#cbd5f5;'>Ask questions grounded in your knowledge base</p>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# Sidebar (UPDATED ABOUT SECTION)
# -------------------------------------------------
with st.sidebar:
    st.markdown("## 🤖 RAG Chatbot")

    st.markdown(
        """
        **An offline-first, explainable AI assistant**  
        that answers questions using your own documents.
        """
    )

    st.markdown("---")

    st.markdown("### 🚀 Key Capabilities")
    st.markdown(
        """
        - 🔍 Semantic document retrieval  
        - 🧠 Context-aware answer generation  
        - 📚 Transparent source attribution  
        - ⚡ Runs fully offline  
        """
    )

    st.markdown("---")

    st.markdown("### 🛠 Tech Stack")
    st.markdown(
        """
        - **Embeddings:** SentenceTransformers  
        - **Vector DB:** ChromaDB  
        - **LLM:** FLAN-T5  
        - **UI:** Streamlit  
        """
    )

    st.markdown("---")
    st.caption("💡 Tip: Ask factual questions related to the uploaded knowledge base.")

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_query" not in st.session_state:
    st.session_state.last_query = None

# -------------------------------------------------
# Helper: Format Answer + Sources
# -------------------------------------------------
def format_answer(answer, sources):
    formatted = answer.strip()

    formatted += (
        "\n\nℹ️ *This answer was generated using retrieved documents "
        "from the knowledge base (RAG).*"
    )

    if sources:
        with st.expander("📚 Show sources used"):
            for i, src in enumerate(sources, 1):
                snippet = src.replace("\n", " ")[:300]
                st.markdown(f"**Source {i}:** {snippet}...")

    return formatted

# -------------------------------------------------
# Empty State
# -------------------------------------------------
if not st.session_state.messages:
    st.info("👋 Ask your first question to get started.")

# -------------------------------------------------
# Render Chat History
# -------------------------------------------------
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(
            f"""
            <div class="bubble user">
                <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/147/147144.png">
                <span>{message}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="bubble assistant">
                <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png">
                <span>{message}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------------------------
# Chat Input
# -------------------------------------------------
user_query = st.chat_input("Type your question and press Enter...")

if user_query and user_query != st.session_state.last_query:
    st.session_state.last_query = user_query

    # Store user message
    st.session_state.messages.append(("user", user_query))

    with st.spinner("🤖 Thinking..."):
        try:
            response = requests.post(
                API_URL,
                json={"query": user_query},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])
                formatted_answer = format_answer(answer, sources)
            else:
                formatted_answer = "❌ Backend error. Please try again."

        except Exception as e:
            formatted_answer = f"⚠️ Backend not reachable.\n\n{e}"

    # Store assistant message
    st.session_state.messages.append(("assistant", formatted_answer))

    st.rerun()
