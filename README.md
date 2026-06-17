# 🌤️ Weather Data Pipeline

A comprehensive data pipeline project that fetches real-time weather data, transforms it, and trains a machine learning model to predict future temperatures. The project integrates with cloud databases and includes a Streamlit web application for interactive predictions.

---

## 📋 Project Overview

This project implements an end-to-end data pipeline that:

1. **Fetches** real-time weather data from the Open-Meteo API
2. **Transforms** raw JSON data into clean, structured CSV format
3. **Trains** a machine learning model to predict future temperatures based on weather features
4. **Stores** historical data in a cloud-based MySQL database
5. **Serves** predictions through an interactive web application

The pipeline is designed to be automated and scalable, with CI/CD integration via GitHub Actions.

---

## 🎯 Key Features

- ✅ **Automated Data Ingestion** - Fetches weather data from Open-Meteo API
- ✅ **Data Transformation** - Cleans and prepares data for ML model training
- ✅ **ML Model Training** - Trains a Random Forest Regressor for temperature prediction
- ✅ **Model Versioning** - Only saves improved models (based on Mean Absolute Error)
- ✅ **Cloud Database Integration** - Connects to MySQL for data persistence
- ✅ **Interactive Web App** - Streamlit application for real-time predictions
- ✅ **CI/CD Automation** - GitHub Actions workflow for automated pipeline execution
- ✅ **Environment Configuration** - Secure credential management via `.env` file

---

## 📁 Project Structure

```
Weather_Data_PIPELINE/
├── data_ingestion.py          # Fetches raw weather data from API
├── transformation.py          # Cleans and prepares data
├── train_model.py             # Trains ML model and manages versioning
├── load_data.py               # Loads and processes data
├── weather_app.py             # Streamlit web application
├── check.py                   # Data validation utilities
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in repo)
├── .github/workflows/         # CI/CD workflows
│   └── weather_pipeline.yml   # Automated pipeline execution
├── raw_weather.json           # Raw API response data
├── clean_weather.csv          # Processed training data
├── weather_model.pkl          # Trained ML model
├── model_score.txt            # Current model MAE score
└── .gitignore                 # Git ignore rules
```

---

## 🔧 What I Did

### 1. **Data Ingestion (`data_ingestion.py`)**
   - Fetches real-time weather data from the **Open-Meteo API** (free, no API key required)
   - Retrieves current weather metrics: temperature, humidity, wind speed, precipitation
   - Saves raw JSON response to `raw_weather.json` for transparency and debugging

### 2. **Data Transformation (`transformation.py`)**
   - Parses hourly weather data from the JSON response
   - Converts data into a pandas DataFrame for easier manipulation
   - Renames columns for clarity (e.g., `temperature_2m` → `temperature`)
   - **Creates target variable**: Shifts temperature 24 hours forward to predict next day's temperature
   - Removes rows with missing values (NaN)
   - Exports cleaned data to `clean_weather.csv`

### 3. **Model Training (`train_model.py`)**
   - Connects to a cloud-based **MySQL database** using credentials from `.env`
   - Fetches historical weather data from the database
   - **Trains a Random Forest Regressor** with 100 decision trees
   - Splits data into 80% training and 20% testing sets
   - Evaluates model performance using:
     - **Mean Absolute Error (MAE)**: Average prediction error in °C
     - **R² Score**: Percentage of variance explained by the model
   - **Smart Model Versioning**: Only saves the model if it performs better than the previous one
   - Persists the best model using pickle serialization

### 4. **Data Processing (`load_data.py`)**
   - Loads and processes data from multiple sources
   - Prepares data for model training and predictions

### 5. **Web Application (`weather_app.py`)**
   - **Streamlit-based interactive dashboard**
   - Displays real-time weather information
   - Makes temperature predictions using the trained model
   - Auto-refreshes to show latest data and predictions
   - User-friendly interface for non-technical users

### 6. **Data Validation (`check.py`)**
   - Validates data quality and integrity
   - Ensures data consistency throughout the pipeline

### 7. **CI/CD Automation (`.github/workflows/weather_pipeline.yml`)**
   - Automated workflow that runs the entire pipeline on schedule
   - Triggers data ingestion → transformation → model training sequentially
   - Ensures the pipeline stays up-to-date automatically

---

## 📊 Data Flow

