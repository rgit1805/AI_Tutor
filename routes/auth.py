from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from security import create_access_token, hash_password, verify_password
from pwdlib.exceptions import UnknownHashError

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
        password=hash_password(auth.password),
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {
        "message": "Registration successful",
        "student_id": new_student.id,
        "name": new_student.name,
    }


@router.post("/login")
async def login(auth: UserLogin, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(
        (models.Student.username == auth.username_or_email) | (models.Student.email == auth.username_or_email)
    ).first()

    if not db_student:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        password_valid = verify_password(auth.password, db_student.password)
    except UnknownHashError:
        password_valid = False

    if not password_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(db_student.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "student_id": db_student.id,
        "name": db_student.name,
    }
