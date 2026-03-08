import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "energy_data.csv"
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "energy_model.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"


def _fallback_training_data(rows=24 * 30, seed=42):
    """Generate synthetic data when CSV is unavailable in deployment."""
    rng = np.random.default_rng(seed)
    temperature = rng.uniform(18, 42, rows)
    occupancy = rng.integers(5, 100, rows)
    hour = rng.integers(0, 24, rows)
    day_of_week = rng.integers(0, 7, rows)

    energy = (
        18
        + 0.7 * temperature
        + 0.35 * occupancy
        + np.where((hour >= 9) & (hour <= 18), 6.5, 1.5)
        + np.where(day_of_week >= 5, -2.0, 2.0)
        + rng.normal(0, 2.2, rows)
    )
    energy = np.clip(energy, 8, None)

    return pd.DataFrame(
        {
            "temperature": temperature,
            "occupancy": occupancy,
            "hour": hour,
            "day_of_week": day_of_week,
            "energy_consumption": energy,
        }
    )


def train_model():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    else:
        print(f"Warning: {DATA_PATH} not found. Using synthetic fallback data.")
        df = _fallback_training_data()

    features = ["temperature", "occupancy", "hour", "day_of_week"]
    target = "energy_consumption"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    preds = model.predict(X_test_scaled)
    print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
    print(f"R2: {r2_score(y_test, preds):.4f}")

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print("Model saved to models/")


def predict(temperature, occupancy, hour, day_of_week):
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        train_model()

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    X = pd.DataFrame(
        [[temperature, occupancy, hour, day_of_week]],
        columns=["temperature", "occupancy", "hour", "day_of_week"],
    )
    X_scaled = scaler.transform(X)
    return float(model.predict(X_scaled)[0])


if __name__ == "__main__":
    train_model()
