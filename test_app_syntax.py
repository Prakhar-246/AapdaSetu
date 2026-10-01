#!/usr/bin/env python3
"""Test app.py for basic syntax and import errors."""

import sys
sys.path.insert(0, '.')

try:
    # Try to import all the required modules
    print("Testing imports...")
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    import joblib
    from pathlib import Path
    print("✓ All core imports successful")
    
    # Try to parse the app.py file
    print("\nChecking app.py syntax...")
    with open('app.py', 'r') as f:
        code = f.read()
    compile(code, 'app.py', 'exec')
    print("✓ app.py syntax is valid")
    
    # Load the model to check it works
    print("\nLoading model...")
    model = joblib.load('Notebook/aapdasetu_priority_model.pkl')
    print(f"✓ Model loaded: {type(model)}")
    
    # Load datasets
    print("\nLoading datasets...")
    df = pd.read_csv('data/raw/incident_dataset.csv')
    print(f"✓ Incident dataset: {df.shape}")
    
    print("\n" + "="*60)
    print("SUCCESS: App is ready to run!")
    print("="*60)
    print("\nTo start the app, run:")
    print("  streamlit run app.py")
    
except SyntaxError as e:
    print(f"\n✗ Syntax Error in app.py: {e}")
    sys.exit(1)
except ImportError as e:
    print(f"\n✗ Import Error: {e}")
    print("Install missing packages with:")
    print("  pip install streamlit pandas numpy plotly scikit-learn joblib")
    sys.exit(1)
except FileNotFoundError as e:
    print(f"\n✗ File not found: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
