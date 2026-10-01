# 🚨 AapdaSetu Quick Reference Card

## ⚡ Super Quick Start (Copy & Paste)

```bash
# Windows PowerShell
cd "Aapda Setu"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py

# macOS/Linux
cd "Aapda Setu"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open: **http://localhost:8501**

---

## 🎯 7 Dashboard Pages

| Icon | Page | Key Feature |
|------|------|------------|
| 🏠 | Command Center | KPI cards + incident table |
| 🗺️ | Incident Map | Interactive geographic map |
| 📊 | Analytics | 6 analytical charts |
| 🚑 | Resource Pressure | Shortage identification |
| 🤖 | AI Prediction | Manual incident prediction |
| 🎬 | Demo Mode | Real incident showcase |
| ℹ️ | About | System documentation |

---

## 📊 Key Metrics at a Glance

- **Total Incidents**: Displayed in KPI cards
- **High Priority**: RED 🔴
- **Medium Priority**: ORANGE 🟠
- **Low Priority**: GREEN 🟢
- **Model Features**: 35 (3 categorical + 32 numeric)
- **Classes**: HIGH / MEDIUM / LOW

---

## 🔧 Sidebar Filters

```
Priority Level    → HIGH, MEDIUM, LOW (multi-select)
State            → All Indian states (multi-select)
Disaster Type    → Storm, Flood, Earthquake, etc. (multi-select)
District         → Updates based on selected states
```

---

## 💻 File Locations

```
app.py                           ← Main app (run this)
requirements.txt                 ← Dependencies
data/raw/*.csv                   ← Input data
Notebook/aapdasetu_priority_model.pkl  ← ML model
```

---

## 📈 Dashboard Sections

### Command Center
- **KPIs**: Total incidents, priority breakdown, people affected, resources
- **Table**: Searchable incident list with sorting
- **Detail**: Click incident → see resource situation + decision support

### Map
- **Markers**: Position = state centroid + jitter, Size = people affected, Color = priority
- **Statistics**: State-level breakdown in expander

### Analytics
- **Chart 1**: Priority distribution (pie)
- **Chart 2**: Incidents by type (bar)
- **Chart 3**: High priority by state (bar, top 15)
- **Chart 4**: People affected by priority (bar)
- **Chart 5**: Resource shortage vs priority (box)
- **Chart 6**: Severity vs priority score (scatter)

### Resource Pressure
- **Cards**: 4 resource types (ambulances, rescue teams, shelter, medical supplies)
- **Table**: Most constrained incidents (top 20)

### AI Prediction
- **Form**: Enter incident parameters
- **Pre-fill**: Load existing incident data
- **Result**: Priority + confidence + probabilities

### Demo
- **Buttons**: HIGH / MEDIUM / LOW priority examples
- **Real data**: From actual incident dataset
- **Quick showcase**: < 30 seconds for judges

### About
- **What**: System explanation
- **How**: Data pipeline
- **Data sources**: Real vs. synthetic
- **Ethics**: "Every life is equally important"

---

## 🎯 Model Info

```
Type:      sklearn Pipeline
Features:  35 (3 categorical + 32 numeric)
Output:    HIGH / MEDIUM / LOW
Classes:   ['HIGH', 'LOW', 'MEDIUM']
Predict:   ✓ Yes
Probabilities: ✓ Yes (confidence scores)
```

---

## 🌐 Deployment

```bash
# Option 1: Streamlit Cloud (FREE)
# → https://share.streamlit.io

# Option 2: Heroku ($7/month)
heroku create your-app-name
git push heroku main

# Option 3: AWS/Azure (Free tier available)
# → See README.md
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: streamlit` | `pip install -r requirements.txt` |
| `FileNotFoundError: incident_dataset.csv` | Check data/raw/ folder exists |
| Map not showing | Check internet, Plotly needs online |
| Slow performance | Close other apps, refresh browser |
| Model prediction error | Ensure categorical values are valid |

---

## ✅ Pre-Demo Checklist

- [ ] App runs without errors
- [ ] All 7 pages load
- [ ] Map displays with markers
- [ ] Filters work
- [ ] AI prediction works
- [ ] Demo mode works
- [ ] No visual glitches
- [ ] Ethical framing is clear

---

## 📞 Documentation Links

- **Full Setup**: TESTING_GUIDE.md
- **Full Docs**: README.md
- **Completion Status**: COMPLETION_REPORT.md
- **This**: QUICK_REFERENCE.md

---

## 🎨 Theme Colors

```
Primary Color:    #EF4444 (RED emergency)
Background:       #0d1321 (Dark navy)
Secondary:        #1a2332 (Charcoal)
Text:             #e2e8f0 (Light gray)

Priority Colors:
  HIGH:    #EF4444 🔴
  MEDIUM:  #F97316 🟠
  LOW:     #22C55E 🟢
```

---

## 👥 For Judges: 30-Second Demo Script

1. **Map (5 sec)**: "This shows all incidents geographically. Red = high priority."
2. **Demo Incident (5 sec)**: "Here's a real HIGH priority incident with massive resource shortage."
3. **Drill-down (10 sec)**: "The AI tells responders: 17 ambulances short, 13 rescue teams short."
4. **Model (5 sec)**: "35 features, real ML model, not hardcoded."
5. **Ethics (5 sec)**: "This supports decisions, doesn't rank whose life matters."

---

## 🚀 You're Ready!

Everything is set up and documented.  
Follow TESTING_GUIDE.md to get started.  
Questions? Check README.md or COMPLETION_REPORT.md.

**Good luck! 🚨**

---

*AapdaSetu — AI-Powered Disaster Response & Resource Allocation*  
*Emergency Operations Command Center Dashboard*
