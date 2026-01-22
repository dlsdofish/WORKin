from pydantic import BaseModel

class CollegeCreate(BaseModel):
    name: str

class CollegeOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
