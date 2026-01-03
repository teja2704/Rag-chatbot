from models.intent_model import detect_intent
from models.rag_engine import answer_query
from routes.tasks import execute_task


def handle_chat(query: str):
    intent = detect_intent(query)

    if intent == "greeting":
        return {"answer": "Hello! How can I help you?"}

    if intent == "task":
        return execute_task(query)

    return answer_query(query)
