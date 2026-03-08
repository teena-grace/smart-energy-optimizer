import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_model():
    df = pd.read_csv("data/energy_data.csv")

    features = ["temperature", "occupancy", "hour", "day_of_week"]
    target   = "energy_consumption"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    preds = model.predict(X_test_scaled)
    print(f"MAE : {mean_absolute_error(y_test, preds):.2f}")
    print(f"R²  : {r2_score(y_test, preds):.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model,  "models/energy_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    print("✅ Model saved to models/")

def predict(temperature, occupancy, hour, day_of_week):
    model  = joblib.load("models/energy_model.pkl")
    scaler = joblib.load("models/scaler.pkl")

    X = pd.DataFrame([[temperature, occupancy, hour, day_of_week]],
                     columns=["temperature", "occupancy", "hour", "day_of_week"])
    X_scaled = scaler.transform(X)
    return float(model.predict(X_scaled)[0])

if __name__ == "__main__":
    train_model()