from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin, coordinator, teacher
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=True)

    college = relationship("College", back_populates="users")
    classes = relationship("Class", back_populates="teacher")
