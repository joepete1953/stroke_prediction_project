from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from stroke_pipeline import predict_stroke


# ===============================
# DATABASE CONNECTION
# ===============================
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    if DATABASE_URL is None:
        raise Exception("DATABASE_URL not found in environment")
    
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


# ===============================
# FASTAPI APP
# ===============================
app = FastAPI(
    title="Stroke Prediction API",
    version="1.0",
    description="Predict stroke & connect to Render PostgreSQL database"
)


# ===============================
# Request Body Model
# ===============================
class StrokeFeatures(BaseModel):
    gender: str
    age: float
    hypertension: int
    heart_disease: int
    ever_married: str
    Residence_type: str
    work_type: str
    smoking_status: str
    avg_glucose_level: float
    bmi: float


# ===============================
# ROUTES
# ===============================

@app.get("/")
def read_root():
    return {"message": "stroke prediction api is running"}


# ---- PREDICTION ENDPOINT ----
@app.post("/predict")
def predict(features: StrokeFeatures):
    data = features.dict()
    result = predict_stroke(data)
    return {"prediction": result}


# ---- CHECK DB ROW COUNT ----
@app.get("/db-count")
def get_row_count():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM stroke_data")
        count = cur.fetchone()["count"]
        conn.close()

        return {"rows_in_database": count}

    except Exception as e:
        return {"error": str(e)}
