import os
import time
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()


def get_pg_connection(retries=3, delay=3):
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST").strip(),
                port=int(os.getenv("DB_PORT", 5432)),
                dbname=os.getenv("DB_NAME", "postgres").strip(),
                user=os.getenv("DB_USER").strip(),
                password=os.getenv("DB_PASSWORD"),
                sslmode="require",
                connect_timeout=10,
            )
        except Exception as e:
            if attempt == retries:
                raise
            print(f"DB connection retry {attempt}/{retries}: {e}")
            time.sleep(delay)


def load_data_to_db():
    print("Connecting to Supabase PostgreSQL...")
    df = pd.read_csv("clean_weather.csv")

    if df.empty:
        print("clean_weather.csv is empty. Skipping DB load.")
        return

    history_rows = [
        (
            str(row["timestamp"]),
            float(row["temperature"]),
            int(row["humidity"]),
            float(row["wind_speed"]),
            float(row["target_temperature"]),
        )
        for _, row in df.iterrows()
    ]


    latest_df = df.tail(72)
    latest_rows = [
        (
            str(row["timestamp"]),
            float(row["temperature"]),
            int(row["humidity"]),
            float(row["wind_speed"]),
        )
        for _, row in latest_df.iterrows()
    ]

    conn = get_pg_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS weather_history (
                        timestamp TEXT PRIMARY KEY,
                        temperature DOUBLE PRECISION,
                        humidity INTEGER,
                        wind_speed DOUBLE PRECISION,
                        target_temperature DOUBLE PRECISION
                    );
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS df_latest (
                        timestamp TEXT PRIMARY KEY,
                        temperature DOUBLE PRECISION,
                        humidity INTEGER,
                        wind_speed DOUBLE PRECISION
                    );
                """)

                execute_values(
                    cur,
                    """
                    INSERT INTO weather_history (
                        timestamp, temperature, humidity, wind_speed, target_temperature
                    )
                    VALUES %s
                    ON CONFLICT (timestamp) DO UPDATE SET
                        temperature = EXCLUDED.temperature,
                        humidity = EXCLUDED.humidity,
                        wind_speed = EXCLUDED.wind_speed,
                        target_temperature = EXCLUDED.target_temperature;
                    """,
                    history_rows,
                )

            
                cur.execute("TRUNCATE TABLE df_latest;")
                execute_values(
                    cur,
                    """
                    INSERT INTO df_latest (timestamp, temperature, humidity, wind_speed)
                    VALUES %s
                    ON CONFLICT (timestamp) DO UPDATE SET
                        temperature = EXCLUDED.temperature,
                        humidity = EXCLUDED.humidity,
                        wind_speed = EXCLUDED.wind_speed;
                    """,
                    latest_rows,
                )

        print("Data successfully loaded into Supabase PostgreSQL!")
    finally:
        conn.close()


if __name__ == "__main__":
    load_data_to_db()