from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    users = relationship("User", back_populates="college")
    students = relationship("Student", back_populates="college")
    classes = relationship("Class", back_populates="college")
