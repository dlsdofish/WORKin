from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.class import Class
from app.models.student import Student
from app.models.user import User
from app.models.class_student import ClassStudent
from app.schemas.student import StudentOut
from app.core.dependencies import get_current_user, coordinator_only

router = APIRouter(prefix="/coordinator", tags=["coordinator"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/classes")
def create_class(name: str, teacher_id: int, user=Depends(coordinator_only), db: Session = Depends(get_db)):
    # Coordinator can only create classes in their college
    new_class = Class(
        name=name,
        college_id=user.college_id,
        teacher_id=teacher_id
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return {"message": "Class created successfully", "class_id": new_class.id}

@router.post("/classes/{class_id}/assign-students")
def assign_students_to_class(class_id: int, student_ids: List[int], user=Depends(coordinator_only), db: Session = Depends(get_db)):
    # Check class belongs to coordinator's college
    class_obj = db.query(Class).filter(Class.id == class_id, Class.college_id == user.college_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found or unauthorized")

    # Assign each student
    for student_id in student_ids:
        student = db.query(Student).filter(Student.id == student_id, Student.college_id == user.college_id).first()
        if not student:
            continue  # skip invalid students
        # Check if already assigned
        existing = db.query(ClassStudent).filter(ClassStudent.class_id == class_id, ClassStudent.student_id == student_id).first()
        if existing:
            continue
        mapping = ClassStudent(class_id=class_id, student_id=student_id)
        db.add(mapping)

    db.commit()
    return {"message": f"{len(student_ids)} students assigned successfully"}

@router.get("/students", response_model=List[StudentOut])
def get_students(user=Depends(coordinator_only), db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.college_id == user.college_id).all()
    return students

