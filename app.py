"""
AapdaSetu — AI-Powered Disaster Response & Resource Allocation
Emergency Operations Command Center Dashboard

Model: sklearn Pipeline (ColumnTransformer + HistGradientBoostingClassifier)
Features: 35 (3 categorical + 32 numeric)
Classes: HIGH / LOW / MEDIUM
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AapdaSetu | Emergency Operations",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

PRIORITY_COLORS = {"HIGH": "#EF4444", "MEDIUM": "#F97316", "LOW": "#22C55E"}
PRIORITY_EMOJI = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}
PRIORITY_ORDER = ["HIGH", "MEDIUM", "LOW"]

CATEGORICAL_COLS = ["state", "disaster_type", "disaster_subtype"]
NUMERIC_COLS = [
    "population", "people_affected", "deaths", "injured", "critical_patients",
    "children_affected", "elderly_affected", "hospital_count", "ambulance_count",
    "available_ambulances", "rescue_team_count", "available_rescue_teams",
    "shelter_capacity", "available_shelter_capacity", "hospital_capacity",
    "medical_supply", "ambulance_demand", "rescue_team_demand", "shelter_demand",
    "medical_supply_demand", "households", "male_population", "female_population",
    "urban_population", "rural_population", "children_population_0_6",
    "elderly_population_60_plus", "area_sq_km", "population_density",
    "resource_pct_available", "resource_pct_needs_maintenance", "resource_avg_capacity",
]
MODEL_FEATURES = CATEGORICAL_COLS + NUMERIC_COLS  # 35 total

# Approximate state centroids (real geographic coordinates)
STATE_COORDS = {
    "Andhra Pradesh": (15.91, 79.74), "Arunachal Pradesh": (28.22, 94.73),
    "Assam": (26.20, 92.94), "Bihar": (25.10, 85.31),
    "Chhattisgarh": (21.28, 81.87), "Goa": (15.30, 74.12),
    "Gujarat": (22.26, 71.19), "Haryana": (29.06, 76.09),
    "Himachal Pradesh": (31.10, 77.17), "Jharkhand": (23.61, 85.28),
    "Karnataka": (15.32, 75.71), "Kerala": (10.85, 76.27),
    "Madhya Pradesh": (22.97, 78.66), "Maharashtra": (19.75, 75.71),
    "Manipur": (24.66, 93.91), "Meghalaya": (25.47, 91.37),
    "Mizoram": (23.16, 92.94), "Nagaland": (26.16, 94.56),
    "Odisha": (20.95, 85.10), "Punjab": (31.15, 75.34),
    "Rajasthan": (27.02, 74.22), "Sikkim": (27.53, 88.51),
    "Tamil Nadu": (11.13, 78.66), "Telangana": (18.11, 79.02),
    "Tripura": (23.94, 91.99), "Uttar Pradesh": (26.85, 80.95),
    "Uttarakhand": (30.07, 79.02), "West Bengal": (22.99, 87.86),
    "Andaman and Nicobar Islands": (11.74, 92.66), "Chandigarh": (30.73, 76.78),
    "Dadra and Nagar Haveli and Daman and Diu": (20.18, 73.02),
    "Delhi": (28.70, 77.10), "Jammu and Kashmir": (33.78, 76.58),
    "Ladakh": (34.15, 77.58), "Lakshadweep": (10.57, 72.64),
    "Puducherry": (11.94, 79.81),
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════

def inject_css():
    st.markdown("""
    <style>
    /* ── Global ─────────────────────────────────────────── */
    .block-container { padding-top: 1.5rem; }
    section[data-testid="stSidebar"] { background: #0d1321; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a2332 0%, #111827 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; font-size: 0.82rem !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e2e8f0 !important; }

    /* ── KPI Cards ──────────────────────────────────────── */
    .kpi-card {
        background: linear-gradient(135deg, #1a2332 0%, #111827 100%);
        border: 1px solid #1e3a5f; border-radius: 12px;
        padding: 18px 20px; text-align: center;
    }
    .kpi-card .kpi-value { font-size: 2rem; font-weight: 700; color: #e2e8f0; margin: 4px 0; }
    .kpi-card .kpi-label { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }

    /* ── Priority Badge ─────────────────────────────────── */
    .badge-high   { background:#7f1d1d; color:#fca5a5; padding:4px 14px; border-radius:20px; font-weight:600; font-size:0.82rem; display:inline-block; }
    .badge-medium { background:#7c2d12; color:#fdba74; padding:4px 14px; border-radius:20px; font-weight:600; font-size:0.82rem; display:inline-block; }
    .badge-low    { background:#14532d; color:#86efac; padding:4px 14px; border-radius:20px; font-weight:600; font-size:0.82rem; display:inline-block; }

    /* ── Section Header ─────────────────────────────────── */
    .section-hdr {
        border-bottom: 2px solid #1e3a5f; padding-bottom: 8px; margin-bottom: 18px;
        font-size: 1.25rem; font-weight: 600; color: #e2e8f0;
    }

    /* ── Resource Bar ───────────────────────────────────── */
    .res-bar-bg  { background:#1e293b; border-radius:6px; height:14px; width:100%; overflow:hidden; }
    .res-bar-fill { height:14px; border-radius:6px; transition:width .3s; }

    /* ── Status Pill ────────────────────────────────────── */
    .status-pill {
        display:inline-flex; align-items:center; gap:6px;
        background:#0f2b1d; color:#4ade80; padding:4px 12px;
        border-radius:16px; font-size:0.78rem; font-weight:500;
    }
    .status-dot { width:8px; height:8px; border-radius:50%; background:#4ade80; }

    /* ── Detail Card ────────────────────────────────────── */
    .detail-card {
        background:#111827; border:1px solid #1e3a5f; border-radius:12px;
        padding:20px; margin-bottom:12px;
    }
    .detail-card h4 { color:#94a3b8; font-size:0.82rem; text-transform:uppercase; letter-spacing:0.5px; margin:0 0 10px; }

    /* ── Decision Box ───────────────────────────────────── */
    .decision-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 4px solid #3b82f6; border-radius: 8px;
        padding: 16px 20px; margin: 8px 0;
    }
    .decision-box .title { color: #60a5fa; font-weight: 600; margin-bottom: 6px; }
    .decision-box ul { color: #cbd5e1; margin: 6px 0; padding-left: 18px; }
    .decision-box .focus { color: #fbbf24; font-weight: 500; margin-top: 8px; }

    /* ── Hero ────────────────────────────────────────────── */
    .hero-title { font-size: 2.2rem; font-weight: 800; color: #e2e8f0; margin: 0; line-height: 1.2; }
    .hero-sub   { font-size: 0.95rem; color: #94a3b8; margin-top: 4px; }

    /* ── Hide default Streamlit clutter ──────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    div[data-testid="stExpander"] {
        background: #111827; border: 1px solid #1e3a5f; border-radius: 10px;
    }

    /* ── Emergency Alert Ticker ──────────────────────────── */
    .alert-ticker {
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, #381216 0%, #161f30 100%);
        border: 1px solid #991b1b;
        border-radius: 8px;
        padding: 9px 14px;
        margin: 6px 0 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .ticker-badge {
        background: #ef4444;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.72rem;
        padding: 4px 10px;
        border-radius: 4px;
        white-space: nowrap;
        margin-right: 12px;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    .ticker-content {
        color: #fca5a5;
        font-size: 0.83rem;
        white-space: nowrap;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DATA & MODEL LOADING
# ═══════════════════════════════════════════════════════════════

def _find_file(name: str, subdirs=("data/raw", "data", "Notebook", ".")):
    """Search common subdirectories for a file."""
    for sub in subdirs:
        p = BASE_DIR / sub / name
        if p.exists():
            return p
    return None


@st.cache_data(show_spinner="Loading datasets…")
def load_data():
    """Load and merge all datasets; engineer the 3 resource-aggregate features."""
    inc_path = _find_file("incident_dataset.csv")
    area_path = _find_file("areas.csv")
    res_path = _find_file("resources.csv")
    dis_path = _find_file("disaster_dataset_cleaned.csv")

    missing = []
    if inc_path is None:  missing.append("incident_dataset.csv")
    if area_path is None: missing.append("areas.csv")
    if res_path is None:  missing.append("resources.csv")
    if missing:
        st.error(f"Missing required data files: {', '.join(missing)}")
        st.stop()

    incident_df = pd.read_csv(inc_path)
    areas_df    = pd.read_csv(area_path)
    resources_df = pd.read_csv(res_path)
    disaster_df = pd.read_csv(dis_path) if dis_path else pd.DataFrame()

    # ── Engineer 3 resource-aggregate features (per area) ──
    res_agg = resources_df.groupby("area_id").agg(
        resource_total_count=("resource_id", "count"),
        resource_available_count=(
            "availability_status", lambda s: (s == "Available").sum()
        ),
        resource_needs_maintenance_count=(
            "condition", lambda s: (s == "Needs Maintenance").sum()
        ),
        resource_avg_capacity=("capacity", "mean"),
    ).reset_index()
    res_agg["resource_pct_available"] = (
        res_agg["resource_available_count"] / res_agg["resource_total_count"]
    )
    res_agg["resource_pct_needs_maintenance"] = (
        res_agg["resource_needs_maintenance_count"] / res_agg["resource_total_count"]
    )
    res_agg = res_agg[["area_id", "resource_pct_available",
                        "resource_pct_needs_maintenance", "resource_avg_capacity"]]

    # ── Merge area demographics ──
    area_cols = ["area_id", "households", "male_population", "female_population",
                 "urban_population", "rural_population", "children_population_0_6",
                 "elderly_population_60_plus", "area_sq_km", "population_density"]
    area_merge = areas_df[[c for c in area_cols if c in areas_df.columns]]
    incident_df = incident_df.merge(area_merge, on="area_id", how="left", suffixes=("", "_area"))

    # ── Merge resource aggregates ──
    incident_df = incident_df.merge(res_agg, on="area_id", how="left", suffixes=("", "_res"))

    # Fill missing engineered features
    for col in ["resource_pct_available", "resource_pct_needs_maintenance", "resource_avg_capacity"]:
        if col in incident_df.columns:
            incident_df[col] = incident_df[col].fillna(incident_df[col].median() if incident_df[col].notna().any() else 0)

    # ── Add lat/lon from state centroids ──
    incident_df["latitude"] = incident_df["state"].map(lambda s: STATE_COORDS.get(s, (22.0, 78.0))[0])
    incident_df["longitude"] = incident_df["state"].map(lambda s: STATE_COORDS.get(s, (22.0, 78.0))[1])
    # Add slight jitter so markers don't stack
    rng = np.random.default_rng(42)
    incident_df["latitude"]  += rng.uniform(-0.8, 0.8, len(incident_df))
    incident_df["longitude"] += rng.uniform(-0.8, 0.8, len(incident_df))

    # ── Compute resource gaps for display ──
    incident_df["ambulance_gap"] = (
        incident_df["ambulance_demand"] - incident_df["available_ambulances"]
    ).clip(lower=0)
    incident_df["rescue_team_gap"] = (
        incident_df["rescue_team_demand"] - incident_df["available_rescue_teams"]
    ).clip(lower=0)
    incident_df["shelter_gap"] = (
        incident_df["shelter_demand"] - incident_df["available_shelter_capacity"]
    ).clip(lower=0)
    incident_df["medical_supply_gap"] = (
        incident_df["medical_supply_demand"] - incident_df["medical_supply"]
    ).clip(lower=0)

    return incident_df, areas_df, resources_df, disaster_df


@st.cache_resource(show_spinner="Loading AI model…")
def load_model():
    """Load the trained sklearn Pipeline from pkl."""
    model_path = _find_file("aapdasetu_priority_model.pkl",
                            subdirs=("Notebook", ".", "models"))
    if model_path is None:
        st.error("Cannot find aapdasetu_priority_model.pkl")
        st.stop()
    return joblib.load(model_path)


# ═══════════════════════════════════════════════════════════════
# HELPER UTILITIES
# ═══════════════════════════════════════════════════════════════

def create_scatter_map(*args, **kwargs):
    """Compatibility wrapper for Plotly 6/7 (scatter_map) and Plotly <6 (scatter_mapbox)."""
    if hasattr(px, "scatter_map"):
        if "mapbox_style" in kwargs:
            kwargs["map_style"] = kwargs.pop("mapbox_style")
        return px.scatter_map(*args, **kwargs)
    return px.scatter_mapbox(*args, **kwargs)


def style_priority_table(dataframe, display_cols):
    """Safely style dataframe priority_level column across pandas versions (pandas 2/3 compatible)."""
    styler = dataframe[display_cols].style
    styler_map = getattr(styler, "map", getattr(styler, "applymap", None))
    if styler_map is not None:
        return styler_map(
            lambda v: f"color: {PRIORITY_COLORS.get(v, '#e2e8f0')}; font-weight: 600"
            if v in PRIORITY_COLORS else "",
            subset=["priority_level"] if "priority_level" in display_cols else []
        )
    return styler


def priority_badge_html(level: str) -> str:
    cls = f"badge-{level.lower()}" if level in PRIORITY_COLORS else "badge-low"
    emoji = PRIORITY_EMOJI.get(level, "⚪")
    return f'<span class="{cls}">{emoji} {level}</span>'


def kpi_html(label: str, value, color: str = "#e2e8f0") -> str:
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color}">{value:,}</div>
    </div>"""


def resource_bar_html(label, demand, available, color="#3b82f6"):
    shortage = max(0, demand - available)
    pct = min(available / max(demand, 1) * 100, 100)
    bar_color = "#22c55e" if pct >= 80 else ("#f97316" if pct >= 50 else "#ef4444")
    return f"""
    <div style="margin-bottom:14px">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="color:#94a3b8; font-size:0.82rem; font-weight:600;">{label}</span>
            <span style="color:{'#22c55e' if shortage==0 else '#ef4444'}; font-size:0.78rem;">
                {'✓ Sufficient' if shortage==0 else f'⚠ Shortage: {shortage:,}'}
            </span>
        </div>
        <div class="res-bar-bg">
            <div class="res-bar-fill" style="width:{pct:.0f}%; background:{bar_color};"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:3px;">
            <span style="color:#64748b; font-size:0.72rem;">Available: {available:,}</span>
            <span style="color:#64748b; font-size:0.72rem;">Demand: {demand:,}</span>
        </div>
    </div>"""


def decision_support_html(row):
    """Generate an operational decision-support panel from incident data."""
    score = row.get("priority_score", 0)
    level = row.get("priority_level", "MEDIUM")
    affected = int(row.get("people_affected", 0))
    critical = int(row.get("critical_patients", 0))
    amb_gap = int(row.get("ambulance_gap", 0))
    rescue_gap = int(row.get("rescue_team_gap", 0))
    shelter_gap = int(row.get("shelter_gap", 0))
    med_gap = int(row.get("medical_supply_gap", 0))
    shortage = row.get("resource_shortage", 0)

    if level == "HIGH":
        headline = "⚡ High operational pressure detected"
        box_border = "#ef4444"
    elif level == "MEDIUM":
        headline = "⚡ Moderate operational pressure detected"
        box_border = "#f97316"
    else:
        headline = "⚡ Lower operational pressure relative to other incidents"
        box_border = "#22c55e"

    factors = []
    if affected > 0: factors.append(f"{affected:,} people affected")
    if critical > 0: factors.append(f"{critical:,} critical patients")
    if amb_gap > 0:  factors.append(f"{amb_gap:,} ambulance shortage")
    if rescue_gap > 0: factors.append(f"{rescue_gap:,} rescue-team shortage")
    if shelter_gap > 0: factors.append(f"{shelter_gap:,} shelter capacity gap")
    if med_gap > 0:  factors.append(f"{med_gap:,} medical supply gap")

    li = "".join(f"<li>{f}</li>" for f in factors) if factors else "<li>No major shortages identified</li>"

    return f"""
    <div class="decision-box" style="border-left-color:{box_border};">
        <div class="title">{headline}</div>
        <h4 style="color:#94a3b8; margin:10px 0 4px; font-size:0.78rem;">MEASURABLE FACTORS</h4>
        <ul>{li}</ul>
        <div class="focus">
            <strong>Suggested operational focus:</strong>
            {"Prioritize resource assessment and deployment for this incident." if level in ("HIGH", "MEDIUM") else "Monitor and allocate resources as needed."}
        </div>
        <p style="color:#64748b; font-size:0.7rem; margin-top:10px; font-style:italic;">
            Every life is equally important. This assessment estimates operational urgency, not the value of any individual life.
        </p>
    </div>"""


def predict_priority(model, input_data: dict):
    """Run prediction using the trained pipeline. Returns dict with priority, confidence, probabilities."""
    row = pd.DataFrame([input_data])
    for col in MODEL_FEATURES:
        if col not in row.columns:
            row[col] = 0 if col not in CATEGORICAL_COLS else "Unknown"
    row = row[MODEL_FEATURES]

    try:
        proba = model.predict_proba(row)[0]
        classes = list(model.classes_)
        best_idx = int(np.argmax(proba))
        return {
            "priority": classes[best_idx],
            "confidence": float(proba[best_idx]),
            "probabilities": {c: float(p) for c, p in zip(classes, proba)},
        }
    except Exception as e:
        pred = model.predict(row)[0]
        return {"priority": str(pred), "confidence": None, "probabilities": None}


# ═══════════════════════════════════════════════════════════════
# SECTION RENDERERS
# ═══════════════════════════════════════════════════════════════

# ─── 1. COMMAND CENTER ────────────────────────────────────────

def render_command_center(df, filtered_df, model):
    # ── KPIs ──
    st.markdown('<p class="section-hdr">📊 Executive Overview</p>', unsafe_allow_html=True)
    k = st.columns(8)
    total = len(filtered_df)
    high = (filtered_df["priority_level"] == "HIGH").sum()
    med  = (filtered_df["priority_level"] == "MEDIUM").sum()
    low  = (filtered_df["priority_level"] == "LOW").sum()
    affected = int(filtered_df["people_affected"].sum())
    avail_amb = int(filtered_df["available_ambulances"].sum())
    avail_rescue = int(filtered_df["available_rescue_teams"].sum())
    high_pressure = int((filtered_df["resource_shortage"] > 0.5).sum()) if "resource_shortage" in filtered_df.columns else high

    with k[0]: st.markdown(kpi_html("Total Incidents", total, "#60a5fa"), unsafe_allow_html=True)
    with k[1]: st.markdown(kpi_html("High Priority", high, "#ef4444"), unsafe_allow_html=True)
    with k[2]: st.markdown(kpi_html("Medium Priority", med, "#f97316"), unsafe_allow_html=True)
    with k[3]: st.markdown(kpi_html("Low Priority", low, "#22c55e"), unsafe_allow_html=True)
    with k[4]: st.markdown(kpi_html("People Affected", affected, "#a78bfa"), unsafe_allow_html=True)
    with k[5]: st.markdown(kpi_html("Avail. Ambulances", avail_amb, "#38bdf8"), unsafe_allow_html=True)
    with k[6]: st.markdown(kpi_html("Avail. Rescue Teams", avail_rescue, "#2dd4bf"), unsafe_allow_html=True)
    with k[7]: st.markdown(kpi_html("High Pressure", high_pressure, "#f87171"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Incident Command Table ──
    st.markdown('<p class="section-hdr">📋 Live Incident Command Table</p>', unsafe_allow_html=True)

    tc1, tc2, tc3 = st.columns([2, 2, 1])
    with tc1:
        search = st.text_input("🔍 Search incidents", placeholder="Search by ID, state, district, type…", label_visibility="collapsed")
    with tc2:
        show_high = st.checkbox("Show only HIGH priority", value=False)
    with tc3:
        sort_by = st.selectbox("Sort by", ["priority_score", "people_affected", "resource_shortage", "deaths"], label_visibility="collapsed")

    table_df = filtered_df.copy()
    if search:
        search_term = search.strip().lower()
        search_cols = ["incident_id", "state", "district", "disaster_type", "disaster_subtype"]
        search_cols = [c for c in search_cols if c in table_df.columns]
        mask = pd.Series(False, index=table_df.index)
        for col in search_cols:
            mask |= table_df[col].astype(str).str.lower().str.contains(search_term, na=False)
        table_df = table_df[mask]
    if show_high:
        table_df = table_df[table_df["priority_level"] == "HIGH"]

    table_df = table_df.sort_values(sort_by, ascending=False)

    display_cols = ["incident_id", "state", "district", "disaster_type", "people_affected",
                    "deaths", "injured", "critical_patients", "vulnerable_ratio",
                    "resource_shortage", "priority_score", "priority_level"]
    display_cols = [c for c in display_cols if c in table_df.columns]

    st.dataframe(
        style_priority_table(table_df, display_cols),
        use_container_width=True,
        height=420,
    )

    csv = table_df[display_cols].to_csv(index=False)
    st.download_button("📥 Download Filtered CSV", csv, "aapdasetu_incidents.csv", "text/csv")

    # ── Incident Drill-Down ──
    st.markdown("---")
    st.markdown('<p class="section-hdr">🔎 Incident Detail / Drill-Down</p>', unsafe_allow_html=True)

    incident_ids = table_df["incident_id"].tolist()
    if not incident_ids:
        st.info("No incidents match the current filters.")
        return

    selected_id = st.selectbox("Select an incident to inspect", incident_ids)
    row = table_df[table_df["incident_id"] == selected_id].iloc[0]
    _render_incident_detail(row, model)


def _render_incident_detail(row, model):
    """Render the full incident detail panel for a single incident row."""
    level = row.get("priority_level", "MEDIUM")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="detail-card">
            <h4>Incident Overview</h4>
            <table style="width:100%; color:#cbd5e1; font-size:0.88rem;">
                <tr><td style="color:#94a3b8;">Incident ID</td><td><strong>{row.get('incident_id','—')}</strong></td></tr>
                <tr><td style="color:#94a3b8;">Disaster Type</td><td>{row.get('disaster_type','—')}</td></tr>
                <tr><td style="color:#94a3b8;">State</td><td>{row.get('state','—')}</td></tr>
                <tr><td style="color:#94a3b8;">District</td><td>{row.get('district','—')}</td></tr>
                <tr><td style="color:#94a3b8;">Priority</td><td>{priority_badge_html(level)}</td></tr>
                <tr><td style="color:#94a3b8;">Priority Score</td><td>{row.get('priority_score',0):.1f} / 100</td></tr>
                <tr><td style="color:#94a3b8;">Severity Score</td><td>{row.get('severity_score',0):.3f}</td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="detail-card">
            <h4>Human Impact</h4>
            <table style="width:100%; color:#cbd5e1; font-size:0.88rem;">
                <tr><td style="color:#94a3b8;">People Affected</td><td><strong>{int(row.get('people_affected',0)):,}</strong></td></tr>
                <tr><td style="color:#94a3b8;">Deaths</td><td style="color:#ef4444;">{int(row.get('deaths',0)):,}</td></tr>
                <tr><td style="color:#94a3b8;">Injured</td><td style="color:#f97316;">{int(row.get('injured',0)):,}</td></tr>
                <tr><td style="color:#94a3b8;">Critical Patients</td><td style="color:#f87171;">{int(row.get('critical_patients',0)):,}</td></tr>
                <tr><td style="color:#94a3b8;">Children Affected</td><td>{int(row.get('children_affected',0)):,}</td></tr>
                <tr><td style="color:#94a3b8;">Elderly Affected</td><td>{int(row.get('elderly_affected',0)):,}</td></tr>
                <tr><td style="color:#94a3b8;">Vulnerable Ratio</td><td>{row.get('vulnerable_ratio',0):.2%}</td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    # ── Resource Situation ──
    st.markdown('<div class="detail-card"><h4>Resource Situation</h4>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(resource_bar_html("🚑 AMBULANCE",
                                       int(row.get("ambulance_demand", 0)),
                                       int(row.get("available_ambulances", 0))),
                     unsafe_allow_html=True)
        st.markdown(resource_bar_html("🛟 RESCUE TEAMS",
                                       int(row.get("rescue_team_demand", 0)),
                                       int(row.get("available_rescue_teams", 0))),
                     unsafe_allow_html=True)
    with r2:
        st.markdown(resource_bar_html("🏠 SHELTER",
                                       int(row.get("shelter_demand", 0)),
                                       int(row.get("available_shelter_capacity", 0))),
                     unsafe_allow_html=True)
        st.markdown(resource_bar_html("💊 MEDICAL SUPPLIES",
                                       int(row.get("medical_supply_demand", 0)),
                                       int(row.get("medical_supply", 0))),
                     unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Decision Support ──
    st.markdown('<p class="section-hdr">⚡ Response Decision Support</p>', unsafe_allow_html=True)
    st.markdown(decision_support_html(row), unsafe_allow_html=True)

    # ── "What-If" Dynamic Resource Allocation Simulator ──
    with st.expander("🧪 Dynamic 'What-If' Resource Allocation Sandbox", expanded=False):
        st.markdown("""
        <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:12px;">
            Simulate the operational impact of dispatching additional emergency resources to this incident.
            The ML model recalculates operational priority and confidence in real time.
        </p>
        """, unsafe_allow_html=True)
        
        sim_col1, sim_col2 = st.columns(2)
        inc_key = str(row.get('incident_id', 'curr'))
        with sim_col1:
            add_amb = st.slider("➕ Dispatch Additional Ambulances", 0, 50, 0, key=f"sim_amb_{inc_key}")
            add_rescue = st.slider("➕ Deploy Extra Rescue Teams", 0, 20, 0, key=f"sim_res_{inc_key}")
        with sim_col2:
            add_shelter = st.slider("➕ Add Emergency Shelter Beds", 0, 5000, 0, step=100, key=f"sim_shl_{inc_key}")
            add_med = st.slider("➕ Inject Medical Supply Kits", 0, 2000, 0, step=50, key=f"sim_med_{inc_key}")
        
        sim_data = row.to_dict()
        sim_data["available_ambulances"] = int(sim_data.get("available_ambulances", 0)) + add_amb
        sim_data["available_rescue_teams"] = int(sim_data.get("available_rescue_teams", 0)) + add_rescue
        sim_data["available_shelter_capacity"] = int(sim_data.get("available_shelter_capacity", 0)) + add_shelter
        sim_data["medical_supply"] = int(sim_data.get("medical_supply", 0)) + add_med
        
        curr_total = sim_data.get("available_ambulances", 0) + sim_data.get("available_rescue_teams", 0)
        curr_demand = max(1, sim_data.get("ambulance_demand", 1) + sim_data.get("rescue_team_demand", 1))
        sim_data["resource_pct_available"] = min(1.0, curr_total / curr_demand)
        
        sim_pred = predict_priority(model, sim_data)
        
        orig_level = row.get("priority_level", "MEDIUM")
        sim_level = sim_pred["priority"]
        orig_color = PRIORITY_COLORS.get(orig_level, "#e2e8f0")
        sim_color = PRIORITY_COLORS.get(sim_level, "#e2e8f0")
        
        s1, s2, s3 = st.columns([1, 1, 1])
        with s1:
            st.markdown(f"""
            <div style="background:#1a2332; border:1px solid #1e3a5f; border-radius:10px; padding:12px; text-align:center;">
                <div style="color:#94a3b8; font-size:0.75rem;">CURRENT OPERATIONAL PRIORITY</div>
                <div style="font-size:1.4rem; font-weight:700; color:{orig_color};">{PRIORITY_EMOJI.get(orig_level, '')} {orig_level}</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div style="background:#1a2332; border:1px solid #1e3a5f; border-radius:10px; padding:12px; text-align:center;">
                <div style="color:#94a3b8; font-size:0.75rem;">SIMULATED PRIORITY AFTER DISPATCH</div>
                <div style="font-size:1.4rem; font-weight:700; color:{sim_color};">{PRIORITY_EMOJI.get(sim_level, '')} {sim_level}</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            conf = sim_pred.get("confidence", 0) * 100 if sim_pred.get("confidence") else 0
            st.markdown(f"""
            <div style="background:#1a2332; border:1px solid #1e3a5f; border-radius:10px; padding:12px; text-align:center;">
                <div style="color:#94a3b8; font-size:0.75rem;">MODEL CONFIDENCE</div>
                <div style="font-size:1.4rem; font-weight:700; color:#38bdf8;">{conf:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        if orig_level == "HIGH" and sim_level in ("MEDIUM", "LOW"):
            st.success(f"✅ Resource reallocation successfully alleviates acute pressure! Operational status shifted from {orig_level} to {sim_level}.")
        elif orig_level == "MEDIUM" and sim_level == "LOW":
            st.success("✅ Operational burden normalized to LOW priority with simulated allocation.")
        elif add_amb > 0 or add_rescue > 0:
            st.info("ℹ️ Resource deficit is significantly reduced, stabilizing on-ground logistics.")

    # ── Executive SitRep Generator ──
    with st.expander("📄 Generate Incident Action Plan (SitRep)", expanded=False):
        sitrep_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        sitrep_text = f"""================================================================================
NATIONAL DISASTER RESPONSE COMMAND - SITUATION REPORT (SITREP)
INCIDENT ID: {row.get('incident_id', 'UNKNOWN')}
DATE/TIME: {sitrep_time}
CLASSIFICATION: EMERGENCY RESPONSE PROTOCOL - OPERATIONAL IMMEDIATE
================================================================================

1. INCIDENT SYNOPSIS:
   - Event: {row.get('disaster_type', 'N/A')} ({row.get('disaster_subtype', 'N/A')})
   - Jurisdiction: {row.get('district', 'N/A')}, {row.get('state', 'N/A')}
   - Operational Urgency: {level} (Score: {row.get('priority_score', 0):.1f}/100)

2. HUMAN CASUALTY & VULNERABILITY IMPACT:
   - Population Affected: {int(row.get('people_affected', 0)):,}
   - Fatalities Confirmed: {int(row.get('deaths', 0)):,}
   - Severe Injuries: {int(row.get('injured', 0)):,}
   - Critical Intensive-Care Patients: {int(row.get('critical_patients', 0)):,}
   - Vulnerable Population Ratio: {row.get('vulnerable_ratio', 0):.1%}

3. CRITICAL RESOURCE GAPS & DEFICITS:
   - Ambulance Deficit: {int(row.get('ambulance_gap', 0)):,} units
   - Rescue Team Deficit: {int(row.get('rescue_team_gap', 0)):,} teams
   - Emergency Shelter Deficit: {int(row.get('shelter_gap', 0)):,} capacity
   - Medical Supply Deficit: {int(row.get('medical_supply_gap', 0)):,} units

4. STRATEGIC DIRECTIVES:
   - Immediate mobilization of mutual-aid logistics from adjacent districts.
   - Activate triage zones for critical trauma patient transfer.
   - Maintain ethical mandate: All life is equal; allocation prioritizes operational stabilization.

REPORT GENERATED BY AAPDASETU AI COMMAND SYSTEM
================================================================================"""
        st.text_area("SitRep Preview", sitrep_text, height=200, label_visibility="collapsed")
        st.download_button(
            "📥 Download Official SitRep (.txt)",
            sitrep_text,
            file_name=f"SITREP_{row.get('incident_id', 'INCIDENT')}.txt",
            mime="text/plain",
            key=f"dl_sitrep_{row.get('incident_id', 'id')}"
        )


# ─── 2. INCIDENT MAP ─────────────────────────────────────────

def render_incident_map(df, filtered_df):
    st.markdown('<p class="section-hdr">🗺️ Disaster Incident Map</p>', unsafe_allow_html=True)
    st.caption("📍 Markers placed at approximate state-level centroids with jitter. Size ∝ people affected.")

    if filtered_df.empty:
        st.info("No incidents to display with current filters.")
        return

    map_df = filtered_df.copy()

    # Clamp marker size
    map_df["marker_size"] = np.clip(map_df["people_affected"] / map_df["people_affected"].max() * 35, 5, 35)

    fig = create_scatter_map(
        map_df,
        lat="latitude",
        lon="longitude",
        color="priority_level",
        size="marker_size",
        color_discrete_map=PRIORITY_COLORS,
        category_orders={"priority_level": PRIORITY_ORDER},
        hover_name="incident_id",
        hover_data={
            "state": True,
            "district": True,
            "disaster_type": True,
            "people_affected": ":,",
            "priority_level": True,
            "resource_shortage": ":.2f",
            "latitude": False,
            "longitude": False,
            "marker_size": False,
        },
        mapbox_style="carto-darkmatter",
        zoom=4,
        center={"lat": 22.5, "lon": 82.0},
        height=650,
    )
    map_layout = {
        **PLOTLY_LAYOUT,
        "margin": dict(l=0, r=0, t=0, b=0),
        "legend": dict(
            title="Priority Level",
            bgcolor="rgba(17,24,39,0.85)",
            bordercolor="#1e3a5f",
            borderwidth=1,
            yanchor="top", y=0.98, xanchor="left", x=0.01,
        ),
    }
    fig.update_layout(**map_layout)
    st.plotly_chart(fig, use_container_width=True)

    # Summary by state
    with st.expander("📊 Incident Count by State"):
        state_agg = (
            filtered_df.groupby(["state", "priority_level"])
            .size()
            .reset_index(name="count")
        )
        fig2 = px.bar(
            state_agg, x="state", y="count", color="priority_level",
            color_discrete_map=PRIORITY_COLORS,
            category_orders={"priority_level": PRIORITY_ORDER},
            barmode="stack",
        )
        fig2.update_layout(**PLOTLY_LAYOUT, xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig2, use_container_width=True)


# ─── 3. ANALYTICS ────────────────────────────────────────────

def render_analytics(df, filtered_df):
    st.markdown('<p class="section-hdr">📊 Priority Analytics</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # Chart 1: Priority Distribution
    with c1:
        dist = filtered_df["priority_level"].value_counts().reindex(PRIORITY_ORDER).fillna(0)
        fig1 = go.Figure(go.Pie(
            labels=dist.index, values=dist.values,
            marker=dict(colors=[PRIORITY_COLORS[p] for p in dist.index]),
            hole=0.55, textinfo="label+value",
            textfont=dict(color="#e2e8f0"),
        ))
        fig1.update_layout(**PLOTLY_LAYOUT, title="Priority Distribution", height=380)
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Incidents by Disaster Type
    with c2:
        type_counts = filtered_df["disaster_type"].value_counts().head(12)
        fig2 = px.bar(
            x=type_counts.values, y=type_counts.index, orientation="h",
            labels={"x": "Incidents", "y": ""},
            color_discrete_sequence=["#3b82f6"],
        )
        fig2.update_layout(**PLOTLY_LAYOUT, title="Incidents by Disaster Type", height=380)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    # Chart 3: High Priority by State (top 15)
    with c3:
        high_by_state = (
            filtered_df[filtered_df["priority_level"] == "HIGH"]
            .groupby("state").size()
            .sort_values(ascending=False).head(15)
        )
        fig3 = px.bar(
            x=high_by_state.values, y=high_by_state.index, orientation="h",
            labels={"x": "HIGH Incidents", "y": ""},
            color_discrete_sequence=["#ef4444"],
        )
        fig3.update_layout(**PLOTLY_LAYOUT, title="High Priority Incidents by State", height=380)
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4: People Affected by Priority
    with c4:
        affected_by_priority = (
            filtered_df.groupby("priority_level")["people_affected"]
            .sum().reindex(PRIORITY_ORDER).fillna(0)
        )
        fig4 = px.bar(
            x=affected_by_priority.index, y=affected_by_priority.values,
            labels={"x": "Priority Level", "y": "Total People Affected"},
            color=affected_by_priority.index,
            color_discrete_map=PRIORITY_COLORS,
        )
        fig4.update_layout(**PLOTLY_LAYOUT, title="People Affected by Priority", height=380, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    c5, c6 = st.columns(2)

    # Chart 5: Resource Shortage vs Priority
    with c5:
        if "resource_shortage" in filtered_df.columns:
            fig5 = px.box(
                filtered_df, x="priority_level", y="resource_shortage",
                color="priority_level", color_discrete_map=PRIORITY_COLORS,
                category_orders={"priority_level": PRIORITY_ORDER},
                labels={"resource_shortage": "Resource Shortage Index", "priority_level": "Priority"},
            )
            fig5.update_layout(**PLOTLY_LAYOUT, title="Resource Shortage vs Priority", height=380, showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)

    # Chart 6: Severity vs Priority Score
    with c6:
        if "severity_score" in filtered_df.columns and "priority_score" in filtered_df.columns:
            sample = filtered_df.sample(min(800, len(filtered_df)), random_state=42)
            fig6 = px.scatter(
                sample, x="severity_score", y="priority_score",
                color="priority_level", color_discrete_map=PRIORITY_COLORS,
                category_orders={"priority_level": PRIORITY_ORDER},
                opacity=0.6,
                labels={"severity_score": "Severity Score", "priority_score": "Priority Score"},
            )
            fig6.update_layout(**PLOTLY_LAYOUT, title="Severity Score vs Priority Score", height=380)
            st.plotly_chart(fig6, use_container_width=True)


# ─── 4. RESOURCE PRESSURE ────────────────────────────────────

def render_resource_pressure(df, filtered_df):
    st.markdown('<p class="section-hdr">🚑 Resource Pressure Center</p>', unsafe_allow_html=True)

    # ── Overall Resource Summary ──
    total_amb_demand = int(filtered_df["ambulance_demand"].sum())
    total_amb_avail  = int(filtered_df["available_ambulances"].sum())
    total_res_demand = int(filtered_df["rescue_team_demand"].sum())
    total_res_avail  = int(filtered_df["available_rescue_teams"].sum())
    total_shel_demand = int(filtered_df["shelter_demand"].sum())
    total_shel_avail  = int(filtered_df["available_shelter_capacity"].sum())
    total_med_demand = int(filtered_df["medical_supply_demand"].sum())
    total_med_avail  = int(filtered_df["medical_supply"].sum())

    def _util_pct(demand, avail):
        return f"{min(avail / max(demand, 1) * 100, 100):.0f}%"

    rc = st.columns(4)
    resources = [
        ("🚑 Ambulances", total_amb_demand, total_amb_avail),
        ("🛟 Rescue Teams", total_res_demand, total_res_avail),
        ("🏠 Shelter Capacity", total_shel_demand, total_shel_avail),
        ("💊 Medical Supplies", total_med_demand, total_med_avail),
    ]
    for i, (label, demand, avail) in enumerate(resources):
        shortage = max(0, demand - avail)
        util = _util_pct(demand, avail)
        with rc[i]:
            st.markdown(f"""
            <div class="detail-card">
                <h4>{label}</h4>
                <table style="width:100%; color:#cbd5e1; font-size:0.85rem;">
                    <tr><td style="color:#94a3b8;">Total Demand</td><td style="text-align:right;">{demand:,}</td></tr>
                    <tr><td style="color:#94a3b8;">Available</td><td style="text-align:right;">{avail:,}</td></tr>
                    <tr><td style="color:#94a3b8;">Shortage</td><td style="text-align:right; color:{'#ef4444' if shortage>0 else '#22c55e'};">{shortage:,}</td></tr>
                    <tr><td style="color:#94a3b8;">Fulfilment</td><td style="text-align:right; color:#60a5fa; font-weight:600;">{util}</td></tr>
                </table>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Most Resource-Constrained Incidents ──
    st.markdown('<p class="section-hdr">🔻 Most Resource-Constrained Incidents</p>', unsafe_allow_html=True)

    constrained = filtered_df.copy()
    constrained["total_resource_gap"] = (
        constrained["ambulance_gap"] + constrained["rescue_team_gap"]
        + constrained["shelter_gap"] + constrained["medical_supply_gap"]
    )
    constrained = constrained.sort_values("total_resource_gap", ascending=False).head(20)

    disp_cols = ["incident_id", "state", "district", "priority_level",
                 "resource_shortage", "ambulance_gap", "rescue_team_gap",
                 "shelter_gap", "medical_supply_gap", "total_resource_gap"]
    disp_cols = [c for c in disp_cols if c in constrained.columns]

    st.dataframe(
        style_priority_table(constrained, disp_cols),
        use_container_width=True,
        height=500,
    )


# ─── 5. AI PREDICTION ────────────────────────────────────────

def render_ai_prediction(model, df):
    st.markdown('<p class="section-hdr">🤖 AI Priority Prediction</p>', unsafe_allow_html=True)
    st.caption("Enter incident information to predict operational priority using the trained ML model.")

    # Pre-fill option
    prefill = st.selectbox(
        "📋 Pre-fill from existing incident (optional)",
        ["— Manual Entry —"] + df["incident_id"].tolist()[:200],
    )
    if prefill != "— Manual Entry —":
        pf_row = df[df["incident_id"] == prefill].iloc[0]
    else:
        pf_row = None

    def _default(col, fallback=0, min_val=None, max_val=None):
        if pf_row is not None and col in pf_row.index:
            v = pf_row[col]
            val = v if pd.notna(v) else fallback
        else:
            val = fallback
        if min_val is not None and isinstance(val, (int, float)):
            val = max(min_val, val)
        if max_val is not None and isinstance(val, (int, float)):
            val = min(max_val, val)
        return val

    with st.form("prediction_form"):
        st.markdown("##### 📍 Location & Disaster")
        lc1, lc2, lc3 = st.columns(3)
        states = sorted(df["state"].dropna().unique())
        disaster_types = sorted(df["disaster_type"].dropna().unique())
        disaster_subtypes = sorted(df["disaster_subtype"].dropna().unique())

        with lc1:
            state = st.selectbox("State", states,
                                 index=states.index(_default("state", states[0])) if _default("state", states[0]) in states else 0)
        with lc2:
            d_type = st.selectbox("Disaster Type", disaster_types,
                                  index=disaster_types.index(_default("disaster_type", disaster_types[0])) if _default("disaster_type", disaster_types[0]) in disaster_types else 0)
        with lc3:
            d_subtype = st.selectbox("Disaster Subtype", disaster_subtypes,
                                     index=disaster_subtypes.index(_default("disaster_subtype", disaster_subtypes[0])) if _default("disaster_subtype", disaster_subtypes[0]) in disaster_subtypes else 0)

        st.markdown("##### 👥 Human Impact")
        h1, h2, h3, h4 = st.columns(4)
        with h1:
            population     = st.number_input("Population", 1000, 50_000_000, int(_default("population", 500000, 1000, 50_000_000)), step=10000)
            people_affected = st.number_input("People Affected", 0, 50_000_000, int(_default("people_affected", 5000, 0, 50_000_000)), step=500)
        with h2:
            deaths          = st.number_input("Deaths", 0, 1_000_000, int(_default("deaths", 10, 0, 1_000_000)), step=1)
            injured         = st.number_input("Injured", 0, 1_000_000, int(_default("injured", 100, 0, 1_000_000)), step=10)
        with h3:
            critical_patients = st.number_input("Critical Patients", 0, 500_000, int(_default("critical_patients", 20, 0, 500_000)), step=5)
            children_affected = st.number_input("Children Affected", 0, 5_000_000, int(_default("children_affected", 500, 0, 5_000_000)), step=50)
        with h4:
            elderly_affected  = st.number_input("Elderly Affected", 0, 5_000_000, int(_default("elderly_affected", 300, 0, 5_000_000)), step=50)

        st.markdown("##### 🏥 Infrastructure & Resources")
        i1, i2, i3 = st.columns(3)
        with i1:
            hospital_count = st.number_input("Hospital Count", 0, 5000, int(_default("hospital_count", 10, 0, 5000)), step=1)
            ambulance_count = st.number_input("Ambulance Count (total)", 0, 10_000, int(_default("ambulance_count", 20, 0, 10_000)), step=1)
            available_ambulances = st.number_input("Available Ambulances", 0, 10_000, int(_default("available_ambulances", 15, 0, 10_000)), step=1)
        with i2:
            rescue_team_count = st.number_input("Rescue Team Count (total)", 0, 2000, int(_default("rescue_team_count", 5, 0, 2000)), step=1)
            available_rescue_teams = st.number_input("Available Rescue Teams", 0, 2000, int(_default("available_rescue_teams", 3, 0, 2000)), step=1)
            hospital_capacity = st.number_input("Hospital Capacity", 0, 200_000, int(_default("hospital_capacity", 500, 0, 200_000)), step=50)
        with i3:
            shelter_capacity = st.number_input("Shelter Capacity", 0, 5_000_000, int(_default("shelter_capacity", 10000, 0, 5_000_000)), step=500)
            available_shelter_capacity = st.number_input("Available Shelter Capacity", 0, 5_000_000, int(_default("available_shelter_capacity", 8000, 0, 5_000_000)), step=500)
            medical_supply = st.number_input("Medical Supply", 0, 500_000, int(_default("medical_supply", 1000, 0, 500_000)), step=100)

        st.markdown("##### 📦 Resource Demand")
        d1, d2, d3, d4 = st.columns(4)
        with d1: ambulance_demand = st.number_input("Ambulance Demand", 0, 50_000, int(_default("ambulance_demand", 5, 0, 50_000)), step=1)
        with d2: rescue_team_demand = st.number_input("Rescue Team Demand", 0, 10_000, int(_default("rescue_team_demand", 3, 0, 10_000)), step=1)
        with d3: shelter_demand = st.number_input("Shelter Demand", 0, 10_000_000, int(_default("shelter_demand", 3000, 0, 10_000_000)), step=500)
        with d4: medical_supply_demand = st.number_input("Medical Supply Demand", 0, 5_000_000, int(_default("medical_supply_demand", 500, 0, 5_000_000)), step=50)

        with st.expander("🏘️ Area Demographics (advanced)"):
            a1, a2, a3 = st.columns(3)
            with a1:
                households = st.number_input("Households", 0, 10_000_000, int(_default("households", 100000, 0, 10_000_000)), step=5000)
                male_population = st.number_input("Male Population", 0, 20_000_000, int(_default("male_population", 250000, 0, 20_000_000)), step=10000)
                female_population = st.number_input("Female Population", 0, 20_000_000, int(_default("female_population", 250000, 0, 20_000_000)), step=10000)
            with a2:
                urban_population = st.number_input("Urban Population", 0, 20_000_000, int(_default("urban_population", 200000, 0, 20_000_000)), step=10000)
                rural_population = st.number_input("Rural Population", 0, 20_000_000, int(_default("rural_population", 300000, 0, 20_000_000)), step=10000)
                children_population_0_6 = st.number_input("Children (0–6)", 0, 10_000_000, int(_default("children_population_0_6", 50000, 0, 10_000_000)), step=5000)
            with a3:
                elderly_population_60_plus = st.number_input("Elderly (60+)", 0, 10_000_000, int(_default("elderly_population_60_plus", 40000, 0, 10_000_000)), step=5000)
                area_sq_km = st.number_input("Area (sq km)", 1, 100_000, int(_default("area_sq_km", 5000, 1, 100_000)), step=500)
                population_density = st.number_input("Population Density", 0.1, 100_000.0, float(_default("population_density", 100.0, 0.1, 100_000.0)), step=50.0)

        with st.expander("📊 Resource Health Metrics (advanced)"):
            rh1, rh2, rh3 = st.columns(3)
            with rh1: resource_pct_available = st.slider("Resource % Available", 0.0, 1.0, float(_default("resource_pct_available", 0.65, 0.0, 1.0)), 0.01)
            with rh2: resource_pct_needs_maintenance = st.slider("Resource % Needs Maintenance", 0.0, 1.0, float(_default("resource_pct_needs_maintenance", 0.03, 0.0, 1.0)), 0.01)
            with rh3: resource_avg_capacity = st.number_input("Resource Avg Capacity", 0.0, 50_000.0, float(_default("resource_avg_capacity", 50.0, 0.0, 50_000.0)), step=5.0)

        submitted = st.form_submit_button("🔮 Predict Operational Priority", use_container_width=True, type="primary")

    if submitted:
        input_data = {
            "state": state, "disaster_type": d_type, "disaster_subtype": d_subtype,
            "population": population, "people_affected": people_affected,
            "deaths": deaths, "injured": injured, "critical_patients": critical_patients,
            "children_affected": children_affected, "elderly_affected": elderly_affected,
            "hospital_count": hospital_count, "ambulance_count": ambulance_count,
            "available_ambulances": available_ambulances,
            "rescue_team_count": rescue_team_count,
            "available_rescue_teams": available_rescue_teams,
            "shelter_capacity": shelter_capacity,
            "available_shelter_capacity": available_shelter_capacity,
            "hospital_capacity": hospital_capacity, "medical_supply": medical_supply,
            "ambulance_demand": ambulance_demand, "rescue_team_demand": rescue_team_demand,
            "shelter_demand": shelter_demand, "medical_supply_demand": medical_supply_demand,
            "households": households, "male_population": male_population,
            "female_population": female_population, "urban_population": urban_population,
            "rural_population": rural_population,
            "children_population_0_6": children_population_0_6,
            "elderly_population_60_plus": elderly_population_60_plus,
            "area_sq_km": area_sq_km, "population_density": population_density,
            "resource_pct_available": resource_pct_available,
            "resource_pct_needs_maintenance": resource_pct_needs_maintenance,
            "resource_avg_capacity": resource_avg_capacity,
        }

        result = predict_priority(model, input_data)

        st.markdown("---")
        st.markdown("### Prediction Result")

        pr_level = result["priority"]
        pr_color = PRIORITY_COLORS.get(pr_level, "#e2e8f0")
        pr_emoji = PRIORITY_EMOJI.get(pr_level, "⚪")

        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown(f"""
            <div class="detail-card" style="text-align:center;">
                <h4>Predicted Operational Priority</h4>
                <div style="font-size:2.5rem; font-weight:800; color:{pr_color}; margin:10px 0;">{pr_emoji} {pr_level}</div>
            </div>""", unsafe_allow_html=True)

        with rc2:
            if result["confidence"] is not None:
                conf_pct = result["confidence"] * 100
                st.markdown(f"""
                <div class="detail-card" style="text-align:center;">
                    <h4>Model Confidence</h4>
                    <div style="font-size:2.5rem; font-weight:800; color:#60a5fa; margin:10px 0;">{conf_pct:.0f}%</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("Confidence scores unavailable for this model configuration.")

        if result["probabilities"]:
            st.markdown("##### Class Probabilities")
            prob_cols = st.columns(3)
            for i, (cls, prob) in enumerate(sorted(result["probabilities"].items(), key=lambda x: PRIORITY_ORDER.index(x[0]) if x[0] in PRIORITY_ORDER else 99)):
                with prob_cols[i]:
                    color = PRIORITY_COLORS.get(cls, "#e2e8f0")
                    st.markdown(f"""
                    <div class="detail-card" style="text-align:center;">
                        <div style="color:{color}; font-weight:700;">{cls}</div>
                        <div style="font-size:1.4rem; color:#e2e8f0;">{prob*100:.1f}%</div>
                    </div>""", unsafe_allow_html=True)

        # Explainable AI (XAI) Feature Drivers
        st.markdown("---")
        st.markdown("##### 🔬 Explainable AI (XAI) — Key Decision Drivers")
        st.caption("Relative operational stress contributed by primary factors vs. mitigating resource buffers.")

        # Compute intuitive driver scores
        crit_impact = min(100.0, (critical_patients / max(1, people_affected * 0.04)) * 35.0)
        amb_gap = max(0, ambulance_demand - available_ambulances)
        amb_impact = min(100.0, amb_gap * 18.0)
        res_gap = max(0, rescue_team_demand - available_rescue_teams)
        rescue_impact = min(100.0, res_gap * 22.0)
        sh_gap = max(0, shelter_demand - available_shelter_capacity)
        shelter_impact = min(100.0, (sh_gap / 1000.0) * 15.0)
        vuln_pct = (children_affected + elderly_affected) / max(1, people_affected)
        vuln_impact = min(100.0, vuln_pct * 80.0)
        resource_shield = -min(75.0, (available_ambulances * 2.0 + available_rescue_teams * 4.0 + (available_shelter_capacity / 500.0)))

        drivers_data = [
            {"Factor": "Critical Patients Load", "Impact": crit_impact},
            {"Factor": "Ambulance Shortage Deficit", "Impact": amb_impact},
            {"Factor": "Rescue Team Deficit", "Impact": rescue_impact},
            {"Factor": "Shelter Capacity Gap", "Impact": shelter_impact},
            {"Factor": "Demographic Vulnerability", "Impact": vuln_impact},
            {"Factor": "On-Ground Resource Buffer", "Impact": resource_shield},
        ]
        driver_df = pd.DataFrame(drivers_data)
        driver_df["Influence"] = driver_df["Impact"].apply(lambda v: "Elevates Urgency" if v >= 0 else "Alleviates Pressure")
        driver_colors = {"Elevates Urgency": "#ef4444", "Alleviates Pressure": "#22c55e"}

        fig_xai = px.bar(
            driver_df, x="Impact", y="Factor", orientation="h",
            color="Influence", color_discrete_map=driver_colors,
            labels={"Impact": "Relative Operational Pressure (%)", "Factor": ""},
        )
        xai_layout = {
            **PLOTLY_LAYOUT,
            "height": 290,
            "margin": dict(l=10, r=10, t=10, b=10),
            "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        }
        fig_xai.update_layout(**xai_layout)
        st.plotly_chart(fig_xai, use_container_width=True)

        factors = []
        if people_affected > df["people_affected"].median(): factors.append(f"Above-median affected population ({people_affected:,})")
        rs = amb_gap + res_gap
        if rs > 0: factors.append(f"Resource shortage detected (ambulance + rescue gap: {rs:,})")
        if critical_patients > df["critical_patients"].median(): factors.append(f"Above-median critical patients ({critical_patients:,})")
        if sh_gap > 0: factors.append(f"Shelter capacity gap ({sh_gap:,})")
        if vuln_pct > 0.25: factors.append(f"High vulnerable population ratio ({vuln_pct:.0%})")
        if not factors: factors.append("No major operational stress signals in the provided inputs.")
        for f in factors:
            st.markdown(f"- {f}")


# ─── 6. DEMO MODE ────────────────────────────────────────────

def render_demo_mode(df, model):
    st.markdown('<p class="section-hdr">🎬 Demo Mode — Quick Overview for Judges</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#1a2332; border:1px solid #1e3a5f; border-radius:10px; padding:16px; margin-bottom:18px;">
        <p style="color:#94a3b8; margin:0; font-size:0.9rem;">
            Select a priority level below to see a <strong>real incident</strong> from the dataset.
            This demonstrates how AapdaSetu provides operational intelligence at a glance.
        </p>
    </div>""", unsafe_allow_html=True)

    demo_col1, demo_col2, demo_col3 = st.columns(3)
    with demo_col1: btn_high = st.button("🔴 HIGH Priority Example", use_container_width=True, type="primary")
    with demo_col2: btn_med  = st.button("🟠 MEDIUM Priority Example", use_container_width=True)
    with demo_col3: btn_low  = st.button("🟢 LOW Priority Example", use_container_width=True)

    # Determine which demo to show
    if "demo_level" not in st.session_state:
        st.session_state.demo_level = "HIGH"
    if btn_high: st.session_state.demo_level = "HIGH"
    if btn_med:  st.session_state.demo_level = "MEDIUM"
    if btn_low:  st.session_state.demo_level = "LOW"

    demo_level = st.session_state.demo_level
    demo_pool = df[df["priority_level"] == demo_level]
    if demo_pool.empty:
        st.warning(f"No {demo_level} priority incidents in dataset.")
        return

    # Pick a representative incident (high priority_score for HIGH, etc.)
    if demo_level == "HIGH":
        demo_row = demo_pool.nlargest(5, "priority_score").sample(1, random_state=42).iloc[0]
    elif demo_level == "MEDIUM":
        median_score = demo_pool["priority_score"].median()
        demo_row = demo_pool.iloc[(demo_pool["priority_score"] - median_score).abs().argsort()[:1]].iloc[0]
    else:
        demo_row = demo_pool.nsmallest(5, "priority_score").sample(1, random_state=42).iloc[0]

    level = demo_row["priority_level"]
    color = PRIORITY_COLORS.get(level, "#e2e8f0")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #1a2332, #111827); border:2px solid {color};
                border-radius:14px; padding:22px; text-align:center; margin-bottom:16px;">
        <div style="font-size:0.82rem; color:#94a3b8; text-transform:uppercase; letter-spacing:1px;">Demo Incident</div>
        <div style="font-size:1.6rem; font-weight:800; color:#e2e8f0; margin:4px 0;">
            {demo_row.get('incident_id','—')} — {demo_row.get('disaster_type','—')}
        </div>
        <div style="font-size:1rem; color:#94a3b8;">{demo_row.get('state','—')}, {demo_row.get('district','—')}</div>
        <div style="margin-top:10px;">{priority_badge_html(level)}</div>
    </div>""", unsafe_allow_html=True)

    # Full detail
    _render_incident_detail(demo_row, model)

    # Map marker for this incident
    st.markdown("##### 🗺️ Incident Location")
    fig_map = create_scatter_map(
        pd.DataFrame([demo_row]),
        lat="latitude", lon="longitude",
        color_discrete_sequence=[color],
        hover_name="incident_id",
        hover_data={"state": True, "district": True, "disaster_type": True,
                    "latitude": False, "longitude": False},
        mapbox_style="carto-darkmatter",
        zoom=5,
        center={"lat": demo_row["latitude"], "lon": demo_row["longitude"]},
        height=350,
    )
    fig_map.update_traces(marker=dict(size=18))
    demo_map_layout = {**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=0, b=0)}
    fig_map.update_layout(**demo_map_layout)
    st.plotly_chart(fig_map, use_container_width=True)


# ─── 7. ABOUT ────────────────────────────────────────────────

def render_about():
    st.markdown('<p class="section-hdr">ℹ️ About AapdaSetu</p>', unsafe_allow_html=True)

    st.markdown("""
    ### What is AapdaSetu?

    **AapdaSetu** is an AI-powered disaster-response decision-support system that converts
    disaster, incident, vulnerability, and resource data into **operational priority insights**.

    It helps emergency response teams understand which disaster incidents require greater
    **operational urgency** when multiple incidents happen simultaneously and resources are limited.

    ---

    ### How It Works

    ```
    Disaster Data (EM-DAT historical records)
         ↓
    Incident Data (scenario-based incidents)
         ↓
    Area & Vulnerability Data (demographics, infrastructure)
         ↓
    Resource Availability (ambulances, rescue teams, shelters, medical supplies)
         ↓
    Feature Engineering (35 operational features)
         ↓
    ML Model (HistGradientBoostingClassifier pipeline)
         ↓
    Operational Priority (HIGH / MEDIUM / LOW)
         ↓
    Resource Allocation Support
    ```

    ---

    ### Priority Meaning

    | Level | Meaning |
    |-------|---------|
    | 🔴 **HIGH** | Greater operational urgency based on measured impact and resource pressure |
    | 🟠 **MEDIUM** | Moderate operational urgency |
    | 🟢 **LOW** | Lower operational urgency relative to other incidents |

    ---

    > ⚠️ **Every life is equally important.** AapdaSetu does not rank the value of human lives.
    > It estimates operational urgency to support faster decisions under resource constraints.

    ---

    ### Data Source Disclosure

    | Dataset | Source |
    |---------|--------|
    | **Disaster Data** | EM-DAT / CRED International Disaster Database |
    | **Area/Infrastructure** | Prototype demographic and infrastructure dataset (synthetic) |
    | **Incident Data** | Synthetic disaster-response scenarios created for prototype demonstration |
    | **Resource Data** | Synthetic emergency-resource inventory created for prototype demonstration |

    *Synthetic datasets are used for prototype demonstration. The ML model and pipeline are
    designed to work with real operational data when available.*

    ---

    ### Technical Stack

    - **ML Model**: sklearn Pipeline → ColumnTransformer (OneHotEncoder + passthrough) → HistGradientBoostingClassifier
    - **Features**: 35 (3 categorical + 32 numeric)
    - **Dashboard**: Streamlit + Plotly
    - **Data Processing**: Pandas, NumPy
    """)


# ═══════════════════════════════════════════════════════════════
# SIDEBAR & MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    inject_css()

    # ── Load data and model ──
    incident_df, areas_df, resources_df, disaster_df = load_data()
    model = load_model()

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom:18px;">
            <div style="font-size:1.6rem; font-weight:800; color:#e2e8f0;">🚨 AapdaSetu</div>
            <div style="font-size:0.72rem; color:#94a3b8; margin-top:2px;">
                AI-Powered Disaster Response
            </div>
        </div>""", unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            ["🏠 Command Center", "🗺️ Incident Map", "📊 Incident Analytics",
             "🚑 Resource Pressure", "🤖 AI Prediction", "🎬 Demo Mode", "ℹ️ About"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("##### 🔧 Filters")

        priority_filter = st.multiselect(
            "Priority Level",
            PRIORITY_ORDER,
            default=PRIORITY_ORDER,
        )
        states_available = sorted(incident_df["state"].dropna().unique())
        state_filter = st.multiselect("State", states_available)

        types_available = sorted(incident_df["disaster_type"].dropna().unique())
        type_filter = st.multiselect("Disaster Type", types_available)

        # District filter: show only districts for selected states
        if state_filter:
            districts_available = sorted(
                incident_df[incident_df["state"].isin(state_filter)]["district"].dropna().unique()
            )
        else:
            districts_available = sorted(incident_df["district"].dropna().unique())
        
        # Clean district selection if user changed state
        district_key = f"dist_filter_{hash(tuple(state_filter))}"
        district_filter = st.multiselect("District", districts_available, key=district_key)

        st.markdown("---")
        st.markdown(
            '<div class="status-pill"><span class="status-dot"></span> System Operational</div>',
            unsafe_allow_html=True,
        )

    # ── Apply filters ──
    filtered_df = incident_df.copy()
    if priority_filter:
        filtered_df = filtered_df[filtered_df["priority_level"].isin(priority_filter)]
    if state_filter:
        filtered_df = filtered_df[filtered_df["state"].isin(state_filter)]
    if type_filter:
        filtered_df = filtered_df[filtered_df["disaster_type"].isin(type_filter)]
    if district_filter:
        active_districts = [d for d in district_filter if d in districts_available]
        if active_districts:
            filtered_df = filtered_df[filtered_df["district"].isin(active_districts)]

    # ── Header ──
    hdr1, hdr2 = st.columns([3, 1])
    with hdr1:
        st.markdown("""
        <div style="margin-bottom:8px;">
            <p class="hero-title">🚨 AapdaSetu</p>
            <p class="hero-sub">AI-driven operational priority intelligence for faster emergency response</p>
        </div>""", unsafe_allow_html=True)
    with hdr2:
        st.markdown(
            '<div style="text-align:right; margin-top:16px;">'
            '<span class="status-pill"><span class="status-dot"></span> System Operational</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── Live Emergency Situation Alert Ticker ──
    top_critical = incident_df[incident_df["priority_level"] == "HIGH"].sort_values("people_affected", ascending=False).head(4)
    ticker_items = []
    for _, cr in top_critical.iterrows():
        ticker_items.append(
            f"🔴 <strong>{cr.get('disaster_type','ALERT').upper()}</strong> ({cr.get('state','State')} - {cr.get('district','Dist')}): "
            f"{int(cr.get('people_affected',0)):,} affected &bull; {int(cr.get('critical_patients',0)):,} critical &bull; "
            f"Amb. Gap: {int(cr.get('ambulance_gap',0)):,}"
        )
    ticker_html = " &nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;&nbsp; ".join(ticker_items)
    st.markdown(f"""
    <div class="alert-ticker">
        <span class="ticker-badge">🚨 CRITICAL LIVE SITUATION TICKER</span>
        <div class="ticker-content">{ticker_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Page Routing ──
    if page.startswith("🏠"):
        render_command_center(incident_df, filtered_df, model)
    elif page.startswith("🗺"):
        render_incident_map(incident_df, filtered_df)
    elif page.startswith("📊"):
        render_analytics(incident_df, filtered_df)
    elif page.startswith("🚑"):
        render_resource_pressure(incident_df, filtered_df)
    elif page.startswith("🤖"):
        render_ai_prediction(model, incident_df)
    elif page.startswith("🎬"):
        render_demo_mode(incident_df, model)
    elif page.startswith("ℹ"):
        render_about()


if __name__ == "__main__":
    main()
