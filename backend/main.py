from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid

from ai.ai_client import (
    generate_question,
    evaluate_answer,
    generate_final_summary,
)

# Optional: if db.py exists, we use it; if not, we just ignore db in test-db
try:
    from db import db
except ImportError:
    db = None

# -------------------------------------------------
# Create FastAPI app ONCE
# -------------------------------------------------
app = FastAPI(
    title="AI Mock Interview Backend",
    description="FastAPI backend for AI-powered mock interview platform using Gemini",
    version="1.0.0",
)

# -------------------------------------------------
# CORS middleware (so frontend at localhost:5173 can call backend)
# -------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # you can use ["*"] during dev if you prefer
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# In-memory session store (temporary)
# -------------------------------------------------
_sessions: Dict[str, List[Dict[str, Any]]] = {}

# -------------------------------------------------
# Pydantic models
# -------------------------------------------------
class StartInterviewRequest(BaseModel):
    role: str
    user_id: str | None = "guest"


class SubmitAnswerRequest(BaseModel):
    session_id: str
    role: str
    question: str
    answer: str


class FinalFeedbackRequest(BaseModel):
    session_id: str
    role: str


# -------------------------------------------------
# Health & test routes
# -------------------------------------------------
@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/test-db")
def test_db():
    if db is None:
        return {"error": "MongoDB (db) not configured"}
    try:
        return {"collections": db.list_collection_names()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test-question")
def test_question():
    try:
        q = generate_question("Machine Learning Engineer", [])
        return {"question": q}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test-eval")
def test_eval():
    try:
        q = "Explain overfitting in simple terms."
        a = "Overfitting is when a model memorizes training data instead of learning patterns."
        result = evaluate_answer("Machine Learning Engineer", q, a)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {
        "message": "AI Mock Interview Backend is running",
        "endpoints": [
            "/ping",
            "/test-question",
            "/test-eval",
            "/start-interview",
            "/submit-answer",
            "/final-feedback",
        ],
    }


# -------------------------------------------------
# Core Interview APIs
# -------------------------------------------------
@app.post("/start-interview")
def start_interview(req: StartInterviewRequest):
    """
    Start a new interview:
    - Create a new session_id
    - Initialize empty Q&A history
    - Generate first question using Gemini
    """
    try:
        session_id = str(uuid.uuid4())
        _sessions[session_id] = []

        first_question = generate_question(req.role, history=[])

        return {
            "session_id": session_id,
            "question": first_question,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit-answer")
def submit_answer(req: SubmitAnswerRequest):
    """
    Submit one answer:
    - Evaluate answer (scores + feedback)
    - Append Q&A with scores to session history
    - Generate next question using updated history
    """
    if req.session_id not in _sessions:
        raise HTTPException(status_code=400, detail="Invalid session_id")

    try:
        # 1. Evaluate answer
        eval_result = evaluate_answer(req.role, req.question, req.answer)

        # 2. Save to session history
        _sessions[req.session_id].append(
            {
                "question": req.question,
                "answer": req.answer,
                "scores": eval_result,
            }
        )

        # 3. Generate next question, using entire history for context
        history = [
            {"question": qa["question"], "answer": qa["answer"]}
            for qa in _sessions[req.session_id]
        ]
        next_question = generate_question(req.role, history=history)

        return {
            "scores": eval_result,
            "next_question": next_question,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/final-feedback")
def final_feedback(req: FinalFeedbackRequest):
    """
    End the interview and get final feedback:
    - Use full Q&A history + per-question scores
    - Generate overall scores, strengths, weaknesses, and improvement plan
    """
    if req.session_id not in _sessions:
        raise HTTPException(status_code=400, detail="Invalid session_id")

    try:
        qa_list = _sessions[req.session_id]
        summary = generate_final_summary(req.role, qa_list)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
