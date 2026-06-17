import json
import pandas as pd

def transform_data():
    print("Transforming raw JSON data...")
    
    with open("raw_weather.json", "r") as f:
        raw_data = json.load(f)
    hourly_data = raw_data["hourly"]
    df = pd.DataFrame(hourly_data)
    df.rename(columns={
        "time": "timestamp",
        "temperature_2m": "temperature",
        "relative_humidity_2m": "humidity",
        "wind_speed_10m": "wind_speed"
    }, inplace=True)
    df["target_temperature"] = df["temperature"].shift(-24)
    df.dropna(inplace=True)
    df.to_csv("clean_weather.csv", index=False)
    print(f"Data transformed successfully! Saved {len(df)} rows to clean_weather.csv")

if __name__ == "__main__":
    transform_data()