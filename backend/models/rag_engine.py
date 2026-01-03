import os
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "data", "knowledge_base")


def load_documents() -> List[str]:
    docs = []

    for file in os.listdir(KNOWLEDGE_BASE_PATH):
        path = os.path.join(KNOWLEDGE_BASE_PATH, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                docs.append(f.read())

        elif file.endswith(".pdf"):
            reader = PdfReader(path)
            for page in reader.pages:
                docs.append(page.extract_text())

    return docs

def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap

    return chunks


class RAGEngine:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.Client(
            Settings(persist_directory="chroma_db")
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledge_base"
        )

        self._index_documents()

    def _index_documents(self):
        docs = load_documents()
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


    def retrieve(self, query: str, k: int = 3):
        query_embedding = self.embedder.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )

        return results["documents"][0]


    def generate_answer(self, query: str, contexts: List[str]) -> str:
        context = "\n\n".join(contexts)

        prompt = f"""
Answer ONLY using the context below.
If not found, say "I don't know".

Context:
{context}

Question:
{query}
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message["content"]

rag_engine = RAGEngine()


def answer_query(query: str) -> dict:
    contexts = rag_engine.retrieve(query)
    answer = rag_engine.generate_answer(query, contexts)

    return {
        "answer": answer,
        "sources": contexts
    }

