from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime
import os

app = FastAPI()
LOG_FILE = "logs.jsonl"

class Payload(BaseModel):
    user: str
    message: str

@app.post("/webhook")
async def save_message(payload: Payload):
    log_entry = {
        "time": datetime.utcnow().isoformat(),
        "user": payload.user,
        "message": payload.message
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    return {"status": "logged"}

@app.get("/logs")
async def get_logs(limit: int = 50):
    if not os.path.exists(LOG_FILE):
        return {"logs": []}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    latest = lines[-limit:]
    logs = [json.loads(line) for line in latest]
    return {"logs": logs}
