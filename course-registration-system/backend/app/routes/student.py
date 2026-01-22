from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentOut

router = APIRouter(prefix="/students", tags=["students"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Public student registration
@router.post("/register", response_model=StudentOut)
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Find the coordinator of this college
    coordinator = db.query(User).filter(User.college_id == student.college_id, User.role == "coordinator").first()
    if not coordinator:
        raise HTTPException(status_code=400, detail="No coordinator assigned to this college")
    
    new_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        college_id=student.college_id,
        coordinator_id=coordinator.id
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
