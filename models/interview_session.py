# backend/models/interview_session.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class InterviewSession(BaseModel):
    id: Optional[str] = None
    user_id: str              # link to User
    role: str                 # e.g. "ML Engineer", "Data Analyst"
    start_time: datetime
    end_time: Optional[datetime] = None
    overall_scores: Optional[Dict[str, float]] = None
    # e.g. {"communication": 7.5, "technical": 8.0, "confidence": 6.5}
