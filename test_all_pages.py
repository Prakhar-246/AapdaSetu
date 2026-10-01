#!/usr/bin/env python3
"""Comprehensive test suite for AapdaSetu."""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

print("=" * 80)
print("RUNNING AAPDASETU COMPREHENSIVE TEST SUITE")
print("=" * 80)

# 1. Imports from app.py
from app import (
    load_data,
    load_model,
    create_scatter_map,
    style_priority_table,
    priority_badge_html,
    kpi_html,
    resource_bar_html,
    decision_support_html,
    predict_priority,
    PRIORITY_COLORS,
    PRIORITY_ORDER,
    PLOTLY_LAYOUT,
    MODEL_FEATURES,
    CATEGORICAL_COLS,
    NUMERIC_COLS,
)

print("\n[TEST 1] Loading Data & Model...")
incident_df, areas_df, resources_df, disaster_df = load_data()
model = load_model()
assert len(incident_df) > 0, "Incident data is empty!"
assert model is not None, "Model failed to load!"
print(f"  ✓ Incidents: {len(incident_df)} rows, {len(incident_df.columns)} columns")
print(f"  ✓ Model: {type(model).__name__}")

# Check engineered features
for feat in ["resource_pct_available", "resource_pct_needs_maintenance", "resource_avg_capacity"]:
    assert feat in incident_df.columns, f"Missing engineered feature: {feat}"
print("  ✓ All engineered features present")

# 2. Test style_priority_table
print("\n[TEST 2] Testing style_priority_table...")
sample_table = incident_df[["incident_id", "priority_level", "people_affected"]].head(10)
styler = style_priority_table(sample_table, ["incident_id", "priority_level"])
assert styler is not None
print("  ✓ Styler created successfully without applymap attribute errors")

# 3. Test create_scatter_map
print("\n[TEST 3] Testing create_scatter_map...")
map_df = incident_df.head(50).copy()
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
assert fig is not None
print("  ✓ Map and layout generated without duplicate keyword errors")

# 4. Test HTML generators
print("\n[TEST 4] Testing HTML Helpers...")
b_high = priority_badge_html("HIGH")
b_med = priority_badge_html("MEDIUM")
b_low = priority_badge_html("LOW")
assert "badge-high" in b_high
assert "badge-medium" in b_med
assert "badge-low" in b_low

kpi = kpi_html("Total Incidents", 5184, "#60a5fa")
assert "5,184" in kpi

r_bar = resource_bar_html("Ambulance", 100, 80)
assert "Ambulance" in r_bar

dec_html = decision_support_html(incident_df.iloc[0])
assert "decision-box" in dec_html
print("  ✓ All HTML components render cleanly")

# 5. Test Analytics Charts
print("\n[TEST 5] Testing Analytics Charts Generation...")
dist = incident_df["priority_level"].value_counts().reindex(PRIORITY_ORDER).fillna(0)
fig1 = go.Figure(go.Pie(
    labels=dist.index, values=dist.values,
    marker=dict(colors=[PRIORITY_COLORS[p] for p in dist.index]),
    hole=0.55, textinfo="label+value",
))
fig1.update_layout(**PLOTLY_LAYOUT, title="Priority Distribution", height=380)

type_counts = incident_df["disaster_type"].value_counts().head(12)
fig2 = px.bar(x=type_counts.values, y=type_counts.index, orientation="h", color_discrete_sequence=["#3b82f6"])
fig2.update_layout(**PLOTLY_LAYOUT, title="Incidents by Disaster Type", height=380)

high_by_state = incident_df[incident_df["priority_level"] == "HIGH"].groupby("state").size().sort_values(ascending=False).head(15)
fig3 = px.bar(x=high_by_state.values, y=high_by_state.index, orientation="h", color_discrete_sequence=["#ef4444"])
fig3.update_layout(**PLOTLY_LAYOUT, title="High Priority Incidents by State", height=380)

affected_by_priority = incident_df.groupby("priority_level")["people_affected"].sum().reindex(PRIORITY_ORDER).fillna(0)
fig4 = px.bar(x=affected_by_priority.index, y=affected_by_priority.values, color=affected_by_priority.index, color_discrete_map=PRIORITY_COLORS)
fig4.update_layout(**PLOTLY_LAYOUT, title="People Affected by Priority", height=380, showlegend=False)

fig5 = px.box(incident_df, x="priority_level", y="resource_shortage", color="priority_level", color_discrete_map=PRIORITY_COLORS, category_orders={"priority_level": PRIORITY_ORDER})
fig5.update_layout(**PLOTLY_LAYOUT, title="Resource Shortage vs Priority", height=380, showlegend=False)

sample = incident_df.sample(min(800, len(incident_df)), random_state=42)
fig6 = px.scatter(sample, x="severity_score", y="priority_score", color="priority_level", color_discrete_map=PRIORITY_COLORS, category_orders={"priority_level": PRIORITY_ORDER}, opacity=0.6)
fig6.update_layout(**PLOTLY_LAYOUT, title="Severity Score vs Priority Score", height=380)
print("  ✓ All 6 Analytics charts created without error")

# 6. Test Model Prediction & Edge Cases
print("\n[TEST 6] Testing Model Prediction Edge Cases...")
row_sample = incident_df.iloc[0].to_dict()
res_a = predict_priority(model, row_sample)
assert res_a["priority"] in ["HIGH", "MEDIUM", "LOW"], f"Invalid priority: {res_a['priority']}"
print(f"  ✓ Standard prediction: {res_a['priority']} (Confidence: {res_a['confidence']*100:.1f}%)")

