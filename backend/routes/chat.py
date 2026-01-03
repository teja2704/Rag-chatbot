from flask import Blueprint, request, jsonify
from db.database import save_chat

# Import RAG function
from models.rag_engine import answer_query

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "").strip()
    user_id = data.get("user_id", 1)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Call RAG engine
    result = answer_query(query)

    answer = result.get("answer", "No answer generated.")
    sources = result.get("sources", [])

    # Save conversation
    save_chat(user_id, query, answer)

    return jsonify({
        "answer": answer,
        "sources": sources
    })
