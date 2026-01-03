def detect_intent(query: str) -> str:
    q = query.lower()

    if any(w in q for w in ["hi", "hello", "hey"]):
        return "greeting"

    if any(w in q for w in ["schedule", "report", "notify", "update"]):
        return "task"

    return "rag"
