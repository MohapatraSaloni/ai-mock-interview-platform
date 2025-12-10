# backend/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None      # MongoDB _id as string
    name: str
    email: EmailStr
    role: Optional[str] = None    # e.g., "student", "job seeker"
