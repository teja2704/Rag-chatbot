from flask import Blueprint, request, jsonify

# Import RAG function
from models.rag_engine import answer_query

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data.get("query", "").strip()

    # Call RAG engine
    result = answer_query(query)

    answer = result.get("answer", "No answer generated.")
    sources = result.get("sources", [])

    return jsonify({
        "answer": answer,
        "sources": sources
    })
