# 🚀 AapdaSetu — Local Setup & Testing Guide

## Prerequisites

- Python 3.9+ installed
- Git (optional, for version control)
- Internet connection (for Plotly mapbox and Streamlit)
- ~500 MB free disk space

---

## Step 1: Clone or Extract Project

```bash
# If you have the project as a ZIP:
unzip "Aapda Setu.zip"
cd "Aapda Setu"

# Or if using Git:
git clone https://github.com/your-repo/Aapda-Setu.git
cd Aapda-Setu
```

---

## Step 2: Create Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` prefix in terminal now**

---

## Step 3: Install Dependencies

```bash
# Upgrade pip (recommended)
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**This installs:**
- `streamlit>=1.28.0` — Dashboard framework
- `pandas>=1.5.0` — Data processing
- `numpy>=1.23.0` — Numerical computing
- `plotly>=5.15.0` — Interactive visualizations
- `scikit-learn>=1.2.0` — ML model
- `joblib>=1.2.0` — Model serialization

**Installation time: ~3-5 minutes (depends on internet speed)**

---

## Step 4: Verify Installation

```bash
python -c "import streamlit; import pandas; import plotly; print('✓ All packages installed')"
```

**Expected output:**
```
✓ All packages installed
```

---

## Step 5: Run the Dashboard

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## Step 6: Access the Dashboard

Open your web browser and go to:
```
http://localhost:8501
```

The AapdaSetu dashboard should load with the emergency operations center theme.

---

## 📋 Testing Checklist

### ✅ Initial Load (< 5 seconds)
- [ ] No error messages
- [ ] Dark theme loads (navy background)
- [ ] Sidebar visible with navigation
- [ ] Status pill shows "System Operational"

### ✅ Page 1: Command Center (Home)
- [ ] KPI cards display: Total Incidents, High/Medium/Low Priority, People Affected, Resources
- [ ] Incident table loads with data
- [ ] Search box works (try: "INC0")
- [ ] Sort dropdown works
- [ ] "Show only HIGH priority" checkbox works
- [ ] CSV download button available
- [ ] Drill-down incident detail opens
- [ ] Decision support panel displays

**How to test**:
1. Search for "INC" in the search box
2. Click on an incident ID in the dropdown
3. Verify the resource situation bars display

### ✅ Page 2: Incident Map
- [ ] Map loads (may take 2-3 seconds for tiles)
- [ ] Markers visible (red, orange, green colors)
- [ ] Hover over marker shows popup
- [ ] State statistics expander opens/closes
- [ ] No map errors in browser console (F12)

**How to test**:
1. Hover over a marker to see incident details
2. Click state statistics expander to see breakdown
3. Use browser zoom to inspect markers

### ✅ Page 3: Incident Analytics
- [ ] All 6 charts render (pie, bar, box, scatter)
- [ ] Charts are interactive (hover shows values)
- [ ] No blank/error states
- [ ] Colors match priority levels

**How to test**:
1. Hover over chart elements to see tooltips
2. Scroll through charts
3. Zoom in/out on scatter plot

### ✅ Page 4: Resource Pressure
- [ ] 4 resource cards display (Ambulances, Rescue Teams, Shelter, Medical Supplies)
- [ ] Utilization % looks reasonable
- [ ] Top 20 constrained incidents table displays
- [ ] Shortage indicators are clear (red = shortage)

**How to test**:
1. Scroll down to see all resources
2. Check if shortage numbers make sense
3. Verify table is sorted by total resource gap

### ✅ Page 5: AI Prediction
- [ ] Form loads with all input fields
- [ ] Pre-fill dropdown works
- [ ] Can enter custom values
- [ ] "Predict Operational Priority" button works
- [ ] Shows prediction, confidence, and probabilities
- [ ] Key operational factors listed

**How to test**:
1. Select a pre-fill incident
2. Modify a few values
3. Click predict button
4. Verify result makes sense

### ✅ Page 6: Demo Mode
- [ ] 3 demo buttons visible (HIGH, MEDIUM, LOW)
- [ ] Buttons switch between different incidents
- [ ] Incident detail displays
- [ ] Map shows incident location
- [ ] Completes in < 30 seconds

**How to test**:
1. Click HIGH button
2. Review the incident details
3. Click MEDIUM and LOW buttons
4. Verify different incidents display

### ✅ Page 7: About
- [ ] All sections readable
- [ ] Data source disclosure visible
- [ ] Ethical framing prominent
- [ ] Technical stack listed

**How to test**:
1. Scroll through entire section
2. Verify no broken links or formatting

---

## 🎛️ Sidebar Filters

### Test Filtering:
1. **Priority Filter**
   - [ ] Select only "HIGH" → only high-priority incidents display
   - [ ] Select "HIGH" + "MEDIUM" → both display
   - [ ] Deselect all → no incidents show

2. **State Filter**
   - [ ] Select 1-2 states → only those states' incidents display
   - [ ] Verify all pages update

3. **Disaster Type Filter**
   - [ ] Select 1 type → only that type displays
   - [ ] Verify analytics charts update

4. **District Filter**
   - [ ] District dropdown updates based on selected states
   - [ ] Filtering works correctly

---

## 🔍 Performance Benchmarks

| Page | Load Time | Expected |
|------|-----------|----------|
| Command Center | 2-3s | First load caching data |
| Map | 3-5s | Loading Plotly mapbox tiles |
| Analytics | 1-2s | Cached data, plotting |
| Resource Pressure | 1-2s | Cached data |
| AI Prediction | <1s | Form only, no data load |
| Demo Mode | 1-2s | Cached data |

**Subsequent navigations should be < 1 second** (due to caching)

---

## 🐛 Debugging

### If app crashes or shows error:

1. **Check terminal output**
   ```
   Look for error message in terminal where you ran `streamlit run app.py`
   ```

2. **Check browser console**
   - Press F12 or right-click → Inspect
   - Click "Console" tab
   - Look for red error messages

3. **Common issues**:

   | Error | Solution |
   |-------|----------|
   | `FileNotFoundError: data/raw/incident_dataset.csv` | Check file paths, ensure data/ folder exists |
   | `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
   | `ConnectionError` when loading map | Check internet, Plotly needs online tiles |
   | `Model prediction error` | Check feature names, ensure categorical values are valid |
   | `Slow performance` | Close other apps, refresh browser cache (Ctrl+Shift+Delete) |

