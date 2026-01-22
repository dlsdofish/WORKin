from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    coordinator_id = Column(Integer, ForeignKey("users.id"))

    college = relationship("College", back_populates="students")
    coordinator = relationship("User")
    class_assignments = relationship("ClassStudent", back_populates="student")
