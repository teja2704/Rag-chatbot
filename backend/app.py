from flask import Flask
from flask_cors import CORS

from routes.chat import chat_bp
from routes.tasks import tasks_bp
from db.database import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize database
    init_db()

    # Register routes
    app.register_blueprint(chat_bp)
    app.register_blueprint(tasks_bp)

    @app.route("/ping", methods=["GET"])
    def ping():
        return {"status": "Backend running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
