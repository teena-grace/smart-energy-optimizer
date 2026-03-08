import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n = 8760  # 1 year hourly data

timestamps = [datetime(2024, 1, 1) + timedelta(hours=i) for i in range(n)]
temperature = np.random.uniform(18, 42, n)
occupancy   = np.random.randint(0, 100, n)
hour        = [t.hour for t in timestamps]
day_of_week = [t.weekday() for t in timestamps]

# Simulate realistic energy consumption
energy = (
    20 +
    0.5 * temperature +
    0.3 * occupancy +
    np.sin(np.array(hour) * np.pi / 12) * 10 +
    np.random.normal(0, 2, n)
)

df = pd.DataFrame({
    "timestamp": timestamps,
    "temperature": temperature,
    "occupancy": occupancy,
    "hour": hour,
    "day_of_week": day_of_week,
    "energy_consumption": energy
})

df.to_csv("data/energy_data.csv", index=False)
print("✅ Dataset generated: data/energy_data.csv")
print(df.head())