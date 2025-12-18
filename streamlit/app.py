import streamlit as st
import requests

# ============================
# CONFIG & GLOBAL UI SETTINGS
# ============================
st.set_page_config(
    page_title="Stroke Risk Predictor",
    page_icon="🧠",
    layout="centered",
)

# ---------------------------
# CUSTOM CSS for Premium UI
# ---------------------------
st.markdown("""
<style>

body {
    background-color:#0E1117;
}

.big-title {
    font-size:40px !important;
    font-weight:800 !important;
    color:white !important;
}

.sub-text {
    font-size:18px;
    opacity:0.7;
}

.card {
  padding: 25px;
  border-radius: 14px;
  background: linear-gradient(145deg, #111827, #020617);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 0 30px #00000050;
}

.pred-card-safe {
  padding: 25px;
  border-radius: 14px;
  background: linear-gradient(145deg,#092e1b,#05210f);
  border: 1px solid rgba(0,255,0,0.3);
}

.pred-card-risk {
  padding: 25px;
  border-radius: 14px;
  background: linear-gradient(145deg,#381111,#1e0202);
  border: 1px solid rgba(255,0,0,0.4);
}

.number-box label {
    font-size:16px !important;
    font-weight:500 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================
# HEADER
# ============================
st.markdown("<p class='big-title'>🧠 Stroke Risk Prediction System</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>AI-powered health prediction system to assess stroke risk based on patient medical factors.</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================
# API URL
# ============================
API_URL = "https://stroke-prediction-project-8p02.onrender.com/predict"

cat = {
    "gender": ["Male", "Female", "Other"],
    "ever_married": ["Yes", "No"],
    "Residence_type": ["Urban", "Rural"],
    "work_type": ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
    "smoking_status": ["formerly smoked", "never smoked", "smokes", "Unknown"]
}

# ============================
# FORM UI
# ============================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📋 Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("👤 Gender", cat["gender"])
        age = st.slider("🎂 Age", 1, 100, 50)
        hypertension = st.selectbox("❤️ Hypertension", [0, 1])
        heart_disease = st.selectbox("💔 Heart Disease", [0, 1])

    with col2:
        ever_married = st.selectbox("💍 Ever Married?", cat["ever_married"])
        Residence_type = st.selectbox("🏠 Residence Type", cat["Residence_type"])
        work_type = st.selectbox("💼 Work Type", cat["work_type"])
        smoking_status = st.selectbox("🚬 Smoking Status", cat["smoking_status"])

    avg_glucose_level = st.slider("🩸 Average Glucose Level", 50.0, 300.0, 100.0)
    bmi = st.slider("⚖️ BMI", 10.0, 60.0, 25.0)

    st.markdown("</div>", unsafe_allow_html=True)


# ============================
# PREDICT BUTTON
# ============================
if st.button("🔮 Predict Stroke Risk", use_container_width=True):

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

    with st.spinner("Analyzing patient data with AI... ⏳"):
        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                pred = result["prediction"]["prediction"]
                prob = result["prediction"]["probability"]
                label = result["prediction"]["label"]

                st.markdown("<br>", unsafe_allow_html=True)

                if pred == 1:
                    st.markdown("<div class='pred-card-risk'>", unsafe_allow_html=True)
                    st.markdown("## ⚠️ HIGH Stroke Risk Detected")
                    st.markdown(f"### Probability: **{prob:.3f}**")
                    st.markdown(f"### Model Verdict: **{label}**")
                    st.markdown("</div>", unsafe_allow_html=True)

                else:
                    st.markdown("<div class='pred-card-safe'>", unsafe_allow_html=True)
                    st.markdown("## ✅ Low Stroke Risk")
                    st.markdown(f"### Probability: **{prob:.3f}**")
                    st.markdown(f"### Model Verdict: **{label}**")
                    st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.error("❌ API Error. Please check FastAPI logs.")

        except Exception as e:
            st.error(f"❌ Cannot connect to API: {e}")

# ============================
# FOOTER
# ============================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("© Stroke Risk AI System | Built with ❤️ using FastAPI & Streamlit")
