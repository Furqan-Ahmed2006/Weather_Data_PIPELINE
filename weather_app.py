import pickle
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Lahore Weather Forecast", page_icon="☀️", layout="wide")


st.markdown("""
    <style>
    .main { background-color: #111216; }
    .big-temp { font-size: 75px !important; font-weight: 300; color: #F8B125; line-height: 1; }
    .weather-unit { font-size: 30px; vertical-align: super; color: #F8B125; }
    .condition-text { font-size: 24px; color: #A0A0A0; margin-bottom: 20px; }
    .info-box { background-color: #1A1C23; padding: 15px; border-radius: 12px; border: 1px solid #2D313E; text-align: center; }
    .card-title { color: #8A90A6; font-size: 14px; margin-bottom: 5px; }
    .card-value { font-size: 18px; font-weight: bold; color: #E3E6ED; }
    .hourly-card { background-color: #1A1C23; padding: 10px; border-radius: 8px; text-align: center; min-width: 80px; border: 1px solid #2D313E; }
    </style>
""", unsafe_allow_html=True)


st_autorefresh(interval=10000, key="google_weather_refresh")


def get_weather_condition(code, is_day=True):
    if code in [0, 1]:
        return "Sunny" if is_day else "Clear Night"
    elif code in [2, 3]:
        return "Partly Cloudy"
    elif code in [45, 48]:
        return "Foggy"
    elif code in [51, 53, 55, 61, 63, 65]:
        return "Rainy"
    elif code in [80, 81, 82]:
        return "Showers"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    return "Clear" if not is_day else "Sunny"


try:
    with open("weather_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Model file 'weather_model.pkl' not found.")
    st.stop()


@st.cache_data(ttl=600)
def fetch_live_forecast():
    url = "https://api.open-meteo.com/v1/forecast?latitude=31.5497&longitude=74.3436&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=Asia%2FKarachi&forecast_days=3"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

data = fetch_live_forecast()

if data:
    hourly_data = data["hourly"]
    df = pd.DataFrame(hourly_data)
    df.rename(columns={
        "time": "Timestamp",
        "temperature_2m": "Actual Temperature",
        "relative_humidity_2m": "Humidity",
        "wind_speed_10m": "Wind Speed",
        "weather_code": "WeatherCode"
    }, inplace=True)
    
    df["Timestamp_dt"] = pd.to_datetime(df["Timestamp"])
    
    current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    live_row_match = df[df["Timestamp_dt"] == current_hour]
    latest_row = live_row_match.iloc[0] if not live_row_match.empty else df.iloc[0]
    
    current_hour_int = datetime.now().hour
    is_daytime = 6 <= current_hour_int < 19
    current_condition = get_weather_condition(latest_row['WeatherCode'], is_day=is_daytime)
    
    # ML Predictions
    X_live = df[["Actual Temperature", "Humidity", "Wind Speed"]].copy()
    X_live.columns = ["temperature", "humidity", "wind_speed"]
    df["ML Predicted Temp"] = model.predict(X_live)

    
    st.markdown("<h2 style='margin-bottom:0;'>📍 Lahore, Pakistan</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8A90A6;'>Weather • {datetime.now().strftime('%A %I:%M %p')} • {current_condition}</p>", unsafe_allow_html=True)
    
    
    col_temp, col_metrics = st.columns([1, 2])
    
    with col_temp:
        st.markdown(f"<div class='big-temp'>{latest_row['Actual Temperature']:.0f}<span class='weather-unit'>°C</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='condition-text'>{current_condition}</div>", unsafe_allow_html=True)
        
    with col_metrics:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='info-box'><div class='card-title'>Humidity</div><div class='card-value'>{latest_row['Humidity']}%</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='info-box'><div class='card-title'>Wind Speed</div><div class='card-value'>{latest_row['Wind Speed']} km/h</div></div>", unsafe_allow_html=True)
        with c3:
            current_pred = df[df["Timestamp_dt"] == current_hour]["ML Predicted Temp"].values
            val = current_pred[0] if len(current_pred) > 0 else latest_row['Actual Temperature']
            st.markdown(f"<div class='info-box' style='border: 1px solid #F8B125;'><div class='card-title' style='color:#F8B125;'>ML Prediction (Next Day)</div><div class='card-value' style='color:#F8B125;'>{val:.1f}°C</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h3>Hourly Forecast (Next 8 Hours)</h3>", unsafe_allow_html=True)
    hourly_cols = st.columns(8)
    
    future_hourly_df = df[df["Timestamp_dt"] > current_hour].head(8)
    
    for idx, col in enumerate(hourly_cols):
        if idx < len(future_hourly_df):
            row = future_hourly_df.iloc[idx]
            hr_dt = pd.to_datetime(row["Timestamp"])
            hour_str = hr_dt.strftime('%I %p')
            hr_is_day = 6 <= hr_dt.hour < 19
            
            cond_str = get_weather_condition(row['WeatherCode'], is_day=hr_is_day)
            icon = "☀️" if "Sunny" in cond_str else ("🌙" if "Clear Night" in cond_str else "☁️")
            
            with col:
                st.markdown(f"""
                    <div class='hourly-card'>
                        <div style='color:#8A90A6; font-size:12px;'>{hour_str}</div>
                        <div style='font-size:25px; margin:5px 0;'>{icon}</div>
                        <div style='color:#E3E6ED; font-weight:bold;'>{row['Actual Temperature']:.0f}°</div>
                        <div style='color:#4285F4; font-size:11px;'>{row['ML Predicted Temp']:.0f}° (ML)</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📊 Weather Analytics: Actual vs ML Prediction Trend")
    st.write("💡 *Yellow Line represents the Actual Weather API Forecast, and the Blue Line shows your Machine Learning Model's Predictions.*")
    
    chart_df = df[df["Timestamp_dt"] >= current_hour].head(24).copy()
    chart_df["Hour"] = chart_df["Timestamp_dt"].dt.strftime('%I %p')
    chart_df.set_index("Hour", inplace=True)
    
    st.line_chart(chart_df[["Actual Temperature", "ML Predicted Temp"]], color=["#F8B125", "#4285F4"])

else:
    st.error("Failed to fetch live data from Open-Meteo API.")