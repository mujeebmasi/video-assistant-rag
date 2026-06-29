import shutil
import tempfile
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.rag_engine import ask_question
from backend.services.pipeline import run_analysis

load_dotenv(override=True)

app = FastAPI(title="AI Meeting Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_sessions: dict[str, object] = {}


class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    source_type: str = Form(...),
    source_value: str = Form(""),
    file: UploadFile | None = File(None),
) -> dict:
    if source_type == "upload":
        if file is None:
            raise HTTPException(status_code=400, detail="A file is required for upload mode.")

        temp_dir = Path(tempfile.gettempdir()) / "ai_meeting_assistant"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / file.filename

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        source = str(temp_path)
    elif source_type in {"url", "local"}:
        if not source_value.strip():
            raise HTTPException(status_code=400, detail="source_value is required for this mode.")
        source = source_value.strip()
    else:
        raise HTTPException(status_code=400, detail="source_type must be url, upload, or local.")

    result = run_analysis(source)
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = result["rag_chain"]

    return {
        "session_id": session_id,
        "title": result["title"],
        "summary": result["summary"],
        "actionable_items": result["actionable_items"],
        "decisions": result["decisions"],
        "questions": result["questions"],
        "transcript": result["transcript"],
    }


@app.post("/chat/{session_id}")
def chat(session_id: str, payload: ChatRequest) -> dict:
    rag_chain = chat_sessions.get(session_id)
    if rag_chain is None:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    answer = ask_question(rag_chain, payload.question)
    return {"answer": answer}


@app.delete("/chat/{session_id}")
def clear_session(session_id: str) -> dict:
    chat_sessions.pop(session_id, None)
    return {"status": "deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
