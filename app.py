from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Load ML models
model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
app = FastAPI(
    title="AI-Driven Citizen Grievance & Sentiment Analysis System",
    description="AI system to classify grievances, detect sentiment, and assign priority score"
)

# Input schema
class Complaint(BaseModel):
    text: str


# ----------------------------
# Department routing (FIXED LOGIC)
# ----------------------------
def get_department(text):

    text = text.lower()

    if any(word in text for word in ["water", "leak", "flood", "sewer"]):
        return "Water Department"

    elif any(word in text for word in ["garbage", "trash", "waste"]):
        return "Sanitation"

    elif any(word in text for word in ["noise", "loud", "music", "party"]):
        return "Police"

    elif any(word in text for word in ["parking", "illegal parking"]):
        return "Traffic"

    elif any(word in text for word in ["blocked", "driveway", "obstruction"]):
        return "Transport"

    elif any(word in text for word in ["street", "road", "pothole"]):
        return "Road Maintenance"

    else:
        return "General"


# Priority mapping
priority_map = {
    "Positive": 1,
    "Neutral": 2,
    "Negative": 3,
    "Critical": 5
}


# Home route
@app.get("/")
def home():
    return {"message": "AI Grievance System API Running"}


# Prediction route
@app.post("/predict")
def predict(data: Complaint):

    # Clean + vectorize input
    text = data.text.lower()
    X = vectorizer.transform([text])

    # Sentiment prediction (ML model)
    sentiment = model.predict(X)[0]

    # Priority score
    priority_score = priority_map.get(sentiment, 2)

    # Department (RULE-BASED FIX for accuracy)
    department = get_department(text)

    return {
        "complaint": data.text,
        "department": department,
        "sentiment": sentiment,
        "priority_score": priority_score
    }