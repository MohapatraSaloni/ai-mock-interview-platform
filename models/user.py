<<<<<<< HEAD
# backend/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None      # MongoDB _id as string
    name: str
    email: EmailStr
    role: Optional[str] = None    # e.g., "student", "job seeker"
=======
# backend/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None      # MongoDB _id as string
    name: str
    email: EmailStr
    role: Optional[str] = None    # e.g., "student", "job seeker"
>>>>>>> 38ab0df3792f62ad8529ad491af9c9ae9a48a7c8
