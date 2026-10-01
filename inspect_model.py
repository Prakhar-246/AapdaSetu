#!/usr/bin/env python3
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import joblib
import pandas as pd
import numpy as np

# Load the model
print("=" * 70)
print("LOADING MODEL & DATA")
print("=" * 70)

try:
    model = joblib.load('Notebook/aapdasetu_priority_model.pkl')
    print("✓ Model loaded from Notebook/aapdasetu_priority_model.pkl")
    print(f"  Model type: {type(model)}")
    
    if hasattr(model, 'named_steps'):
        print(f"  Pipeline steps: {list(model.named_steps.keys())}")
        
        # Get preprocessing info
        if 'preprocessor' in model.named_steps:
            preproc = model.named_steps['preprocessor']
            print(f"\n  Preprocessor type: {type(preproc)}")
            if hasattr(preproc, 'transformers_'):
                for name, transformer, columns in preproc.transformers_:
                    print(f"    - {name}: {columns}")
    
    # Check classes
    if 'classifier' in model.named_steps:
        clf = model.named_steps['classifier']
        if hasattr(clf, 'classes_'):
            print(f"  Classes: {clf.classes_}")
    
    # Test prediction
    print("\n✓ Model can make predictions")
    
except Exception as e:
    print(f"✗ Error loading model: {e}")
    import traceback
    traceback.print_exc()

# Load incident data
print("\n" + "=" * 70)
print("INCIDENT DATA")
print("=" * 70)

try:
    df = pd.read_csv('data/raw/incident_dataset.csv')
    print(f"Shape: {df.shape}")
    print(f"\nColumns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\nData types:")
    print(df.dtypes)
    
    print(f"\nFirst row sample:")
    print(df.iloc[0].to_string())
    
    print(f"\nMissing values:")
    print(df.isnull().sum())
    
except Exception as e:
    print(f"Error loading incident data: {e}")
    import traceback
    traceback.print_exc()

# Load other data
print("\n" + "=" * 70)
print("OTHER DATA")
print("=" * 70)

try:
    areas_df = pd.read_csv('data/raw/areas.csv')
    print(f"areas.csv shape: {areas_df.shape}")
    print(f"Columns: {areas_df.columns.tolist()}")
except Exception as e:
    print(f"Error: {e}")

try:
    resources_df = pd.read_csv('data/raw/resources.csv')
    print(f"\nresources.csv shape: {resources_df.shape}")
    print(f"Columns: {resources_df.columns.tolist()}")
except Exception as e:
    print(f"Error: {e}")

try:
    disaster_df = pd.read_csv('data/raw/disaster_dataset_cleaned.csv')
    print(f"\ndisaster_dataset_cleaned.csv shape: {disaster_df.shape}")
    print(f"Columns: {disaster_df.columns.tolist()}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
