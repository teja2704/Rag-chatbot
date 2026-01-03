from flask import Blueprint, request, jsonify

from models.rag_engine import answer_query

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data or "query" not in data:
            return jsonify({"error": "Query is required"}), 400

        query = data["query"]

        result = answer_query(query)

        return jsonify(result), 200

    except Exception as e:
        # IMPORTANT: expose error so we stop guessing
        return jsonify({
            "error": "Chat endpoint failed",
            "details": str(e)
        }), 500
