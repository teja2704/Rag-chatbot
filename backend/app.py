from flask import Flask, request, jsonify
from flask_cors import CORS

from routes.chat import handle_chat

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    return jsonify(handle_chat(query))

if __name__ == "__main__":
    app.run(debug=True)
