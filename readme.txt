The AI Powered Personalized Tutor is an interactive, intelligent web application designed to enhance the learning experience of students. By leveraging advanced Language Models (Google Gemini) and Natural Language Processing (Hugging Face API), alongside a Machine Learning engine (Random Forest), the platform dynamically adapts to a student's learning pace, predicts their performance, and offers context-aware assistance. Key features include adaptive quizzes, sentiment analysis of user inputs, automated study plans, persistent cheat sheets, and gamified progress tracking.

## 2. System Architecture
The application follows a modern client-server architecture:
* **Frontend**: A vanilla HTML, CSS, and JavaScript interface adopting a visually appealing Glassmorphism design and dark theme. It communicates asynchronously with the backend via RESTful APIs.
* **Backend**: Built with **FastAPI**, serving as a robust, high-performance web framework. The backend manages all business logic, routing, authentication, and external API calls.
* **Database**: **SQLite** backed by **SQLAlchemy ORM** to persistently store student profiles, quiz attempts, study plans, chat context, and achievements.
* **AI & NLP Layers**: 
  * *Google Gemini API*: Acts as the core conversational agent, generating adaptive quiz questions, drafting cheat sheets, and creating study plans.
  * *Hugging Face Inference API*: Provides specialized NLP capabilities such as sentiment analysis, precise topic classification, knowledge gap detection, and answer validation.
* **ML Engine**: A `scikit-learn` Random Forest Classifier running server-side to predict user performance metrics and adjust quiz difficulty dynamically.

## 3. Technologies Used
| Layer | Technology | Purpose |
|---|---|---|
| **Backend Framework** | FastAPI + Uvicorn | Routing, API Endpoints, Server |
| **Language** | Python 3.x | Core programming language |
| **Database** | SQLite + SQLAlchemy | Data persistence and ORM modeling |
| **Templating** | Jinja2 | Server-side rendering initial HTML pages |
| **Generative AI** | Google Gemini (`google-generativeai`) | LLM for dynamic content generation and chat |
| **NLP Utilities** | Hugging Face API | Sentiment, Topic mapping, and NLP validation |
| **Machine Learning** | Scikit-Learn, Pandas, Numpy, Joblib | Performance prediction and difficulty scaling |
| **Frontend UI** | HTML5, CSS3, Vanilla JS | Client-side interface, API consumption |

## 4. Database Schema
The database uses the following core entities (tables):
1. **Student (`students`)**: Stores user credentials, total gamification points, and links to their historical data.
2. **QuizAttempt (`quiz_attempts`)**: Logs each quiz session including subject, score, duration, difficulty, and attempt number.
3. **Question (`questions`)**: Repository for standard, static database questions as fallbacks for AI generation.
4. **Achievement (`achievements`)**: Unlockable badges earned based on points or milestones.
5. **StudyPlan (`study_plans`)**: AI-generated structured markdown schedules detailing topics and timeframes.
6. **ChatMessage (`chat_messages`)**: Persistent storage of the student's conversation history with the AI doubt solver.

## 5. Key Modules and Features

### 5.1. Authentication & Profiling
Secure user registration and login ensuring personalized environments. Once authenticated, users access a dashboard portraying their progress, accrued points, and recent activities.

### 5.2. Gamified Progress Tracker
A robust analytics dashboard tracking total points, average scores, and attempting frequencies. Includes an achievements system to motivate learners by unlocking customizable icons/badges.

### 5.3. Adaptive Quizzes with ML Scaling
Quizzes generate either via predefined Database sets, Gemini LLM, or Hugging Face Question generation. Upon submission, a trained local ML classifier analyses the student's success rate and time taken to recommend an optimal difficulty level (Beginner to Master) for future assessments.

### 5.4. Persistent Context AI Chat and Cheat Sheet Generator
The 'AI Doubt Solver' utilizes Google Gemini to provide instant tutoring. Unique to this module, conversations are stored persistently in the database (`ChatMessage`). At any point, a student can click 'Generate Cheat Sheet' to condense their entire chat history into an actionable, summarized markdown document containing formulas, concepts, and summaries.

### 5.5. Study Plan Generator
A dedicated tool accepting a specific topic and timeframe (e.g., "Algebra in 7 days"). The backend queries Gemini to build a structured, daily roadmap, storing the comprehensive HTML-formatted markdown plan to the student's profile history.

### 5.6. Hugging Face NLP Suite
Deep sentiment and context evaluation using state-of-the-art Hugging Face models:
*   **Sentiment Analysis**: Evaluates student messages to detect frustration or confidence.
*   **Topic Classification**: Categorizes user questions into standard subjects.
*   **Knowledge Gap Analysis**: Analyzes historical quiz data and chat to highlight specific weak points.
*   **Answer Validation**: Uses similarity models to check the accuracy of textual answers against known rubrics.

## 6. Machine Learning Engine Details
The `MLEngine` utilizes a **Random Forest Classifier**:
*   **Training Data**: Initially trained on a synthetic dataset representing various student behavior profiles (score, time taken, difficulty).
*   **Feature Engineering**: Subjects are encoded via a `LabelEncoder`. Features fed to the model include integer representation of `subject`, `score` (0-100), and `time_taken` (seconds).
*   **Output Classes**: Predicts one of 5 performance tiers: **Beginner**, **Intermediate**, **Advanced**, **Expert**, **Master**. The model is serialized using `joblib` for rapid inference.

## 7. API Endpoints Overview
The project divides functionalities efficiently across FastAPI routers:
*   `/login`, `/register`: Auth routes.
*   `/quiz/questions`, `/quiz/submit`: Quiz administration and scoring.
*   `/chat_api/ask`, `/chat_api/history`, `/chat_api/cheat-sheet`: Chat persistence and summarizations.
*   `/study_api/generate`, `/study_api/history`: Plan creation.
*   `/hf/generate-questions`, `/hf/sentiment`, `/hf/classify-topic`, `/hf/knowledge-gaps`, `/hf/validate-answer`: Specialized NLP operations.
*   `/progress`, `/analytics`: Metrics retrieval.

## 8. Conclusion and Future Enhancements
The AI Powered Personalized Tutor successfully merges LLM reasoning and localized ML algorithms to create an evolving educational ecosystem. 

**Future Scope:**
*   **Authentication Upgrades**: Integrate OAuth2 (e.g., Sign in with Google) and token-based session management (JWTs).
*   **Rich Media Generation**: Introduce image/diagram generation using text-to-image models for visual learners.
*   **Voice Interface**: Incorporate Whisper or similar Speech-to-Text capability in the Chat interface for conversational tutoring.
*   **Multiplayer / Social**: Leaderboards across students or collaborative quiz environments.
