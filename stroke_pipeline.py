# pipeline utilities for stroke prediction using the trained model
from pathlib import Path
from typing import Dict, Any

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "models" / "logreg_no_pca_with_optuna.pkl"

_EXPECTED_COLUMNS = [
    "gender",
    "age",
    "hypertension",
    "heart_disease",
    "ever_married",
    "Residence_type",
    "work_type",
    "smoking_status",
    "avg_glucose_level",
    "bmi",
]

_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def _prepare_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame([data])
    for col in _EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[_EXPECTED_COLUMNS]
    return df


def predict_stroke(data: Dict[str, Any]) -> Dict[str, Any]:
    model = get_model()
    df = _prepare_dataframe(data)
    proba = model.predict_proba(df)[0][1]
    pred = int(proba >= 0.5)
    label = "Stroke" if pred == 1 else "No Stroke"
    return {
        "prediction": pred,
        "probability": float(proba),
        "label": label,
    }
