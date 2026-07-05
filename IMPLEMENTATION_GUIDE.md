# Step-by-Step Implementation Guide

This document outlines the step-by-step process for setting up, configuring, and running the AI Powered Personalized Tutor from scratch. It is intended for developers who want to replicate or contribute to the project.

---

## Phase 1: Environment Setup

### 1. Prerequisites
Ensure your system has the following installed:
*   **Python 3.9+**: The core language for the backend and ML engine.
*   **Git**: For version control and cloning the repository.

### 2. Clone the Repository
Open your terminal or command prompt and clone the project directory:
```bash
git clone <repository_url>
cd AI_TUTOR
```

### 3. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies and avoid conflicts:
```bash
# Create the virtual environment named 'venv'
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS / Linux:
source venv/bin/activate
```

### 4. Install Dependencies
Install all the required Python packages (FastAPI, SQLAlchemy, scikit-learn, google-generativeai, etc.):
```bash
pip install -r requirements.txt
```

---

## Phase 2: API Keys and Configuration

The application relies on external APIs for LLM and NLP functionalities. You need to configure these securely.

### 1. Set Up the `.env` File
Copy the example environment file to create your local `.env` file:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

### 2. Procure External API Keys
*   **Google Gemini API Key**: 
    1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    2. Sign in and create a new API key.
*   **Hugging Face Inference API Token**:
    1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens).
    2. Create a new token (Read access is sufficient for inference).

### 3. Update the `.env` File
Open the newly created `.env` file and insert your keys:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
HF_API_KEY=your_actual_huggingface_api_key_here
```

---

## Phase 3: Database Setup and Seeding

The application uses SQLite, meaning no heavy database server installation is required.

### 1. Automatic Schema Creation
You do not need to manually run SQL scripts to create tables. Upon the first launch, SQLAlchemy will automatically detect missing tables and generate `ai_tutor.db` based on the definitions in `models.py`.

### 2. Seed Initial Data (Optional but Recommended)
To populate the database with default subjects and initial fallback questions, run the seeding script:
```bash
python seeds.py
```
*Note: This script will insert sample questions into the `questions` table.*

---

## Phase 4: Machine Learning Engine Initialization

The platform uses a `scikit-learn` Random Forest model to predict performance and scale quiz difficulty.

### 1. Model Auto-Generation
There is no separate training script you *must* run manually. When the backend starts or when a quiz is submitted for the first time, `ml_engine.py` checks for the existence of `ml_model.joblib`. 
If it is missing, the engine automatically generates synthetic educational data, trains the Random Forest model on the fly, and caches it to the disk.

---

## Phase 5: Running the Application

### 1. Start the FastAPI Server
With the virtual environment active and your `.env` file configured, start the Uvicorn ASGI server:
```bash
uvicorn main:app --reload
```
*The `--reload` flag enables auto-reloading upon saving code changes.*

### 2. Access the Local Server
Open your preferred web browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

---

## Phase 6: Basic Usage Workflow

Once the application is running, follow this flow to verify the implementation:
1.  **Register/Login**: Create a new student account via the UI.
2.  **Take a Quiz**: Navigate to the Quiz section. Select a subject and choose whether to generate questions via AI or DB. Complete the quiz and submit it.
3.  **Check Progress**: Go to the Dashboard to see your ML-adjusted performance level and points.
4.  **Chat & Cheat Sheet**: Open the AI Doubt Solver, ask a few concept questions, and then click "Generate Cheat Sheet" to verify the persistent context summary.
5.  **Study Plan**: Generate a 7-day study plan for a desired topic and verify it renders beautifully in markdown.