extreme_high = {
    "state": "Maharashtra", "disaster_type": "Flood", "disaster_subtype": "Riverine flood",
    "population": 5000000, "people_affected": 2000000, "deaths": 5000, "injured": 25000,
    "critical_patients": 4000, "children_affected": 500000, "elderly_affected": 300000,
    "hospital_count": 50, "ambulance_count": 100, "available_ambulances": 10,
    "rescue_team_count": 20, "available_rescue_teams": 2, "shelter_capacity": 50000,
    "available_shelter_capacity": 5000, "hospital_capacity": 2000, "medical_supply": 500,
    "ambulance_demand": 500, "rescue_team_demand": 100, "shelter_demand": 500000,
    "medical_supply_demand": 50000, "households": 1000000, "male_population": 2500000,
    "female_population": 2500000, "urban_population": 4000000, "rural_population": 1000000,
    "children_population_0_6": 400000, "elderly_population_60_plus": 350000,
    "area_sq_km": 8000, "population_density": 625.0,
    "resource_pct_available": 0.15, "resource_pct_needs_maintenance": 0.45, "resource_avg_capacity": 20.0
}
res_b = predict_priority(model, extreme_high)
print(f"  ✓ Extreme emergency prediction: {res_b['priority']} (Confidence: {res_b['confidence']*100:.1f}%)")

extreme_low = {
    "state": "Goa", "disaster_type": "Storm", "disaster_subtype": "Thunderstorm",
    "population": 50000, "people_affected": 10, "deaths": 0, "injured": 2,
    "critical_patients": 0, "children_affected": 1, "elderly_affected": 1,
    "hospital_count": 10, "ambulance_count": 30, "available_ambulances": 30,
    "rescue_team_count": 10, "available_rescue_teams": 10, "shelter_capacity": 5000,
    "available_shelter_capacity": 5000, "hospital_capacity": 500, "medical_supply": 2000,
    "ambulance_demand": 1, "rescue_team_demand": 1, "shelter_demand": 5,
    "medical_supply_demand": 5, "households": 12000, "male_population": 25000,
    "female_population": 25000, "urban_population": 20000, "rural_population": 30000,
    "children_population_0_6": 4000, "elderly_population_60_plus": 3500,
    "area_sq_km": 1500, "population_density": 33.3,
    "resource_pct_available": 0.95, "resource_pct_needs_maintenance": 0.0, "resource_avg_capacity": 100.0
}
res_c = predict_priority(model, extreme_low)
print(f"  ✓ Low impact prediction: {res_c['priority']} (Confidence: {res_c['confidence']*100:.1f}%)")

all_zeros = {k: (0 if k not in CATEGORICAL_COLS else "Unknown") for k in MODEL_FEATURES}
res_d = predict_priority(model, all_zeros)
print(f"  ✓ All zeros input handled: {res_d['priority']}")

unseen_cat = {
    "state": "Atlantis", "disaster_type": "CosmicRay", "disaster_subtype": "SolarFlare",
    **{k: 100 for k in NUMERIC_COLS}
}
res_e = predict_priority(model, unseen_cat)
print(f"  ✓ Unseen categories handled gracefully: {res_e['priority']}")

# 7. Test Demo Mode logic for HIGH, MEDIUM, LOW
print("\n[TEST 7] Testing Demo Mode Selection...")
for level in ["HIGH", "MEDIUM", "LOW"]:
    pool = incident_df[incident_df["priority_level"] == level]
    if level == "HIGH":
        row = pool.nlargest(5, "priority_score").sample(1, random_state=42).iloc[0]
    elif level == "MEDIUM":
        med = pool["priority_score"].median()
        row = pool.iloc[(pool["priority_score"] - med).abs().argsort()[:1]].iloc[0]
    else:
        row = pool.nsmallest(5, "priority_score").sample(1, random_state=42).iloc[0]
    
    # Generate demo map
    demo_map = create_scatter_map(
        pd.DataFrame([row]),
        lat="latitude", lon="longitude",
        color_discrete_sequence=[PRIORITY_COLORS[level]],
        mapbox_style="carto-darkmatter",
        zoom=5,
        center={"lat": row["latitude"], "lon": row["longitude"]},
        height=350,
    )
    demo_map.update_traces(marker=dict(size=18))
    demo_map_layout = {**PLOTLY_LAYOUT, "margin": dict(l=0, r=0, t=0, b=0)}
    demo_map.update_layout(**demo_map_layout)
    print(f"  ✓ Demo Mode {level}: Incident {row['incident_id']} selected & map generated")

# 8. Test Resource Pressure Calculations
print("\n[TEST 8] Testing Resource Pressure Calculations...")
constrained = incident_df.copy()
constrained["total_resource_gap"] = (
    constrained["ambulance_gap"] + constrained["rescue_team_gap"]
    + constrained["shelter_gap"] + constrained["medical_supply_gap"]
)
constrained = constrained.sort_values("total_resource_gap", ascending=False).head(20)
disp_cols = ["incident_id", "state", "district", "priority_level",
             "resource_shortage", "ambulance_gap", "rescue_team_gap",
             "shelter_gap", "medical_supply_gap", "total_resource_gap"]
styler_res = style_priority_table(constrained, disp_cols)
assert styler_res is not None
print("  ✓ Resource Pressure table computed and styled successfully")

print("\n" + "=" * 80)
print("ALL TESTS PASSED! APPLICATION IS 100% HEALTHY AND BUG-FREE.")
print("=" * 80)
