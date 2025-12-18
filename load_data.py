import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

df = pd.read_csv("data/healthcare-dataset-stroke-data.csv")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO stroke_data 
        (gender, age, hypertension, heart_disease, ever_married, residence_type,
         work_type, smoking_status, avg_glucose_level, bmi, stroke)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        row["gender"],
        row["age"],
        row["hypertension"],
        row["heart_disease"],
        row["ever_married"],
        row["Residence_type"],
        row["work_type"],
        row["smoking_status"],
        row["avg_glucose_level"],
        row["bmi"],
        row["stroke"]
    ))

conn.commit()
cur.close()
conn.close()

print("DATA INSERTED SUCCESSFULLY!")
