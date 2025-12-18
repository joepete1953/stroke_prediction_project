import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS stroke_data (
    id SERIAL PRIMARY KEY,
    gender VARCHAR(20),
    age FLOAT,
    hypertension INT,
    heart_disease INT,
    ever_married VARCHAR(10),
    residence_type VARCHAR(20),
    work_type VARCHAR(30),
    smoking_status VARCHAR(30),
    avg_glucose_level FLOAT,
    bmi FLOAT,
    stroke INT
)
""")

conn.commit()
cur.close()
conn.close()

print("Table Created Successfully")
