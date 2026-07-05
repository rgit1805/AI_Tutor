"""
routes/hf.py — HuggingFace Inference API endpoints
Prefix: /hf    Tag: HuggingFace
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from database import get_db
import models
from hf_utils import (
    generate_questions_hf,
    analyze_sentiment,
    classify_topic,
    get_knowledge_gaps,
    validate_answer,
)

router = APIRouter()


# ── Pydantic schemas ─────────────────────────────────────────────────────────

class QuestionGenRequest(BaseModel):
    subject: str
    difficulty: str = "Easy"
    count: int = 5

class SentimentRequest(BaseModel):
    text: str

class TopicRequest(BaseModel):
    text: str

class GapRequest(BaseModel):
    student_id: int

class AnswerValidationRequest(BaseModel):
    question: str
    context: str
    answer: str


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/generate-questions")
async def hf_generate_questions(req: QuestionGenRequest):
    """
    Feature 1 — Generate quiz MCQs via T5 question-generation model.
    """
    questions = await generate_questions_hf(req.subject, req.difficulty, req.count)
    if not questions:
        raise HTTPException(status_code=503, detail="HF question generation unavailable. Check HF_API_KEY or try again.")
    return [
        {"id": f"hf-{i}", "text": q["text"], "options": q["options"], "correct": q["correct"]}
        for i, q in enumerate(questions)
    ]


@router.post("/sentiment")
async def hf_sentiment(req: SentimentRequest):
    """
    Feature 2 — Detect student sentiment from chat messages.
    Returns label (POSITIVE / NEUTRAL / NEGATIVE), score, and emoji.
    """
    result = await analyze_sentiment(req.text)
    return result


@router.post("/classify-topic")
async def hf_classify_topic(req: TopicRequest):
    """
    Feature 3 — Zero-shot classify a student's question into a subject.
    """
    result = await classify_topic(req.text)
    return result


@router.get("/knowledge-gaps/{student_id}")
async def hf_knowledge_gaps(student_id: int, db: Session = Depends(get_db)):
    """
    Feature 4 — Use sentence embeddings + quiz history to surface weak subjects.
    """
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Build subject → average score map from quiz attempts
    rows = (
        db.query(
            models.QuizAttempt.subject,
            func.avg(models.QuizAttempt.score).label("avg_score")
        )
        .filter(models.QuizAttempt.student_id == student_id)
        .group_by(models.QuizAttempt.subject)
        .all()
    )

    if not rows:
        return {"weak_areas": [], "gap_details": [], "message": "No quiz attempts yet."}

    subject_scores = {row.subject: float(row.avg_score) for row in rows}
    return await get_knowledge_gaps(subject_scores)


@router.post("/validate-answer")
async def hf_validate_answer(req: AnswerValidationRequest):
    """
    Feature 5 — Validate a student's free-text answer using RoBERTa QA.
    """
    result = await validate_answer(req.question, req.context, req.answer)
    return result
