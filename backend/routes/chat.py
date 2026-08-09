from flask import Blueprint, request, jsonify

# Import RAG function
from models.rag_engine import answer_query
from db.database import save_chat

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data.get("query", "").strip()
    user_id = data.get("user_id", 1)

    # Call RAG engine
    result = answer_query(query)

    answer = result.get("answer", "No answer generated.")
    sources = result.get("sources", [])

    save_chat(user_id, query, answer)

    return jsonify({
        "answer": answer,
        "sources": sources
    })
