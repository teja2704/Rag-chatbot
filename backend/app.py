from flask import Flask
from flask_cors import CORS

from routes.chat import chat_bp
#from routes.tasks import tasks_bp
from db.database import init_db


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Initialize database (once at startup)
    init_db()

    # Register blueprints
    app.register_blueprint(chat_bp)
    #app.register_blueprint(tasks_bp)

    @app.route("/ping", methods=["GET"])
    def ping():
        return {"status": "Backend running"}

    return app


# -------------------------------------------------
# App entry point
# -------------------------------------------------
if __name__ == "__main__":
    app = create_app()

    # IMPORTANT:
    # - debug=False → no Werkzeug PIN
    # - use_reloader=False → prevents double execution on Windows
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
