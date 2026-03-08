THRESHOLD = 50.0  # kWh threshold

DEVICES = {
    "AC":          {"critical": False, "power_kw": 2.5},
    "Lights":      {"critical": True,  "power_kw": 0.5},
    "Fans":        {"critical": True,  "power_kw": 0.3},
    "Servers":     {"critical": False, "power_kw": 5.0},
    "Water Heater":{"critical": False, "power_kw": 3.0},
}

SOLAR_PEAK_HOURS = range(10, 16)  # 10 AM – 4 PM

def optimize(predicted_energy: float, current_hour: int) -> dict:
    suggestions = []
    actions     = []
    savings     = 0.0

    if predicted_energy > THRESHOLD:
        # Turn off non-critical devices
        for device, info in DEVICES.items():
            if not info["critical"]:
                actions.append(f"🔴 Turn OFF {device}")
                suggestions.append(f"Turn off {device} to save {info['power_kw']} kW")
                savings += info["power_kw"]

        # Load shifting
        if current_hour in range(8, 20):
            actions.append("🔄 Shift Server workload → 10 PM (off-peak)")
            suggestions.append("Shift non-critical server tasks to off-peak hours")

    # Renewable recommendation
    if current_hour in SOLAR_PEAK_HOURS:
        actions.append("☀️ Switch to SOLAR energy (peak solar hours)")
        suggestions.append("Solar energy available — prioritize solar over grid")
    else:
        actions.append("🔌 Use grid power (off solar hours)")

    status = "⚠️ HIGH LOAD — Optimization Active" if predicted_energy > THRESHOLD \
             else "✅ NORMAL — No action needed"

    return {
        "predicted_energy_kwh": round(predicted_energy, 2),
        "threshold_kwh":        THRESHOLD,
        "status":               status,
        "actions":              actions,
        "suggestions":          suggestions,
        "estimated_savings_kw": round(savings, 2),
    }