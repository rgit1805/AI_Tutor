from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String) # In a real app, this should be hashed
    total_points = Column(Integer, default=0)

    attempts = relationship("QuizAttempt", back_populates="student")
    achievements = relationship("Achievement", back_populates="student")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    score = Column(Float)
    time_taken = Column(Integer)  # in seconds
    difficulty = Column(String)    # Easy, Medium, Hard
    attempt_number = Column(Integer)

    student = relationship("Student", back_populates="attempts")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    text = Column(String)
    options = Column(String)  # JSON string of options
    correct_option = Column(Integer)  # Index of correct option
    difficulty = Column(String)  # Easy, Medium, Hard

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    title = Column(String)
    description = Column(String)
    icon = Column(String)

    student = relationship("Student", back_populates="achievements")

# Update Student model to include achievements relationship
# (Already handled by adding the back_populates above, 
# but need to add the relationship property to Student class as well)

class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    topic = Column(String)
    timeframe = Column(String)
    plan_content = Column(String) # Store Markdown string

    student = relationship("Student", back_populates="study_plans")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    role = Column(String) # 'user' or 'ai'
    content = Column(String)
    
    student = relationship("Student", back_populates="chat_messages")

# Need to update Student to have `study_plans = relationship("StudyPlan", back_populates="student")`
Student.study_plans = relationship("StudyPlan", back_populates="student")
Student.chat_messages = relationship("ChatMessage", back_populates="student")
