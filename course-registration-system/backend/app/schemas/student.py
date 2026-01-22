from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    college_id: int  # dropdown in form

class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    college_id: int
    coordinator_id: int

    class Config:
        orm_mode = True
