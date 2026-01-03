from flask import Blueprint, request, jsonify
from db.database import save_chat

# Import RAG function (implemented by RAG engineer)
try:
    from models.rag_engine import answer_query
except ImportError:
    answer_query = None

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")
    user_id = data.get("user_id", 1)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    response = f"You asked: {query}"
    save_chat(user_id, query, response)

    return jsonify({"answer": response})


@chat_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query")
    user_id = data.get("user_id", 1)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    if answer_query is None:
        return jsonify({
            "answer": "RAG engine not integrated yet.",
            "sources": []
        })

    result = answer_query(query)

    save_chat(user_id, query, result["answer"])

    return jsonify(result)
