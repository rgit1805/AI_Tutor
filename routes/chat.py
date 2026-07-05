from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import asyncio

import models
from database import get_db
from ai_utils import get_gemini_model
from hf_utils import analyze_sentiment, classify_topic

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    student_id: int
    message: str

@router.get("/history/{student_id}")
async def get_chat_history(student_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.ChatMessage).filter(models.ChatMessage.student_id == student_id).order_by(models.ChatMessage.id.asc()).all()
    return [{"role": m.role, "content": m.content} for m in messages]

@router.post("/ask")
async def ask_bot(req: ChatRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == req.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 1. Save user message
    user_msg = models.ChatMessage(student_id=req.student_id, role="user", content=req.message)
    db.add(user_msg)
    db.commit()

    # Run sentiment + topic classification in parallel
    sentiment_task = asyncio.create_task(analyze_sentiment(req.message))
    topic_task     = asyncio.create_task(classify_topic(req.message))

    # 2. Fetch history for context (last 6 messages = 3 interactions)
    past_messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.student_id == req.student_id
    ).order_by(models.ChatMessage.id.desc()).limit(6).all()
    past_messages.reverse()

    model = get_gemini_model()
    reply = ""

    if model:
        try:
            # Build context
            context_prompt = "Here is the recent conversation history for context:\n"
            for msg in past_messages:
                # exclude current message as it's already there
                if msg.id != user_msg.id:
                    role_name = "Student" if msg.role == "user" else "AI Tutor"
                    context_prompt += f"{role_name}: {msg.content}\n"
            
            prompt = (
                f"You are an AI Tutor. {context_prompt}\n"
                f"The student is now asking: {req.message}. Provide a helpful, educational, and concise response."
            )
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            reply = "I'm having a bit of trouble thinking right now. But don't stop learning! The answer is likely in your textbook."
    else:
        # Static Fallback if no API key
        reply = "I am your AI Tutor. I can help you with Mathematics, Science, and more!"
        if "math" in req.message.lower():
            reply = "Mathematics is the study of numbers, shapes, and patterns. What specific topic are you interested in?"
        elif "science" in req.message.lower():
            reply = "Science is a systematic enterprise that builds and organizes knowledge. Are we talking about Physics, Chemistry, or Biology?"
        reply += " (Note: Connect Gemini API for real-time answers)"

    # 3. Save AI response
    ai_msg = models.ChatMessage(student_id=req.student_id, role="ai", content=reply)
    db.add(ai_msg)
    db.commit()

    sentiment = await sentiment_task
    topic     = await topic_task

    return {"reply": reply, "sentiment": sentiment, "topic": topic}

@router.get("/cheat-sheet/{student_id}")
async def generate_cheat_sheet(student_id: int, request: Request, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    messages = db.query(models.ChatMessage).filter(models.ChatMessage.student_id == student_id).order_by(models.ChatMessage.id.asc()).all()
    
    if not messages:
        return templates.TemplateResponse("cheat_sheet.html", {"request": request, "content": "You haven't asked any questions yet! Chat with your tutor to build a cheat sheet.", "student_name": student.name})

    model = get_gemini_model()
    if not model:
        return templates.TemplateResponse("cheat_sheet.html", {"request": request, "content": "Error: Gemini model not configured.", "student_name": student.name})

    try:
        chat_log = ""
        for m in messages:
            role = "Student" if m.role == "user" else "Tutor"
            chat_log += f"{role}: {m.content}\n"

        prompt = (
            f"You are generating an offline Study Cheat Sheet and Notes guide for a student named {student.name}.\n"
            f"Please deeply analyze the following chat history between the student and their tutor.\n"
            f"Create a beautifully formatted Markdown cheat sheet that extracts all the key concepts, formulas, definitions, and important takeaways from the conversation.\n"
            f"Format it with clear headings, bullet points, and bold text for emphasis. Ignore casual chit-chat.\n\n"
            f"Chat History:\n{chat_log}"
        )
        response = model.generate_content(prompt)
        content = response.text
    except Exception as e:
        print(f"Gemini Cheat Sheet Error: {e}")
        content = "Failed to generate cheat sheet due to an error."

    return templates.TemplateResponse("cheat_sheet.html", {"request": request, "content": content, "student_name": student.name})
