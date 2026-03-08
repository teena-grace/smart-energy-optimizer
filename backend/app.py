from datetime import datetime
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

from optimize import optimize
from predict import predict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "energy_data.csv"

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({"message": "Smart Energy Optimizer API"})


@app.route("/predict", methods=["POST"])
def predict_energy():
    data = request.json or {}
    temperature = data.get("temperature", 30)
    occupancy = data.get("occupancy", 50)
    hour = data.get("hour", datetime.now().hour)
    day_of_week = data.get("day_of_week", datetime.now().weekday())

    predicted = predict(temperature, occupancy, hour, day_of_week)
    result = optimize(predicted, hour)
    return jsonify(result)


@app.route("/forecast", methods=["GET"])
def forecast():
    """Return 24-hour forecast for today."""
    import random

    hours = list(range(24))
    forecast_data = []
    for h in hours:
        temp = random.uniform(25, 38)
        occ = random.randint(10, 90)
        pred = predict(temp, occ, h, datetime.now().weekday())
        forecast_data.append({"hour": h, "predicted_kwh": round(pred, 2)})
    return jsonify(forecast_data)


@app.route("/history", methods=["GET"])
def history():
    df = pd.read_csv(DATA_PATH)
    sample = df.tail(48)[["timestamp", "energy_consumption"]].to_dict(orient="records")
    return jsonify(sample)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