```
┌─────────────────────┐
│  Open-Meteo API     │
└──────────┬──────────┘
           │ (fetch_weather_data())
           ↓
┌─────────────────────┐
│ raw_weather.json    │
└──────────┬──────────┘
           │ (transform_data())
           ↓
┌─────────────────────┐
│ clean_weather.csv   │
└──────────┬──────────┘
           │ (train_predictive_model())
           ↓
┌─────────────────────────────────┐
│ MySQL Database (weather_history)│
└──────────┬──────────────────────┘
           │
           ↓
┌──────────────────────────────────────┐
│ Trained ML Model (weather_model.pkl) │
│ + Performance Score (model_score.txt)│
└──────────┬───────────────────────────┘
           │
           ↓
┌──────────────────────┐
│ Streamlit Web App    │
│ (weather_app.py)     │
└──────────────────────┘
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL database (cloud or local)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Furqan-Ahmed2006/Weather_Data_PIPELINE.git
cd Weather_Data_PIPELINE
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```bash
# Database Configuration
DB_HOST=your_mysql_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=weather_db
```

### Step 5: Set Up Database
Create the required table in your MySQL database:
```sql
CREATE TABLE weather_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    target_temperature FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🏃 Running the Pipeline

### Option 1: Run Individual Modules
```bash
# Fetch fresh weather data
python data_ingestion.py

# Transform and clean data
python transformation.py

# Train the ML model
python train_model.py
```

### Option 2: Run the Web Application
```bash
streamlit run weather_app.py
```
The app will be available at `http://localhost:8501`

### Option 3: Automated Pipeline (GitHub Actions)
The pipeline runs automatically on schedule (configured in `.github/workflows/weather_pipeline.yml`)

---

## 📈 Model Performance

The model tracks its performance using:
- **Mean Absolute Error (MAE)**: How far off predictions are, on average (in °C)
- **R² Score**: How well the model explains temperature variation (0-100%)
- **Current Score**: Stored in `model_score.txt`

The model uses the following features for prediction:
| Feature | Description |
|---------|-------------|
| temperature | Current temperature in °C |
| humidity | Relative humidity percentage |
| wind_speed | Wind speed in km/h |

---

## 🔒 Security Best Practices

- ✅ Sensitive credentials stored in `.env` (not committed to repo)
- ✅ Database credentials loaded using `python-dotenv`
- ✅ API calls use HTTPS
- ✅ `.gitignore` protects sensitive files

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP API calls |
| `pandas` | Data manipulation & analysis |
| `scikit-learn` | Machine learning models |
| `mysql-connector-python` | MySQL database connection |
| `python-dotenv` | Environment variable management |
| `streamlit` | Web application framework |
| `streamlit-autorefresh` | Auto-refresh functionality |
| `pytz` | Timezone handling |

---

## 🛠️ Troubleshooting

### API Connection Issues
- Verify internet connection
- Check Open-Meteo API status: https://api.open-meteo.com

### Database Connection Errors
- Verify `.env` credentials are correct
- Ensure MySQL server is running
- Check database table exists with correct schema

### Model Training Issues
- Ensure `clean_weather.csv` exists
- Verify database has sufficient historical data (minimum 10 rows)
- Check that `weather_history` table is populated

### Streamlit App Won't Start
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/
streamlit run weather_app.py
```

---

## 📝 Output Files Generated

| File | Description |
|------|-------------|
| `raw_weather.json` | Raw API response (hourly & current weather) |
| `clean_weather.csv` | Processed data ready for ML training |
| `weather_model.pkl` | Serialized trained Random Forest model |
| `model_score.txt` | Current model's Mean Absolute Error |

---

## 🔄 How Model Versioning Works

1. **Train** a new model on the latest data
2. **Calculate** MAE on test set
3. **Compare** with previous best MAE (from `model_score.txt`)
4. **Decision**:
   - If new MAE < old MAE → Save new model ✅
   - If new MAE ≥ old MAE → Keep old model ⏹️

This ensures only improvements are deployed to production.

---

## 🎓 Learning Outcomes

This project demonstrates:
- End-to-end data pipeline design
- ETL (Extract, Transform, Load) processes
- Machine learning model development
- Cloud database integration
- CI/CD automation with GitHub Actions
- Web application development with Streamlit
- Best practices for data science projects

---

## 📌 Future Enhancements

- [ ] Add more weather features (precipitation, weather codes)
- [ ] Implement hyperparameter tuning for the ML model
- [ ] Add data quality monitoring & alerting
- [ ] Deploy model to production API
- [ ] Add prediction confidence intervals
- [ ] Implement A/B testing for model versions
- [ ] Add support for multiple locations
- [ ] Create forecasting beyond 24 hours

---

## 📧 Contact & Support

For questions or issues, please open an issue on GitHub.

---

## 📄 License

This project is open source and available under the MIT License.

---

**Last Updated**: June 2026  
**Status**: Active & Maintained ✅
