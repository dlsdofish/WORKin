from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import SessionLocal
from app.models.class import Class
from app.models.class_student import ClassStudent
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.attendance_record import AttendanceRecord
from app.schemas.student import StudentOut
from app.core.dependencies import teacher_only

router = APIRouter(prefix="/teacher", tags=["teacher"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#view classes assigned to the teacher
@router.get("/classes")
def get_classes(user=Depends(teacher_only), db: Session = Depends(get_db)):
    classes = db.query(Class).filter(Class.teacher_id == user.id).all()
    return [{"id": c.id, "name": c.name, "college_id": c.college_id} for c in classes]

#view students in a class
@router.get("/classes/{class_id}/students", response_model=List[StudentOut])
def get_class_students(class_id: int, user=Depends(teacher_only), db: Session = Depends(get_db)):
    # Verify class belongs to this teacher
    class_obj = db.query(Class).filter(Class.id == class_id, Class.teacher_id == user.id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found or unauthorized")
    
    student_mappings = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
    students = [db.query(Student).filter(Student.id == mapping.student_id).first() for mapping in student_mappings]
    return students

#mark attendance for a class on a specific date
@router.post("/classes/{class_id}/attendance")
def take_attendance(class_id: int, student_ids_present: List[int], user=Depends(teacher_only), db: Session = Depends(get_db)):
    # Verify class belongs to teacher
    class_obj = db.query(Class).filter(Class.id == class_id, Class.teacher_id == user.id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found or unauthorized")
    
    today = date.today()
    attendance_entry = Attendance(class_id=class_id, teacher_id=user.id, date=today)
    db.add(attendance_entry)
    db.commit()
    db.refresh(attendance_entry)
    
    # Record each student's attendance
    student_mappings = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
    for mapping in student_mappings:
        status = "Present" if mapping.student_id in student_ids_present else "Absent"
        record = AttendanceRecord(attendance_id=attendance_entry.id, student_id=mapping.student_id, status=status)
        db.add(record)
    
    db.commit()
    return {"message": "Attendance recorded successfully", "attendance_id": attendance_entry.id}

