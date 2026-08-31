from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from security import hash_password, verify_password

router = APIRouter()

class UserRegister(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username_or_email: str
    password: str

@router.post("/register")
async def register(auth: UserRegister, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(
        (models.Student.username == auth.username) | (models.Student.email == auth.email)
    ).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    new_student = models.Student(
        name=auth.name,
        username=auth.username,
        email=auth.email,
        password=hash_password(auth.password)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Registration successful", "student_id": new_student.id, "name": new_student.name}

@router.post("/login")
async def login(auth: UserLogin, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(
        (models.Student.username == auth.username_or_email) | (models.Student.email == auth.username_or_email)
    ).first()
    
    if not db_student or not verify_password(
    auth.password,
    db_student.password
):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "student_id": db_student.id, "name": db_student.name}
