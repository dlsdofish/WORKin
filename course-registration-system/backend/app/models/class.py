from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))

    college = relationship("College", back_populates="classes")
    teacher = relationship("User", back_populates="classes")
    students = relationship("ClassStudent", back_populates="class_")
    attendance = relationship("Attendance", back_populates="class_")
