# AI Tutor — Project Results

## Students
| ID | Name | Points |
|---|---|---|
| 1 | Test User | 0 |
| 2–4 | QA Testers | 30 each |
| 5 | richa | **440** |

## Quiz Attempts (19 total)
| Subject | Attempts | Avg Score | Difficulty |
|---|---|---|---|
| Mathematics | 10 | 92.2% | Medium |
| Science | 6 | 100.0% | Easy/Medium |
| History | 1 | 100.0% | Easy |

## ML Model Output
**Model:** RandomForestClassifier · 100 trees · 4 features · Classes: High / Medium / Low

| Score | Subject | → Level |
|---|---|---|
| 95% | Mathematics | **High** |
| 72% | Science | **Medium** |
| 45% | History | **Medium** |
| 20% | English | **Low** |
| 100% | Geography | **High** |

## Database
- **Questions:** 50 (10 per subject: Maths, Science, History, Geography, English)
- **Achievements:** 2 unlocked ("Perfect Score")
- **Study Plans:** 2 generated (Python 7-day, DSA 2-week)
- **Chat Messages:** 8 stored

## API Endpoints — Live Status
| Route | Status |
|---|---|
| `/login`, `/register` | ✅ Working |
| `/quiz/questions`, `/quiz/submit` | ✅ Working |
| `/chat_api/ask`, `/cheat-sheet` | ✅ Working |
| `/study_api/generate` | ✅ Working |
| `/hf/sentiment`, `/hf/classify-topic` | ✅ Working |
| `/progress`, `/analytics` | ✅ Working |
