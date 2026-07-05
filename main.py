from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routes import auth, quiz, analytics, hf, study, chat
from pydantic import BaseModel
import os
from ai_utils import get_gemini_model

# Get shared Gemini model
model = get_gemini_model()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Powered Personalized Tutor")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(hf.router, prefix="/hf", tags=["HuggingFace"])
app.include_router(study.router, prefix="/study_api", tags=["Study Plan"])
app.include_router(chat.router, prefix="/chat_api", tags=["Chat"])

from hf_utils import analyze_sentiment, classify_topic

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/quiz")
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/progress")
async def progress_page(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})

@app.get("/study")
async def study_page(request: Request):
    return templates.TemplateResponse("study_plan.html", {"request": request})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