4. **Reset Streamlit cache** (if data looks stale):
   ```bash
   # Stop the app (Ctrl+C)
   # Delete cache:
   rm -r ~/.streamlit/cache  # macOS/Linux
   rmdir %USERPROFILE%\.streamlit\cache  # Windows
   # Re-run: streamlit run app.py
   ```

---

## 📊 Verifying Model Works

The model file `Notebook/aapdasetu_priority_model.pkl` should be a trained sklearn Pipeline.

To verify it loads:
```python
import joblib
model = joblib.load('Notebook/aapdasetu_priority_model.pkl')
print(type(model))  # Should print: <class 'sklearn.pipeline.Pipeline'>
print(model.classes_)  # Should print: ['HIGH' 'LOW' 'MEDIUM']
```

---

## 🎯 Demo Talking Points (30 seconds for judges)

1. **Show the map** (5 sec)
   - "This is the geographical view of all disasters. Red = high priority, orange = medium, green = low."

2. **Click to Demo Mode** (5 sec)
   - "Let's see a real HIGH priority incident. Notice the massive resource shortage."

3. **Show the drill-down** (10 sec)
   - "The system tells us what resources are missing. Here we have a 17-ambulance shortage and 13-rescue-team shortage."

4. **Show the prediction form** (5 sec)
   - "We can also predict priority for new incidents. Enter the numbers, and the AI model predicts urgency."

5. **Emphasize the ethical framing** (5 sec)
   - "This is NOT ranking whose life is more valuable. It's helping responders allocate limited resources faster."

---

## ✅ Ready for Judges Checklist

Before showing to judges:
- [ ] App runs without errors
- [ ] All 7 pages load correctly
- [ ] Map displays
- [ ] Filters work
- [ ] AI prediction works
- [ ] Demo mode works
- [ ] No lag or visual glitches
- [ ] Ethical framing is clear

---

## 🚀 Next Steps After Local Testing

Once you've verified everything locally:

1. **Push to GitHub** (if deploying to Streamlit Community Cloud)
2. **Deploy to Streamlit Cloud** (see README.md for steps)
3. **Test on mobile** (Streamlit is responsive)
4. **Share the link** with judges

---

## 📞 Troubleshooting Support

If stuck:
1. Review the README.md troubleshooting section
2. Check browser console (F12) for errors
3. Review app.py comments for implementation details
4. Try on a different browser (Chrome, Firefox, Edge)
5. Restart the app (`Ctrl+C`, then `streamlit run app.py`)

---

**Good luck with your hackathon! 🚨**
