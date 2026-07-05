import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

MODEL_PATH = "ml_model.joblib"
ENCODER_PATH = "label_encoder.joblib"

class MLEngine:
    def __init__(self):
        self.model = None
        self.encoder = LabelEncoder()
        self.subjects = ["Mathematics", "Science", "History", "Geography", "English"]
        self.encoder.fit(self.subjects)
        
        if os.path.exists(MODEL_PATH):
            self.load_model()
        else:
            self.train_initial_model()

    def train_initial_model(self):
        print("Training initial ML model with synthetic data...")
        # Generate synthetic data
        n_samples = 1000
        data = {
            'previous_score': np.random.randint(0, 101, n_samples),
            'time_taken': np.random.randint(30, 600, n_samples),
            'subject': np.random.choice(self.subjects, n_samples),
            'attempt_number': np.random.randint(1, 10, n_samples)
        }
        df = pd.DataFrame(data)
        
        # Features and Target
        X = df.copy()
        X['subject'] = self.encoder.transform(X['subject'])
        
        # Enhanced rule-based performance for synthetic target
        def define_performance(row):
            score = row['previous_score']
            time = row['time_taken']
            # Better score with less time = higher level
            efficiency = score / (time / 60) if time > 0 else 0
            
            if score < 40: return "Beginner"
            elif score < 60: return "Intermediate"
            elif score < 80: return "Advanced"
            elif score < 95: return "Expert"
            else: return "Master"
            
        y = df.apply(define_performance, axis=1)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Save model and encoder
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.encoder, ENCODER_PATH)
        print("Optimized model trained and saved.")

    def load_model(self):
        try:
            self.model = joblib.load(MODEL_PATH)
            self.encoder = joblib.load(ENCODER_PATH)
            print("Model loaded from disk.")
        except:
            self.train_initial_model()

    def predict_performance(self, previous_score, time_taken, subject, attempt_number):
        if subject not in self.subjects:
            # Fallback for unknown subjects
            if previous_score < 50: return "Beginner"
            return "Intermediate"
            
        subject_encoded = self.encoder.transform([subject])[0]
        features = np.array([[previous_score, time_taken, subject_encoded, attempt_number]])
        prediction = self.model.predict(features)
        return prediction[0]

ml_engine = MLEngine()
