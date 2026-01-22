from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    attendance_id = Column(Integer, ForeignKey("attendance.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(String, default="Absent")  # Present / Absent

    attendance = relationship("Attendance", back_populates="records")
    student = relationship("Student")
