#!/usr/bin/env python3
"""Quick test to verify model and data setup."""

import sys
sys.path.insert(0, 'Notebook')

import joblib
import pandas as pd
import numpy as np

print("=" * 80)
print("AAPDASETU - Model & Data Verification")
print("=" * 80)

# 1. Load model
print("\n[1] Loading Model...")
try:
    model = joblib.load('Notebook/aapdasetu_priority_model.pkl')
    print(f"    ✓ Model loaded: {type(model).__name__}")
    if hasattr(model, 'named_steps'):
        print(f"    ✓ Pipeline steps: {list(model.named_steps.keys())}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    sys.exit(1)

# 2. Load incident data
print("\n[2] Loading Incident Data...")
try:
    df = pd.read_csv('data/raw/incident_dataset.csv')
    print(f"    ✓ Shape: {df.shape}")
    print(f"    ✓ Columns: {len(df.columns)}")
    print(f"    ✓ Priority levels: {df['priority_level'].unique().tolist()}")
    print(f"    ✓ Sample incident ID: {df['incident_id'].iloc[0]}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    sys.exit(1)

# 3. Load and merge other data
print("\n[3] Loading & Merging Supporting Data...")
try:
    areas_df = pd.read_csv('data/raw/areas.csv')
    resources_df = pd.read_csv('data/raw/resources.csv')
    disaster_df = pd.read_csv('data/raw/disaster_dataset_cleaned.csv')
    print(f"    ✓ areas.csv: {areas_df.shape}")
    print(f"    ✓ resources.csv: {resources_df.shape}")
    print(f"    ✓ disaster_dataset_cleaned.csv: {disaster_df.shape}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    sys.exit(1)

# 4. Test feature engineering
print("\n[4] Testing Feature Engineering...")
try:
    # Resource aggregation (from app.py)
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
    
    # Merge area demographics
    area_cols = ["area_id", "households", "male_population", "female_population",
                 "urban_population", "rural_population", "children_population_0_6",
                 "elderly_population_60_plus", "area_sq_km", "population_density"]
    area_merge = areas_df[[c for c in area_cols if c in areas_df.columns]]
    merged_df = df.merge(area_merge, on="area_id", how="left", suffixes=("", "_area"))
    merged_df = merged_df.merge(res_agg, on="area_id", how="left", suffixes=("", "_res"))
    
    print(f"    ✓ After merge: {merged_df.shape}")
    print(f"    ✓ Resource features added: resource_pct_available, resource_pct_needs_maintenance, resource_avg_capacity")
except Exception as e:
    print(f"    ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Test prediction
print("\n[5] Testing Model Prediction...")
try:
    # Get a sample row
    sample = merged_df.iloc[0:1].copy()
    
    # Identify model features (from app.py constants)
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
    MODEL_FEATURES = CATEGORICAL_COLS + NUMERIC_COLS
    
    print(f"    - Model expects {len(MODEL_FEATURES)} features")
    print(f"      - {len(CATEGORICAL_COLS)} categorical")
    print(f"      - {len(NUMERIC_COLS)} numeric")
    
    # Prepare input
    pred_input = sample.copy()
    for col in MODEL_FEATURES:
        if col not in pred_input.columns:
            pred_input[col] = 0 if col not in CATEGORICAL_COLS else "Unknown"
    pred_input = pred_input[MODEL_FEATURES]
    
    # Predict
    pred = model.predict(pred_input)[0]
    print(f"    ✓ Prediction made: {pred}")
    
    # Check if predict_proba works
    try:
        proba = model.predict_proba(pred_input)[0]
        classes = model.classes_
        print(f"    ✓ Classes: {classes}")
        for cls, prob in zip(classes, proba):
            print(f"      - {cls}: {prob*100:.1f}%")
    except Exception as e:
        print(f"    ⚠ predict_proba not available: {e}")
    
except Exception as e:
    print(f"    ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✓ All checks passed! Ready to run Streamlit app.")
print("=" * 80)
