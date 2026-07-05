from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from ml_engine import ml_engine
from pydantic import BaseModel
import json
from ai_utils import get_gemini_model

router = APIRouter()

class QuizSubmission(BaseModel):
    student_id: int
    subject: str
    score: float
    time_taken: int  # seconds
    difficulty: str

@router.get("/questions")
async def get_questions(subject: str, difficulty: str = "Easy", ai: bool = False, count: int = 5, db: Session = Depends(get_db)):
    if ai:
        model = get_gemini_model()
        if model:
            try:
                prompt = (
                    f"Generate {count} multiple-choice questions for the subject '{subject}' "
                    f"with difficulty '{difficulty}'. "
                    "Return only a JSON array of objects. Each object must have: "
                    "'text' (string), 'options' (array of 4 strings), and 'correct' (integer index of correct option, 0-3). "
                    "Do not include any other text or markdown formatting."
                )
                response = model.generate_content(prompt)
                
                # Strip markdown code blocks if present
                content = response.text.strip()
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                
                ai_questions = json.loads(content)
                
                # Format to match expectations
                formatted_questions = []
                for i, q in enumerate(ai_questions):
                    formatted_questions.append({
                        "id": f"ai-{i}",
                        "text": q["text"],
                        "options": q["options"],
                        "correct": q["correct"]
                    })
                return formatted_questions[:count] # Ensure exact count
            except Exception as e:
                print(f"Gemini Quiz Error: {e}")
                # Fallback to database if AI fails
    
    questions = db.query(models.Question).filter(
        models.Question.subject == subject,
        models.Question.difficulty == difficulty
    ).limit(count).all()
    
    if not questions:
        # Fallback to any difficulty if specific one not found
        questions = db.query(models.Question).filter(models.Question.subject == subject).limit(count).all()
    
    return [
        {
            "id": q.id,
            "text": q.text,
            "options": q.options if isinstance(q.options, list) else json.loads(q.options),
            "correct": q.correct_option
        } for q in questions
    ]

@router.post("/submit")
async def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    # 1. Store result in database
    student = db.query(models.Student).filter(models.Student.id == submission.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    attempt_count = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.student_id == submission.student_id
    ).count() + 1

    new_attempt = models.QuizAttempt(
        student_id=submission.student_id,
        subject=submission.subject,
        score=submission.score,
        time_taken=submission.time_taken,
        difficulty=submission.difficulty,
        attempt_number=attempt_count
    )
    db.add(new_attempt)
    
    # 2. Predict performance level using ML model
    performance_level = ml_engine.predict_performance(
        submission.score, submission.time_taken, submission.subject, attempt_count
    )

    # 3. Determine next difficulty
    next_difficulty = "Medium"
    if performance_level in ["Beginner", "Intermediate"]: next_difficulty = "Easy"
    elif performance_level == "Advanced": next_difficulty = "Medium"
    elif performance_level in ["Expert", "Master"]: next_difficulty = "Hard"

    # 4. Generate recommendation & Award achievements
    recommendation = "Great job! Keep practicing to reach the next level."
    achievements_earned = []
    
    if submission.score == 100:
        achievements_earned.append({"title": "Perfect Score", "description": f"Achieved a perfect score in {submission.subject}!", "icon": "🏆"})
    if performance_level == "Master":
        achievements_earned.append({"title": "Mastery", "description": f"Reached Master level in {submission.subject}!", "icon": "🌌"})
    elif performance_level == "Expert":
        achievements_earned.append({"title": "Subject Expert", "description": f"Reached Expert level in {submission.subject}!", "icon": "🎓"})
    
    for ach in achievements_earned:
        # Check if already earned
        existing = db.query(models.Achievement).filter(
            models.Achievement.student_id == student.id,
            models.Achievement.title == ach["title"]
        ).first()
        if not existing:
            new_ach = models.Achievement(
                student_id=student.id,
                title=ach["title"],
                description=ach["description"],
                icon=ach["icon"]
            )
            db.add(new_ach)

    # 5. Award points based on performance level
    lvl_points = {"Beginner": 10, "Intermediate": 20, "Advanced": 40, "Expert": 70, "Master": 100}
    points = lvl_points.get(performance_level, 10)
    if submission.score > 90: points += 20
    
    student.total_points += points
    db.commit()

    return {
        "score": submission.score,
        "performance_level": performance_level,
        "next_difficulty": next_difficulty,
        "recommendation": recommendation,
        "points_earned": points,
        "total_points": student.total_points,
        "achievements": achievements_earned
    }
