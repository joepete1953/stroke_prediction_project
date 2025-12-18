# streamlit ui for stroke risk prediction
import streamlit as st
import requests
import json
from pathlib import Path

API_URL = "http://localhost:8000/predict"

schema_path = Path(__file__).resolve().parent.parent / "data" / "data_schema.json"
with open(schema_path, "r") as f:
    schema = json.load(f)

cat = schema["categorical_cols"]

st.title("Stroke Risk Prediction")

gender = st.selectbox("Gender", cat.get("gender", []))
age = st.number_input("Age", min_value=0.0, max_value=120.0, value=50.0)
hypertension = st.selectbox("Hypertension (0=No, 1=Yes)", [0, 1])
heart_disease = st.selectbox("Heart Disease (0=No, 1=Yes)", [0, 1])
ever_married = st.selectbox("Ever Married", cat.get("ever_married", []))
Residence_type = st.selectbox("Residence Type", cat.get("Residence_type", []))
work_type = st.selectbox("Work Type", cat.get("work_type", []))
smoking_status = st.selectbox("Smoking Status", cat.get("smoking_status", []))
avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=100.0)
bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)

if st.button("Predict Stroke Risk"):
    payload = {
        "gender": gender,
        "age": age,
        "hypertension": int(hypertension),
        "heart_disease": int(heart_disease),
        "ever_married": ever_married,
        "Residence_type": Residence_type,
        "work_type": work_type,
        "smoking_status": smoking_status,
        "avg_glucose_level": avg_glucose_level,
        "bmi": bmi
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: {result['label']}")
            st.info(f"Probability: {result['probability']:.3f}")
        else:
            st.error("API returned an error")
    except Exception as e:
        st.error(f"Could not reach API: {e}")
