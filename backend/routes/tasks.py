def execute_task(query: str):
    if "report" in query.lower():
        return {"status": "success", "message": "Report generated"}

    if "schedule" in query.lower():
        return {"status": "success", "message": "Event scheduled"}

    return {"status": "failed", "message": "Task not recognized"}
