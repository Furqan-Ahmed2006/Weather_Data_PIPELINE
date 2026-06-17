import os
import pickle
import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score 
from dotenv import load_dotenv

load_dotenv()

def train_predictive_model():
    print("Fetching training data from Cloud Database...")
    
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    query = "SELECT temperature, humidity, wind_speed, target_temperature FROM weather_history"
    df = pd.read_sql(query, conn)
    conn.close()
    
    if len(df) < 10:
        print("Not enough data to train the model yet!")
        return

    X = df[["temperature", "humidity", "wind_speed"]]
    y = df["target_temperature"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training new Random Forest Regressor model...")
    new_model = RandomForestRegressor(n_estimators=100, random_state=42)
    new_model.fit(X_train, y_train)
    
    predictions = new_model.predict(X_test)
    new_mae = mean_absolute_error(y_test, predictions)

    accuracy = r2_score(y_test, predictions) * 100
    if accuracy < 0: 
        accuracy = 0 
    
    print(f"New Model Mean Absolute Error: {new_mae:.2f}°C")
    print(f" New Model Accuracy: {accuracy:.2f}%") 

    old_mae_file = "model_score.txt"
    should_save = True
    
    if os.path.exists("weather_model.pkl") and os.path.exists(old_mae_file):
        with open(old_mae_file, "r") as f:
            old_mae = float(f.read())
        print(f"Existing Model MAE was: {old_mae:.2f}°C")
        
        if new_mae >= old_mae:
            print(" New model is not better than the old one. Keeping the existing model.")
            should_save = False
        else:
            print(" New model has better accuracy (Lower Error)! Updating...")
            
    if should_save:
        with open("weather_model.pkl", "wb") as f:
            pickle.dump(new_model, f)
        with open(old_mae_file, "w") as f:
            f.write(str(new_mae))
        print(" Best model saved successfully!")

if __name__ == "__main__":
    train_predictive_model()