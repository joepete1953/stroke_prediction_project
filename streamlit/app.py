import streamlit as st
import requests

# ---------------------------
# 1️⃣ USE YOUR LIVE FASTAPI URL
# ---------------------------
API_URL = "https://stroke-prediction-project-8p02.onrender.com/predict"

# ---------------------------
# 2️⃣ STATIC CATEGORY OPTIONS
# ---------------------------
cat = {
    "gender": ["Male", "Female", "Other"],
    "ever_married": ["Yes", "No"],
    "Residence_type": ["Urban", "Rural"],
    "work_type": ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
    "smoking_status": ["formerly smoked", "never smoked", "smokes", "Unknown"]
}

# ---------------------------
# 3️⃣ STREAMLIT UI
# ---------------------------
st.title("🧠 Stroke Risk Prediction App")

st.write("Enter patient details to predict stroke risk")

gender = st.selectbox("Gender", cat["gender"])
age = st.number_input("Age", min_value=0.0, max_value=120.0, value=50.0)
hypertension = st.selectbox("Hypertension (0=No, 1=Yes)", [0, 1])
heart_disease = st.selectbox("Heart Disease (0=No, 1=Yes)", [0, 1])
ever_married = st.selectbox("Ever Married", cat["ever_married"])
Residence_type = st.selectbox("Residence Type", cat["Residence_type"])
work_type = st.selectbox("Work Type", cat["work_type"])
smoking_status = st.selectbox("Smoking Status", cat["smoking_status"])
avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=100.0)
bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)

# ---------------------------
# 4️⃣ SEND TO API
# ---------------------------
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

            prediction = result.get("prediction", 0)
            probability = result.get("probability", 0)
            label = result.get("label", "Unknown")

            if prediction == 1:
                st.error(f"⚠️ High Stroke Risk Detected")
            else:
                st.success("✅ Low Stroke Risk")

            st.info(f"🧮 Probability: **{probability:.3f}**")
            st.write(f"Model Label: **{label}**")

        else:
            st.error("❌ API returned an error. Check FastAPI logs.")

    except Exception as e:
        st.error(f"❌ Could not reach API: {e}")
