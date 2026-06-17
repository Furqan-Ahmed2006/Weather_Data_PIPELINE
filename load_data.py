import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def load_data_to_db():
    print("Connecting to Cloud Database...")
    
    df = pd.read_csv("clean_weather.csv")
    
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_history (
            timestamp VARCHAR(50) PRIMARY KEY,
            temperature FLOAT,
            humidity FLOAT,
            wind_speed FLOAT,
            target_temperature FLOAT
        )
    """)
    
    print("Loading data into weather_history table...")
    query = """
        INSERT INTO weather_history (timestamp, temperature, humidity, wind_speed, target_temperature)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            temperature = VALUES(temperature),
            humidity = VALUES(humidity),
            wind_speed = VALUES(wind_speed),
            target_temperature = VALUES(target_temperature)
    """
    
    for _, row in df.iterrows():
        cursor.execute(query, (
            str(row['timestamp']),
            float(row['temperature']),
            float(row['humidity']),
            float(row['wind_speed']),
            float(row['target_temperature'])
        ))
        
    conn.commit()
    cursor.close()
    conn.close()
    print("Data successfully loaded into Aiven Cloud Database!")

if __name__ == "__main__":
    load_data_to_db()