from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.college import College
from app.models.user import User
from app.schemas.college import CollegeCreate, CollegeOut
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.dependencies import get_current_user, admin_only

router = APIRouter(prefix="/admin", tags=["admin"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1️⃣ Add a College
@router.post("/colleges", response_model=CollegeOut)
def add_college(college: CollegeCreate, db: Session = Depends(get_db), user=Depends(admin_only)):
    existing = db.query(College).filter(College.name == college.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="College already exists")
    
    new_college = College(name=college.name)
    db.add(new_college)
    db.commit()
    db.refresh(new_college)
    return new_college

# 2️⃣ Add a Coordinator or Teacher
@router.post("/users")
def add_user(new_user: UserCreate, db: Session = Depends(get_db), user=Depends(admin_only)):
    if new_user.role not in ["coordinator", "teacher"]:
        raise HTTPException(status_code=400, detail="Role must be coordinator or teacher")
    
    existing = db.query(User).filter(User.email == new_user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_obj = User(
        name=new_user.name,
        email=new_user.email,
        password_hash=hash_password(new_user.password),
        role=new_user.role,
        college_id=new_user.college_id
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"message": f"{new_user.role.capitalize()} added successfully", "id": user_obj.id}

# 3️⃣ View All Students
@router.get("/students")
def view_all_students(db: Session = Depends(get_db), user=Depends(admin_only)):
    students = db.query(User).filter(User.role=="student").all()  # optional if you track students as User
    return students
