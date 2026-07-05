# 🎓 AI Tutor — Personalized Learning Platform

An intelligent, adaptive tutoring web application powered by **FastAPI**, **Google Gemini AI**, and a **scikit-learn ML engine**. It delivers personalized quiz experiences, real-time AI doubt solving, gamified progress tracking, and dynamic difficulty adjustment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Doubt Solver** | Chat with Google Gemini AI with persistent context |
| 📝 **Adaptive Quizzes** | AI or DB questions with adjustable difficulty and count |
| 📚 **Study Planner** | Auto-generate personalized study schedules |
| 🧾 **Cheat Sheet** | Generate study guides summarizing your learning sessions |
| 🤗 **HuggingFace NLP** | Sentiment analysis, topic classification, and gap analysis |
| 📊 **Progress Tracker** | View scores, achievements, best subjects, and history |
| 🏆 **Gamification** | Points system, performance levels, and unlockable achievements |
| 🧠 **ML Engine** | Random Forest classifier predicts student performance level |
| 🎨 **Modern UI** | Glassmorphism design with smooth animations and dark theme |

---

## 🏗️ Project Structure

```
AI_TUTOR/
├── main.py               # FastAPI app entry point, routes
├── models.py             # SQLAlchemy ORM models (Student, Quiz, etc.)
├── database.py           # SQLite DB setup and session factory
├── ml_engine.py          # Random Forest ML model for performance prediction
├── ai_utils.py           # Google Gemini API client initialisation
├── hf_utils.py           # HuggingFace Inference API integrations
├── seeds.py              # Seed script to populate initial quiz questions
│
├── routes/
│   ├── auth.py           # Register & login endpoints
│   ├── quiz.py           # Quiz questions, submission, and scoring
│   ├── analytics.py      # Progress, achievements, and analytics endpoints
│   ├── chat.py           # Persistent chat & cheat sheet generator
│   ├── study.py          # Study plan generator endpoints
│   └── hf.py             # HuggingFace model endpoints
│
├── templates/            # Jinja2 HTML templates (server-side rendered)
│   ├── index.html        # Dashboard
│   ├── chat.html         # AI Chat page
│   ├── quiz.html         # Interactive quiz
│   ├── progress.html     # Student progress & analytics
│   ├── study_plan.html   # Study plan generator
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── css/style.css     # Global styles (glassmorphism, animations)
│   └── js/app.js         # Frontend logic (chat, quiz, auth, markdown renderer)
│
├── ml_model.joblib       # Trained ML model (auto-generated on first run)
├── label_encoder.joblib  # Subject label encoder
├── ai_tutor.db           # SQLite database (auto-created)
├── requirements.txt
└── .env                  # Environment variables (not committed)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd AI_TUTOR
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file and add your Gemini API key:

```bash
copy .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_KEY=your_huggingface_api_key_here
```

> Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey)
> Get a free HuggingFace token at [HuggingFace Settings](https://huggingface.co/settings/tokens)

### 5. (Optional) Seed the Database

Populate initial quiz questions:

```bash
python seeds.py
```

### 6. Run the Application

```bash
uvicorn main:app --reload
```

Open your browser at **[http://localhost:8000](http://localhost:8000)**

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/register` | Create a new student account |
| `POST` | `/login` | Log in, returns student data |

### Quiz
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/quiz/questions` | Fetch questions (`subject`, `difficulty`, `ai`, `count`) |
| `POST` | `/quiz/submit` | Submit quiz results, get performance & next difficulty |

### AI Chat (`/chat_api`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/history/{student_id}` | Fetch previous chat messages |
| `POST` | `/ask` | Send a message for AI tutoring |
| `GET` | `/cheat-sheet/{student_id}` | Generate cheat sheet from chat history |

### Study Plan (`/study_api`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/generate` | Generate personalized study plan |
| `GET` | `/history/{student_id}` | Get recent study plans |

### HuggingFace NLP (`/hf`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/generate-questions` | Generate questions using HF models |
| `POST` | `/sentiment` | Analyze sentiment of student input |
| `POST` | `/classify-topic` | Classify educational topic |
| `GET` | `/knowledge-gaps/{student_id}`| Identify student knowledge gaps |
| `POST` | `/validate-answer` | Validate student answers |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/progress/{student_id}` | Points, score average, attempts, achievements |
| `GET` | `/analytics/{student_id}` | Best/weak subjects and performance breakdown |

### Pages
| Route | Description |
|---|---|
| `/` | Dashboard |
| `/chat` | AI Doubt Solver |
| `/quiz` | Quiz (params: `subject`, `ai`, `count`) |
| `/progress` | Progress & Achievements |
| `/study` | Study Plan Generator |
| `/login` | Login page |
| `/register` | Registration page |

---

## 🧠 ML Engine

The `MLEngine` class in `ml_engine.py` uses a **Random Forest Classifier** trained on synthetic student data to predict performance levels:

| Level | Score Range |
|---|---|
| Beginner | < 40% |
| Intermediate | 40 – 59% |
| Advanced | 60 – 79% |
| Expert | 80 – 94% |
| Master | 95 – 100% |

The model trains automatically on first run and is cached to `ml_model.joblib`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Database | SQLite + SQLAlchemy |
| Templating | Jinja2 |
| AI (LLM) | Google Gemini (`google-generativeai`) |
| AI (NLP) | Hugging Face Inference API |
| ML | scikit-learn (Random Forest), joblib |
| Frontend | Vanilla HTML, CSS (Glassmorphism), JavaScript |

---

## 📦 Requirements

```
fastapi
uvicorn
sqlalchemy
pandas
numpy
scikit-learn
joblib
jinja2
python-multipart
google-generativeai
python-dotenv
```

---

## 📄 License

This project is for educational purposes. Feel free to use and modify.
