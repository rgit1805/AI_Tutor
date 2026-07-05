from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

router = APIRouter()

@router.get("/progress/{student_id}")
async def get_progress(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    avg_score = db.query(func.avg(models.QuizAttempt.score)).filter(
        models.QuizAttempt.student_id == student_id
    ).scalar() or 0
    
    achievements = db.query(models.Achievement).filter(
        models.Achievement.student_id == student_id
    ).all()
    
    return {
        "name": student.name,
        "total_points": student.total_points,
        "average_score": round(avg_score, 2),
        "attempts_count": db.query(models.QuizAttempt).filter(models.QuizAttempt.student_id == student_id).count(),
        "achievements": [
            {"title": a.title, "description": a.description, "icon": a.icon} for a in achievements
        ]
    }

@router.get("/analytics/{student_id}")
async def get_analytics(student_id: int, db: Session = Depends(get_db)):
    # Best subject
    best_sub = db.query(
        models.QuizAttempt.subject,
        func.avg(models.QuizAttempt.score).label('avg_score')
    ).filter(models.QuizAttempt.student_id == student_id).group_by(models.QuizAttempt.subject).order_by(func.avg(models.QuizAttempt.score).desc()).first()

    # Recent scores for trend (last 10 attempts with attempt number)
    recent = db.query(
        models.QuizAttempt.score,
        models.QuizAttempt.subject,
        models.QuizAttempt.difficulty
    ).filter(
        models.QuizAttempt.student_id == student_id
    ).order_by(models.QuizAttempt.id.desc()).limit(10).all()

    # Subject performance for radar chart
    subject_rows = db.query(
        models.QuizAttempt.subject,
        func.avg(models.QuizAttempt.score).label('avg_score'),
        func.count(models.QuizAttempt.id).label('attempts')
    ).filter(
        models.QuizAttempt.student_id == student_id
    ).group_by(models.QuizAttempt.subject).all()

    return {
        "best_subject": best_sub[0] if best_sub else "N/A",
        "recent_scores": [
            {"score": r[0], "subject": r[1], "difficulty": r[2]}
            for r in reversed(recent)
        ],
        "subject_performance": [
            {"subject": r[0], "avg_score": round(r[1], 1), "attempts": r[2]}
            for r in subject_rows
        ]
    }
