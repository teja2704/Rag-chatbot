import os
from typing import List
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader

# Optional online LLM (may fail)
import google.generativeai as genai

# Offline LLM
from transformers import pipeline

# -------------------------------------------------
# Environment
# -------------------------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 🔀 HYBRID SWITCH
# online  → try Gemini first
# offline → always use FLAN-T5
LLM_MODE = os.getenv("LLM_MODE", "offline")  # "online" or "offline"

# Online LLM (optional)
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-pro")
else:
    gemini_model = None

# Offline LLM (FLAN-T5)
local_llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=256
)

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "data", "knowledge_base")
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# -------------------------------------------------
# Load documents
# -------------------------------------------------
def load_documents() -> List[str]:
    docs = []

    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return docs

    for file in os.listdir(KNOWLEDGE_BASE_PATH):
        path = os.path.join(KNOWLEDGE_BASE_PATH, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                docs.append(f.read())

        elif file.endswith(".pdf"):
            reader = PdfReader(path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    docs.append(text)

    return docs

# -------------------------------------------------
# Chunking
# -------------------------------------------------
def chunk_text(text: str, size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

# -------------------------------------------------
# RAG Engine
# -------------------------------------------------
class RAGEngine:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.Client(
            Settings(persist_directory=CHROMA_DB_PATH)
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledge_base"
        )

        self._index_documents()

    def _index_documents(self):
        docs = load_documents()
        if not docs:
            return

        chunks = []
        for doc in docs:
            chunks.extend(chunk_text(doc))

        embeddings = self.embedder.encode(chunks).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        if self.collection.count() == 0:
            return []

        query_embedding = self.embedder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )

        return results.get("documents", [[]])[0]

    def generate_answer(self, query: str, contexts: List[str]) -> str:
        if not contexts:
            return "I don't know."

        context = "\n\n".join(contexts)

        prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}
"""

        # 🔵 ONLINE MODE (optional)
        if LLM_MODE == "online" and gemini_model:
            try:
                response = gemini_model.generate_content(prompt)
                return response.text
            except Exception:
                pass  # fall back silently

        # 🟢 OFFLINE MODE (FLAN-T5)
        result = local_llm(prompt)
        return result[0]["generated_text"]

# -------------------------------------------------
# Singleton
# -------------------------------------------------
rag_engine = RAGEngine()

# -------------------------------------------------
# Public API
# -------------------------------------------------
def answer_query(query: str) -> dict:
    contexts = rag_engine.retrieve(query)

    if not contexts:
        return {
            "answer": "I don't have enough information in my knowledge base yet.",
            "sources": []
        }

    answer = rag_engine.generate_answer(query, contexts)

    return {
        "answer": answer,
        "sources": contexts
    }
