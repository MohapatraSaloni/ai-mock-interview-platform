<<<<<<< HEAD
# backend/models/question_answer.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class QuestionAnswer(BaseModel):
    id: Optional[str] = None
    session_id: str          # link to InterviewSession
    question_text: str
    answer_text: str
    created_at: datetime
    scores: Optional[Dict[str, float]] = None
    feedback: Optional[Dict[str, str]] = None
    # scores e.g. {"communication": 8, "technical": 7, "confidence": 6}
    # feedback e.g. {"communication": "Good clarity", ...}
=======
# backend/models/question_answer.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class QuestionAnswer(BaseModel):
    id: Optional[str] = None
    session_id: str          # link to InterviewSession
    question_text: str
    answer_text: str
    created_at: datetime
    scores: Optional[Dict[str, float]] = None
    feedback: Optional[Dict[str, str]] = None
    # scores e.g. {"communication": 8, "technical": 7, "confidence": 6}
    # feedback e.g. {"communication": "Good clarity", ...}
>>>>>>> 38ab0df3792f62ad8529ad491af9c9ae9a48a7c8
