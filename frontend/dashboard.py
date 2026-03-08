import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time
import os

st.set_page_config(
    page_title="⚡ EnergyAI — Smart Optimizer",
    layout="wide",
    page_icon="🌿",
    initial_sidebar_state="expanded"
)

API = os.getenv("API_BASE_URL", "http://localhost:5001").rstrip("/")

# ─── PREMIUM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, body, .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* ── App background */
.stApp {
    background: linear-gradient(160deg, #f0fdf4 0%, #ffffff 40%, #f8fff8 100%);
    color: #1a2e1a;
}

/* ── Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14532d 0%, #166534 60%, #15803d 100%) !important;
    border-right: none;
    box-shadow: 4px 0 20px rgba(20,83,45,0.25);
}
[data-testid="stSidebar"] * { color: #dcfce7 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] label { color: #86efac !important; font-weight: 500 !important; }
[data-testid="stSidebar"] .stSlider > div > div > div { background: #4ade80 !important; }
[data-testid="stSidebar"] .stSlider > div > div { background: rgba(255,255,255,0.2) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 10px;
}
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 0.75rem 1rem !important;
    width: 100% !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(34,197,94,0.4) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(34,197,94,0.5) !important;
}

/* ── Main buttons */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.55rem 1.8rem;
    box-shadow: 0 3px 12px rgba(34,197,94,0.35);
    transition: all 0.25s ease;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(34,197,94,0.5);
    background: linear-gradient(135deg, #4ade80, #22c55e);
}

/* ── Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    border: 1px solid #bbf7d0;
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 4px 20px rgba(34,197,94,0.1), 0 1px 4px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); }
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #22c55e, #16a34a);
    border-radius: 2px 0 0 2px;
}
[data-testid="stMetricLabel"] { color: #4b7c59 !important; font-weight: 600 !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 0.8px; }
[data-testid="stMetricValue"] { color: #14532d !important; font-size: 2rem !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { color: #16a34a !important; font-weight: 600 !important; }

/* ── Info / alert boxes */
.stAlert {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
    border: 1px solid #86efac !important;
    border-left: 5px solid #22c55e !important;
    border-radius: 12px !important;
    color: #166534 !important;
}

/* ── Spinner */
.stSpinner > div { border-top-color: #22c55e !important; }

/* ── Divider */
hr { border-color: rgba(34,197,94,0.2) !important; margin: 1.5rem 0 !important; }

/* ── Progress bar */
.stProgress > div > div > div { background: linear-gradient(90deg, #22c55e, #4ade80) !important; }

/* ── Custom card classes */
.glass-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(20,83,45,0.08), 0 2px 8px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
    margin-bottom: 1rem;
}
.glass-card:hover {
    box-shadow: 0 12px 40px rgba(20,83,45,0.14);
    transform: translateY(-2px);
}

.hero-banner {
    background: linear-gradient(135deg, #14532d 0%, #166534 40%, #15803d 70%, #22c55e 100%);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(20,83,45,0.35);
    margin-bottom: 2rem;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(74,222,128,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%; left: -5%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(34,197,94,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
    position: relative; z-index: 1;
}
.hero-sub {
    font-size: 1.05rem;
    opacity: 0.85;
    margin-top: 0.5rem;
    font-weight: 400;
    position: relative; z-index: 1;
}
.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    position: relative; z-index: 1;
}

.action-pill {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1.5px solid #86efac;
    border-radius: 50px;
    padding: 0.5rem 1.1rem;
    margin: 0.3rem 0;
    font-size: 13px;
    font-weight: 600;
    color: #166534;
    width: 100%;
    box-shadow: 0 2px 8px rgba(34,197,94,0.12);
    transition: all 0.2s ease;
}
.action-pill:hover {
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    transform: translateX(4px);
    box-shadow: 0 4px 14px rgba(34,197,94,0.22);
}

.status-ok {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 16px;
    padding: 1.1rem 1.6rem;
    font-size: 1.05rem;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 6px 24px rgba(34,197,94,0.4);
    letter-spacing: 0.3px;
    margin: 1rem 0;
}
.status-warn {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    border-radius: 16px;
    padding: 1.1rem 1.6rem;
    font-size: 1.05rem;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 6px 24px rgba(245,158,11,0.4);
    letter-spacing: 0.3px;
    margin: 1rem 0;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #14532d;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #dcfce7;
}

.kpi-mini {
    background: linear-gradient(135deg, #f0fdf4, #ffffff);
    border: 1px solid #bbf7d0;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(34,197,94,0.08);
}
.kpi-mini .val { font-size: 1.6rem; font-weight: 800; color: #15803d; }
.kpi-mini .lbl { font-size: 11px; font-weight: 600; color: #4b7c59; text-transform: uppercase; letter-spacing: 0.7px; margin-top: 2px; }

.sidebar-section {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1rem;
}

.footer-bar {
    background: linear-gradient(135deg, #14532d, #166534);
    color: #86efac;
    text-align: center;
    padding: 1rem;
    border-radius: 16px;
    font-size: 13px;
    font-weight: 500;
    margin-top: 2rem;
    box-shadow: 0 4px 20px rgba(20,83,45,0.2);
}

/* Selectbox options */
.stSelectbox option { background: #14532d; color: white; }
</style>
""", unsafe_allow_html=True)


# ─── HERO BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">🌿 AI-Powered Platform</div>
    <div class="hero-title">⚡ Smart Energy Optimizer</div>
    <div class="hero-sub">
        Real-time AI predictions · Automated load balancing · Renewable energy advisory
    </div>
</div>
""", unsafe_allow_html=True)


# ─── LIVE KPI STRIP ──────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    ("🏢", "Building", "Smart Office"),
    ("📡", "Status",   "Live Monitor"),
    ("🕐", "Local Time", datetime.now().strftime("%H:%M")),
    ("📅", "Date", datetime.now().strftime("%d %b %Y")),
    ("🌿", "Mode", "Eco Optimize"),
]
for col, (icon, lbl, val) in zip([k1,k2,k3,k4,k5], kpis):
    col.markdown(f"""
    <div class="kpi-mini">
        <div class="val">{icon}</div>
        <div class="lbl">{lbl}</div>
        <div style="font-size:13px;font-weight:700;color:#166534;margin-top:4px">{val}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Control Panel")
    st.markdown("---")

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🌡️ Environment**")
    temperature = st.slider("Temperature (°C)", 15, 45, 30, key="temp")
    occupancy   = st.slider("Occupancy (%)",    0, 100, 60, key="occ")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🕐 Time Settings**")
    hour = st.slider("Hour of Day", 0, 23, datetime.now().hour)
    day  = st.selectbox("Day of Week", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    st.markdown('</div>', unsafe_allow_html=True)

    day_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}

    st.markdown("<br>", unsafe_allow_html=True)
    run_opt = st.button("⚡ Run AI Optimization", key="run")

    st.markdown("---")
    st.markdown("**📊 Quick Stats**")
    st.markdown("""
    <div style='font-size:12px;color:#86efac;line-height:2'>
    ✅ &nbsp;Model: Random Forest<br>
    ✅ &nbsp;Data: 8,760 hrs trained<br>
    ✅ &nbsp;Threshold: 50 kWh<br>
    ✅ &nbsp;Solar Window: 10–16h
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(255,255,255,0.08);border-radius:12px;padding:0.8rem;font-size:11px;color:#a3e635;text-align:center'>
    🌍 Zero IoT · 100% Software<br>Scalable to Smart Cities
    </div>""", unsafe_allow_html=True)


# ─── OPTIMIZATION RESULT ─────────────────────────────────────────────────────
if run_opt:
    with st.spinner("🤖 AI engine running optimization..."):
        time.sleep(0.6)
        try:
            res = requests.post(f"{API}/predict", json={
                "temperature": temperature,
                "occupancy":   occupancy,
                "hour":        hour,
                "day_of_week": day_map[day]
            }, timeout=5).json()
        except Exception:
            st.error("⚠️ API not reachable. Start Flask: `cd backend && python app.py`")
            st.stop()

    is_high = res["predicted_energy_kwh"] > res["threshold_kwh"]
    css_cls = "status-warn" if is_high else "status-ok"
    icon_s  = "⚠️" if is_high else "✅"
    st.markdown(f'<div class="{css_cls}">{icon_s} &nbsp; {res["status"]}</div>', unsafe_allow_html=True)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚡ Predicted Usage",  f"{res['predicted_energy_kwh']} kWh",  delta="Live")
    col2.metric("🎯 Peak Threshold",   f"{res['threshold_kwh']} kWh",          delta="Fixed")
    col3.metric("💰 Est. Savings",     f"{res['estimated_savings_kw']} kW",    delta="Savings")
    col4.metric("🌡️ Temperature",     f"{temperature} °C",                     delta=f"{occupancy}% occ.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Energy gauge
    gauge_val = res["predicted_energy_kwh"]
    gauge_max = 100
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gauge_val,
        delta={"reference": res["threshold_kwh"], "increasing": {"color": "#ef4444"}, "decreasing": {"color": "#22c55e"}},
        gauge={
            "axis": {"range": [0, gauge_max], "tickcolor": "#166534", "tickwidth": 1},
            "bar":  {"color": "#16a34a" if not is_high else "#f59e0b", "thickness": 0.3},
            "bgcolor": "#f0fdf4",
            "bordercolor": "#bbf7d0",
            "steps": [
                {"range": [0, 35],  "color": "#dcfce7"},
                {"range": [35, 50], "color": "#fef9c3"},
                {"range": [50, 100],"color": "#fef2f2"},
            ],
            "threshold": {"line": {"color": "#ef4444", "width": 4}, "thickness": 0.85, "value": res["threshold_kwh"]}
        },
        title={"text": "Energy Demand (kWh)", "font": {"size": 15, "color": "#166534"}},
        number={"font": {"size": 42, "color": "#14532d"}, "suffix": " kWh"}
    ))
    fig_gauge.update_layout(
        height=280, margin=dict(l=30, r=30, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter")
    )

    col_g, col_r = st.columns([1.1, 1])
    with col_g:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚡ Energy Gauge</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True, key="gauge")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🤖 AI Actions</div>', unsafe_allow_html=True)
        for a in res["actions"]:
            st.markdown(f'<div class="action-pill">{a}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="section-title">💬 Smart Suggestions</div>', unsafe_allow_html=True)
        for s_item in res["suggestions"]:
            st.info(s_item)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

# ─── 24-HOUR FORECAST ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 24-Hour Energy Demand Forecast</div>', unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns([1, 8])
with col_btn1:
    load_fc = st.button("📊 Load")

if load_fc:
    with st.spinner("Fetching forecast data..."):
        time.sleep(0.4)
        try:
            forecast = requests.get(f"{API}/forecast", timeout=5).json()
        except Exception:
            st.error("API not reachable.")
            st.stop()

    df_f = pd.DataFrame(forecast)
    peak_hours = df_f[df_f["predicted_kwh"] > 50]

    fig = go.Figure()

    # Solar window shading
    fig.add_vrect(x0=10, x1=16, fillcolor="rgba(250,204,21,0.10)",
                  layer="below", line_width=0,
                  annotation_text="☀️ Solar Window", annotation_position="top left",
                  annotation_font_color="#ca8a04", annotation_font_size=11)

    # Area fill
    fig.add_trace(go.Scatter(
        x=df_f["hour"], y=df_f["predicted_kwh"],
        fill="tozeroy", fillcolor="rgba(34,197,94,0.12)",
        mode="lines", name="Predicted",
        line=dict(color="#16a34a", width=3, shape="spline", smoothing=0.8)
    ))

    # Dots for peak hours
    if not peak_hours.empty:
        fig.add_trace(go.Scatter(
            x=peak_hours["hour"], y=peak_hours["predicted_kwh"],
            mode="markers", name="⚠️ Peak",
            marker=dict(color="#ef4444", size=10, symbol="circle",
                       line=dict(color="white", width=2))
        ))

    # Threshold dashed line
    fig.add_hline(y=50, line_dash="dot", line_color="#ef4444", line_width=2,
                  annotation_text="Peak Threshold (50 kWh)", annotation_font_color="#ef4444",
                  annotation_font_size=11)

    fig.update_layout(
        xaxis=dict(
            title="Hour of Day", showgrid=True, gridcolor="#f0fdf4",
            tickvals=list(range(0,24,2)),
            ticktext=[f"{h:02d}:00" for h in range(0,24,2)],
            tickfont=dict(size=11, color="#4b7c59"),
            title_font=dict(color="#166534")
        ),
        yaxis=dict(
            title="Energy (kWh)", showgrid=True, gridcolor="#f0fdf4",
            tickfont=dict(size=11, color="#4b7c59"),
            title_font=dict(color="#166534")
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        height=380, margin=dict(l=50, r=30, t=20, b=50),
        font=dict(family="Inter"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=11, color="#166534")),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#14532d", font_size=12, font_color="white")
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key="forecast")

    # Hourly breakdown summary
    avg_kwh = df_f["predicted_kwh"].mean()
    max_kwh = df_f["predicted_kwh"].max()
    peak_h  = df_f.loc[df_f["predicted_kwh"].idxmax(), "hour"]
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="kpi-mini"><div class="val">{avg_kwh:.1f}</div><div class="lbl">Avg kWh / hr</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-mini"><div class="val">{max_kwh:.1f}</div><div class="lbl">Peak kWh</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-mini"><div class="val">{peak_h:02d}:00</div><div class="lbl">Peak Hour</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-mini"><div class="val">{len(peak_hours)}</div><div class="lbl">High-Load Hours</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── HISTORICAL DATA ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Historical Consumption — Last 48 Hours</div>', unsafe_allow_html=True)

col_btn3, col_btn4 = st.columns([1, 8])
with col_btn3:
    load_hist = st.button("📂 Load")

if load_hist:
    with st.spinner("Loading historical data..."):
        time.sleep(0.4)
        try:
            hist = requests.get(f"{API}/history", timeout=5).json()
        except Exception:
            st.error("API not reachable.")
            st.stop()

    df_h = pd.DataFrame(hist)
    rolling_avg = df_h["energy_consumption"].rolling(4).mean()

    fig2 = go.Figure()

    # Main area
    fig2.add_trace(go.Scatter(
        x=df_h["timestamp"], y=df_h["energy_consumption"],
        fill="tozeroy", fillcolor="rgba(34,197,94,0.1)",
        mode="lines", name="Actual Usage",
        line=dict(color="#22c55e", width=2, shape="spline", smoothing=0.6)
    ))

    # Rolling average
    fig2.add_trace(go.Scatter(
        x=df_h["timestamp"], y=rolling_avg,
        mode="lines", name="Rolling Avg (4h)",
        line=dict(color="#f59e0b", width=2.5, dash="dot")
    ))

    fig2.update_layout(
        xaxis=dict(title="Timestamp", showgrid=True, gridcolor="#f0fdf4",
                   tickfont=dict(size=10, color="#4b7c59"), title_font=dict(color="#166534")),
        yaxis=dict(title="Energy (kWh)", showgrid=True, gridcolor="#f0fdf4",
                   tickfont=dict(size=10, color="#4b7c59"), title_font=dict(color="#166534")),
        plot_bgcolor="white", paper_bgcolor="white",
        height=360, margin=dict(l=50, r=30, t=20, b=50),
        font=dict(family="Inter"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=11, color="#166534")),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#14532d", font_size=12, font_color="white")
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, key="history")
    st.markdown('</div>', unsafe_allow_html=True)


# ─── DEVICE STATUS PANEL ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📱 Device Control Status</div>', unsafe_allow_html=True)

devices = [
    ("❄️", "Air Conditioning", "2.5 kW",  "Non-Critical", "#ef4444", "OFF at peak"),
    ("💡", "Lighting",          "0.5 kW",  "Critical",     "#22c55e", "Always ON"),
    ("🌀", "Ventilation Fans",  "0.3 kW",  "Critical",     "#22c55e", "Always ON"),
    ("🖥️","Server Cluster",    "5.0 kW",  "Non-Critical", "#f59e0b", "Shift to 10 PM"),
    ("🚿", "Water Heater",      "3.0 kW",  "Non-Critical", "#ef4444", "OFF at peak"),
    ("☀️", "Solar Inverter",    "— kW",    "Renewable",    "#4ade80", "10:00–16:00"),
]

cols = st.columns(3)
for i, (icon, name, power, priority, color, action) in enumerate(devices):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid {color};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:28px">{icon}</div>
                <div style="background:{color}22;color:{color};font-size:10px;font-weight:700;
                            padding:3px 10px;border-radius:50px;border:1px solid {color}44;">
                    {priority}
                </div>
            </div>
            <div style="font-size:15px;font-weight:700;color:#14532d;margin-top:0.6rem">{name}</div>
            <div style="font-size:12px;color:#4b7c59;margin-top:2px">Power: <b>{power}</b></div>
            <div style="margin-top:0.6rem;font-size:12px;font-weight:600;color:{color}">→ {action}</div>
        </div>""", unsafe_allow_html=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    ⚡ <b>EnergyAI Smart Optimizer</b> &nbsp;·&nbsp; Built for Hackathon 2025 &nbsp;·&nbsp;
    🌍 Powered by ML + Python &nbsp;·&nbsp;
    <span style="color:#4ade80">🌿 Saving Energy. Saving Earth.</span>
</div>
""", unsafe_allow_html=True)
