# fastapi app that uses the stroke pipeline for prediction
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from stroke_pipeline import predict_stroke

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
