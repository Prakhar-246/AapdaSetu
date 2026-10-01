#!/usr/bin/env python3
"""Minimal test of imports and compilation."""

import sys

try:
    # Test imports
    import streamlit
    import pandas
    import numpy
    import plotly
    import joblib
    print("Packages OK")
    
    # Test parse
    with open('app.py', 'r') as f:
        code = f.read()
    compile(code, 'app.py', 'exec')
    print("Syntax OK")
    
    # Test model
    model = joblib.load('Notebook/aapdasetu_priority_model.pkl')
    print("Model OK")
    
    # Test data
    df = pandas.read_csv('data/raw/incident_dataset.csv')
    print(f"Data OK: {len(df)} incidents")
    
    print("\nREADY TO RUN")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
