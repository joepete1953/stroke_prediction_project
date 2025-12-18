# FastAPI app for stroke prediction + Render PostgreSQL connectivity

import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from stroke_pipeline import predict_stroke

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


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


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "stroke prediction api is running"}


@app.post("/predict")
def predict(features: StrokeFeatures):
    data = features.dict()
    result = predict_stroke(data)
    return result


@app.get("/db-count")
def get_row_count():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM stroke_data")
    count = cur.fetchone()[0]
    conn.close()
    return {"rows_in_database": count}
