import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Total rows check karne ke liye
query = "SELECT COUNT(*) as Total_Rows FROM weather_history"
df = pd.read_sql(query, conn)
print("📊 Database Status:")
print(df)

print("\n📋 Aakhri 5 Rows:")
query_latest = "SELECT * FROM weather_history ORDER BY timestamp DESC LIMIT 5"
df_latest = pd.read_sql(query_latest, conn)
print(df_latest)

conn.close()