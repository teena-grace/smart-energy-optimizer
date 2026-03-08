from flask import Flask, jsonify, request
from flask_cors import CORS
from predict  import predict
from optimize import optimize
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Smart Energy Optimizer API 🚀"})

@app.route("/predict", methods=["POST"])
def predict_energy():
    data        = request.json
    temperature = data.get("temperature", 30)
    occupancy   = data.get("occupancy",   50)
    hour        = data.get("hour",        datetime.now().hour)
    day_of_week = data.get("day_of_week", datetime.now().weekday())

    predicted   = predict(temperature, occupancy, hour, day_of_week)
    result      = optimize(predicted, hour)
    return jsonify(result)

@app.route("/forecast", methods=["GET"])
def forecast():
    """Return 24-hour forecast for today"""
    import random
    hours    = list(range(24))
    forecast = []
    for h in hours:
        temp  = random.uniform(25, 38)
        occ   = random.randint(10, 90)
        pred  = predict(temp, occ, h, datetime.now().weekday())
        forecast.append({"hour": h, "predicted_kwh": round(pred, 2)})
    return jsonify(forecast)

@app.route("/history", methods=["GET"])
def history():
    df = pd.read_csv("data/energy_data.csv")
    sample = df.tail(48)[["timestamp", "energy_consumption"]].to_dict(orient="records")
    return jsonify(sample)

if __name__ == "__main__":
    app.run(debug=True, port=5000)