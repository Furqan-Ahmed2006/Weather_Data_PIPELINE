import json
import requests

def fetch_weather_data():
    print("Fetching data from Open-Meteo API...")
    url = "https://api.open-meteo.com/v1/forecast?latitude=31.5497&longitude=74.3436&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&past_days=7&forecast_days=3"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        with open("raw_weather.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Raw data successfully fetched and saved to raw_weather.json")
    else:
        raise Exception(f"API Error! Status Code: {response.status_code}")

if __name__ == "__main__":
    fetch_weather_data()