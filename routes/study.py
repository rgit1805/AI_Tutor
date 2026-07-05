from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from ai_utils import get_gemini_model

router = APIRouter()

class StudyPlanRequest(BaseModel):
    student_id: int
    topic: str
    timeframe: str

@router.post("/generate")
async def generate_study_plan(req: StudyPlanRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == req.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    model = get_gemini_model()
    if not model:
        raise HTTPException(status_code=503, detail="Gemini API is not configured.")

    try:
        prompt = (
            f"You are an AI Tutor creating a personalized study plan for a student.\n"
            f"Topic: {req.topic}\n"
            f"Timeframe: {req.timeframe}\n"
            f"Please generate a detailed, structured study schedule in Markdown format. "
            f"Include daily or weekly goals, recommended topics to cover, and practice suggestions."
        )
        response = model.generate_content(prompt)
        plan_markdown = response.text

        new_plan = models.StudyPlan(
            student_id=req.student_id,
            topic=req.topic,
            timeframe=req.timeframe,
            plan_content=plan_markdown
        )
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        return {"id": new_plan.id, "plan_content": new_plan.plan_content}

    except Exception as e:
        print(f"Gemini Study Plan Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate study plan.")

@router.get("/history/{student_id}")
async def get_study_plans(student_id: int, db: Session = Depends(get_db)):
    plans = db.query(models.StudyPlan).filter(models.StudyPlan.student_id == student_id).all()
    return [{"id": p.id, "topic": p.topic, "timeframe": p.timeframe, "plan_content": p.plan_content} for p in plans]
