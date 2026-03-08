# ⚡ Smart Energy Optimizer

https://smart-energy-dashboard-samh.onrender.com
https://smart-energy-optimizer-us1y.onrender.com

> AI-powered energy management platform for smart buildings — real-time load prediction, automated optimization, and renewable energy advisory.

---

## 🌿 Overview

Smart Energy Optimizer is a full-stack ML application that predicts building energy consumption and automatically recommends actions to reduce peak load, shift non-critical workloads, and maximize renewable energy usage. It was built for **Hackathon 2025**.

The system is trained on a year's worth of simulated hourly data (8,760 records) and uses a **Random Forest Regressor** to predict energy demand based on temperature, occupancy, time of day, and day of week.

---

## ✨ Features

- **⚡ Live Energy Prediction** — Predicts kWh demand from environmental and time inputs
- **🤖 AI Optimization Engine** — Automatically recommends device shutoffs, load shifts, and solar switching
- **📈 24-Hour Forecast** — Hourly demand forecast for the full day with peak-hour detection
- **📊 Historical Dashboard** — Last 48 hours of consumption with rolling average overlay
- **📱 Device Control Panel** — Visual status for AC, lighting, servers, water heater, and solar inverter
- **☀️ Renewable Advisory** — Detects solar peak window (10 AM–4 PM) and recommends grid switching
- **🎨 Premium UI** — Glassmorphism design with animated metrics, gauges, and responsive layout

---

## 🗂️ Project Structure

```
smart-energy-optimizer/
│
├── backend/
│   ├── app.py          # Flask REST API (predict, forecast, history endpoints)
│   ├── predict.py      # ML model training and inference (Random Forest)
│   ├── optimize.py     # Optimization logic (load shedding, solar advisory)
│   └── startup.py      # Auto-generates data and trains model on first run
│
├── data/
│   └── generate_data.py  # Generates 8,760 hours of synthetic training data
│
├── frontend/
│   └── dashboard.py    # Streamlit dashboard UI
│
├── models/             # Auto-created on first run
│   ├── energy_model.pkl
│   └── scaler.pkl
│
├── Procfile            # For deployment (e.g. Render, Railway)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/smart-energy-optimizer.git
cd smart-energy-optimizer

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

**Step 1 — Start the Flask backend**

```bash
cd backend
python startup.py        # Generates data + trains model (first run only)
python app.py            # Starts API on http://localhost:5000
```

**Step 2 — Launch the Streamlit frontend** (in a new terminal)

```bash
streamlit run frontend/dashboard.py
```

The dashboard will open at `http://localhost:8501`.

---

## 🔌 API Reference

Base URL: `http://localhost:5000` (local) or your deployed Render URL

### `GET /`
Health check.

**Response:**
```json
{ "message": "Smart Energy Optimizer API 🚀" }
```

---

### `POST /predict`
Predict energy consumption and get optimization actions.

**Request Body:**
```json
{
  "temperature": 30,
  "occupancy": 60,
  "hour": 14,
  "day_of_week": 0
}
```

| Field | Type | Description |
|---|---|---|
| `temperature` | float | Ambient temperature in °C (15–45) |
| `occupancy` | int | Building occupancy percentage (0–100) |
| `hour` | int | Hour of day (0–23) |
| `day_of_week` | int | 0 = Monday … 6 = Sunday |

**Response:**
```json
{
  "predicted_energy_kwh": 58.34,
  "threshold_kwh": 50.0,
  "status": "⚠️ HIGH LOAD — Optimization Active",
  "actions": ["🔴 Turn OFF AC", "☀️ Switch to SOLAR energy"],
  "suggestions": ["Turn off AC to save 2.5 kW", "Solar energy available"],
  "estimated_savings_kw": 11.0
}
```

---

### `GET /forecast`
Returns a 24-hour energy demand forecast for the current day.

**Response:**
```json
[
  { "hour": 0, "predicted_kwh": 28.14 },
  { "hour": 1, "predicted_kwh": 25.87 },
  ...
]
```

---

### `GET /history`
Returns the last 48 hours of recorded energy consumption.

**Response:**
```json
[
  { "timestamp": "2024-12-30 08:00:00", "energy_consumption": 42.3 },
  ...
]
```

---

## 🤖 ML Model

| Property | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Training data | 8,760 hourly records (1 year) |
| Features | temperature, occupancy, hour, day_of_week |
| Target | energy_consumption (kWh) |
| Train/test split | 80 / 20 |
| Preprocessing | StandardScaler |

The model is auto-trained on first startup via `startup.py`. Retrain manually:

```bash
cd backend
python predict.py
```

---

## ⚙️ Optimization Logic

The optimizer (`optimize.py`) applies the following rules:

- **Peak threshold:** 50 kWh
- If predicted load **exceeds threshold**, non-critical devices (AC, Servers, Water Heater) are flagged for shutdown
- Server workloads are shifted to **off-peak hours (10 PM)** if triggered during business hours
- **Solar window:** 10:00–16:00 — system recommends switching to solar during this period

### Device Priority Table

| Device | Priority | Power | Action at Peak |
|---|---|---|---|
| Air Conditioning | Non-Critical | 2.5 kW | Turn OFF |
| Lighting | Critical | 0.5 kW | Always ON |
| Ventilation Fans | Critical | 0.3 kW | Always ON |
| Server Cluster | Non-Critical | 5.0 kW | Shift to 10 PM |
| Water Heater | Non-Critical | 3.0 kW | Turn OFF |
| Solar Inverter | Renewable | — | Active 10–16h |

---

## ☁️ Deployment

The app is configured for deployment on [Render](https://render.com).

**Backend (Flask API):**
Set the `API_URL` environment variable in `frontend/dashboard.py` or as an env var on your hosting platform to point to your deployed backend URL.

```
API_URL=https://your-app.onrender.com
```

**Frontend (Streamlit):**
Deploy separately on [Streamlit Community Cloud](https://streamlit.io/cloud) or as a second Render service.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Plotly |
| Backend | Flask, Flask-CORS |
| ML | scikit-learn (Random Forest) |
| Data | pandas, NumPy |
| Model persistence | joblib |
| Deployment | Render |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  <b>⚡ EnergyAI Smart Optimizer</b> &nbsp;·&nbsp; Built for Hackathon 2025 &nbsp;·&nbsp; 🌿 Saving Energy. Saving Earth.
</div>
