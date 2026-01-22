from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import SessionLocal
from app.models.college import College
from app.models.class import Class
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.attendance_record import AttendanceRecord
from app.core.dependencies import admin_only

router = APIRouter(prefix="/reports", tags=["reports"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#collge-wise student attendance report
@router.get("/college/{college_id}/students")
def college_students(college_id: int, db: Session = Depends(get_db), user=Depends(admin_only)):
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    students = db.query(Student).filter(Student.college_id == college_id).all()
    return [{"id": s.id, "name": s.name, "email": s.email} for s in students]

#class-wise attendance report
@router.get("/class/{class_id}/attendance")
def class_attendance(class_id: int, db: Session = Depends(get_db), user=Depends(admin_only)):
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    
    attendance_entries = db.query(Attendance).filter(Attendance.class_id == class_id).all()
    report = []
    
    for entry in attendance_entries:
        records = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_id == entry.id).all()
        report.append({
            "date": entry.date,
            "teacher_id": entry.teacher_id,
            "attendance": [{"student_id": r.student_id, "status": r.status} for r in records]
        })
    
    return {"class_id": class_id, "class_name": cls.name, "attendance_report": report}

#college-wise attendance summary
@router.get("/college/{college_id}/attendance-summary")
def college_attendance_summary(college_id: int, db: Session = Depends(get_db), user=Depends(admin_only)):
    students = db.query(Student).filter(Student.college_id == college_id).all()
    summary = []
    
    for student in students:
        records = db.query(AttendanceRecord).join(Attendance).filter(AttendanceRecord.student_id == student.id).all()
        total_classes = len(records)
        present_count = sum(1 for r in records if r.status == "Present")
        summary.append({
            "student_id": student.id,
            "student_name": student.name,
            "total_classes": total_classes,
            "present": present_count,
            "absent": total_classes - present_count,
            "attendance_percentage": (present_count / total_classes * 100) if total_classes > 0 else 0
        })
    
    return {"college_id": college_id, "attendance_summary": summary}

