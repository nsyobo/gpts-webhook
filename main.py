from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

class Payload(BaseModel):
    message: str

@app.post("/webhook")
async def webhook(payload: Payload):
    log = {
        "time": datetime.utcnow().isoformat(),
        "message": payload.message
    }

    with open("logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    return {"reply": "ok"}
