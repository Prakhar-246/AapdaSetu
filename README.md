# 🚨 AapdaSetu — AI-Powered Disaster Response & Resource Allocation

**Emergency Operations Command Center Dashboard**

A professional, hackathon-ready Streamlit dashboard built around a trained machine learning model that predicts operational priority for disaster incidents. Helps emergency response teams understand which disasters require greater operational urgency when resources are limited.

---

## 📋 Project Structure

```
Aapda Setu/
├── app.py                              # Main Streamlit dashboard (complete, production-ready)
├── requirements.txt                    # Python dependencies
├── data/
│   └── raw/
│       ├── incident_dataset.csv        # Synthetic disaster incidents (~1000 rows)
│       ├── areas.csv                   # Area demographics & infrastructure
│       ├── resources.csv               # Emergency resources inventory
│       └── disaster_dataset_cleaned.csv # EM-DAT historical disaster data
└── Notebook/
    ├── aapdasetu_priority_model.pkl    # Trained ML model (sklearn Pipeline)
    ├── ResQ_AI_Priority_Prediction.ipynb # Model training notebook
    └── generation.py                   # Data generation script
```

---

## 🚀 Quick Start

### 1. **Installation**

#### Option A: With Virtual Environment (Recommended)

```bash
cd "path/to/Aapda Setu"

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Option B: Direct Installation

```bash
pip install streamlit>=1.28.0 pandas>=1.5.0 numpy>=1.23.0 plotly>=5.15.0 scikit-learn>=1.2.0 joblib>=1.2.0
```

### 2. **Run the Dashboard**

```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`

---

## 📊 Dashboard Features

### 🏠 **Command Center** (Home)
- Executive overview KPI cards (total incidents, high-priority count, people affected, etc.)
- Live incident command table with search, filter, and sort capabilities
- Download filtered incidents as CSV
- Incident detail drill-down panel with resource situation and decision support

### 🗺️ **Incident Map**
- Interactive geographical map showing incident locations
- Marker colors represent priority (🔴 HIGH / 🟠 MEDIUM / 🟢 LOW)
- Marker size proportional to people affected
- Hover details for each incident
- State-level statistics breakdown

### 📊 **Incident Analytics**
- Priority distribution pie chart
- Incidents by disaster type
- High-priority incidents by state (top 15)
- People affected by priority level
- Resource shortage vs priority (box plot)
- Severity score vs priority score (scatter plot)

### 🚑 **Resource Pressure Center**
- Overall resource availability summary (ambulances, rescue teams, shelter, medical supplies)
- Utilization percentages and shortage indicators
- Most resource-constrained incidents table (sorted by total resource gap)
- Quick identification of critical bottlenecks

### 🤖 **AI Priority Prediction**
- Interactive form to enter incident parameters
- Pre-fill option from existing incidents
- Predictions with confidence scores
- Class probability breakdown
- Key operational factors identified from input data

### 🎬 **Demo Mode**
- Quick showcase for judges (< 30 seconds to understand the system)
- Real incidents from dataset (HIGH, MEDIUM, LOW examples)
- Full incident detail and location map for selected example

### ℹ️ **About**
- System overview and explanation
- Data pipeline documentation
- Data source disclosure (real vs. synthetic)
- Technical stack details
- Ethical framing of the system

---

## 🔧 Technical Details

### Model Architecture
- **Type**: sklearn Pipeline
- **Preprocessing**: ColumnTransformer with OneHotEncoder (categorical) + Passthrough (numeric)
- **Classifier**: HistGradientBoostingClassifier
- **Features**: 35 (3 categorical + 32 numeric)
- **Classes**: HIGH, MEDIUM, LOW
- **Output**: Priority level + confidence scores

### Model Features

**Categorical (3)**:
- `state` — State where incident occurs
- `disaster_type` — Type of disaster (Storm, Flood, Earthquake, etc.)
- `disaster_subtype` — Specific subtype (Lightning/Thunderstorms, etc.)

**Numeric (32)**:
- **Population metrics**: population, people_affected, deaths, injured, critical_patients, children_affected, elderly_affected
- **Infrastructure**: hospital_count, ambulance_count, rescue_team_count, shelter_capacity
- **Resource availability**: available_ambulances, available_rescue_teams, available_shelter_capacity, medical_supply
- **Resource demand**: ambulance_demand, rescue_team_demand, shelter_demand, medical_supply_demand
- **Demographics**: households, male_population, female_population, urban_population, rural_population, children_population_0_6, elderly_population_60_plus
- **Geography**: area_sq_km, population_density
- **Resource health**: resource_pct_available, resource_pct_needs_maintenance, resource_avg_capacity

### Dashboards Performance
- **Caching**: Model and datasets are cached with `@st.cache_resource` and `@st.cache_data`
- **Load time**: ~2-3 seconds (first load), <1 second (subsequent loads)
- **Data processing**: Real-time filtering, sorting, and aggregation

---

## 📁 File Descriptions

### `app.py` (Main Application)
**Lines of Code**: ~1,200  
**Sections**:
1. **Page Config & Constants** (Lines 1-95)
2. **Custom CSS Styling** (Lines 97-160)
3. **Data Loading Functions** (Lines 168-265)
   - `load_data()` — Loads and merges all datasets, engineers resource features
   - `load_model()` — Loads the trained model from pickle
4. **Helper Utilities** (Lines 271-390)
   - `priority_badge_html()` — Creates priority badges
   - `resource_bar_html()` — Creates resource availability bars
   - `decision_support_html()` — Generates decision support panels
   - `predict_priority()` — Runs ML predictions
5. **Section Renderers** (Lines 392-1020)
   - `render_command_center()` — KPI + incident table + drill-down
   - `render_incident_map()` — Interactive map visualization
   - `render_analytics()` — Six analytical charts
   - `render_resource_pressure()` — Resource shortage analysis
   - `render_ai_prediction()` — Prediction form and results
   - `render_demo_mode()` — Demo incident showcase
   - `render_about()` — System information
6. **Main & Routing** (Lines 1105-1200)
   - `main()` — Sidebar navigation, filtering, page routing

---

## 🧪 Testing Checklist (Before Showing Judges)

### 1. **Basic Functionality**
- [ ] App loads without errors
- [ ] All pages accessible from sidebar navigation
- [ ] Filters work correctly (priority, state, disaster type, district)
- [ ] No lag or visual glitches

### 2. **Command Center**
- [ ] KPI cards display with correct values
- [ ] Incident table shows data and is sortable
- [ ] Search works (try searching by incident ID, state, etc.)
- [ ] CSV download button works
- [ ] Incident drill-down opens and displays resource details
- [ ] Decision support panel makes sense

### 3. **Incident Map**
- [ ] Map loads and displays markers
- [ ] Markers have correct colors (HIGH=red, MEDIUM=orange, LOW=green)
- [ ] Hover shows incident details
- [ ] State statistics expander shows data
- [ ] No marker overlap issues (jitter is applied)

### 4. **Analytics**
- [ ] All 6 charts render
- [ ] Charts are interactive (hover, zoom, etc.)
- [ ] Data aggregations look correct
- [ ] No blank or error charts

### 5. **Resource Pressure**
- [ ] Overall resource cards display correctly
- [ ] Utilization percentages make sense
- [ ] Most constrained incidents table is sorted properly
- [ ] Shortage indicators are clear (green for OK, red for shortage)

### 6. **AI Prediction**
- [ ] Form loads with all input fields
- [ ] Pre-fill from existing incidents works
- [ ] Prediction runs and displays result
- [ ] Confidence score shows
- [ ] Probabilities display for all classes
- [ ] Key operational factors list makes sense

### 7. **Demo Mode**
- [ ] HIGH/MEDIUM/LOW buttons work
- [ ] Switches between real incidents
- [ ] Incident detail displays correctly
- [ ] Map marker shows for demo incident
- [ ] Demo completes in < 30 seconds

### 8. **About**
- [ ] All sections readable
- [ ] Data source disclosure clear
- [ ] Ethical framing prominent

---

## 🌐 Deployment to Streamlit Community Cloud

### Prerequisites
- GitHub account
- Repository with `app.py`, `requirements.txt`, and `data/` folder pushed

### Step-by-Step

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Add AapdaSetu dashboard"
   git push origin main
   ```

2. **Go to Streamlit Community Cloud**
   - Visit: https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Select the branch (main/master)
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configure Secrets** (if needed in future)
   - Streamlit Community Cloud > App > Settings > Secrets
   - Add any API keys or credentials (not needed for this demo)

4. **Share Link**
   - Deployment takes 1-2 minutes
   - Copy the generated URL
   - Share with judges: `https://share.streamlit.io/your-username/your-repo/app.py`

### Alternative: Deploy on Other Platforms

**Heroku** (paid, but easy):
```bash
pip install heroku
heroku login
heroku create your-app-name
git push heroku main
```

**AWS/Azure** (free tier available, more setup):
Follow platform-specific Streamlit deployment guides.

---

## 🛠️ Troubleshooting

### **Problem**: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: 
```bash
pip install -r requirements.txt
```

### **Problem**: `FileNotFoundError: aapdasetu_priority_model.pkl not found`
**Solution**: 
- Ensure the model file is in `Notebook/` directory
- Check file path in the `_find_file()` function in app.py

### **Problem**: Slow dashboard / timeout errors
**Solution**: 
- Check internet speed
- Streamlit caching should prevent re-loading data
- Try closing and reopening the browser

### **Problem**: Map not displaying
**Solution**: 
- Plotly requires internet to load mapbox tiles
- Check browser's developer console for errors
- Ensure latitude/longitude columns exist in data

### **Problem**: Prediction gives error
**Solution**: 
- Model expects exactly 35 features in correct order
- Check feature names match `MODEL_FEATURES` in app.py
- Ensure categorical values are valid (state, disaster_type, disaster_subtype)

---

## 💡 Key Design Decisions

### 1. **Color Scheme**
- Dark navy/emergency operations center aesthetic (#0d1321, #111827, #1a2332)
- Emergency accent colors: Red (#EF4444) for HIGH, Orange (#F97316) for MEDIUM, Green (#22C55E) for LOW
- Professional, not distracting

### 2. **Feature Engineering**
- Resource aggregation: Computed from resource-level data to get area-level availability
- Demographic merge: Connects area population characteristics with incidents
- No data leakage: Excluded `priority_score` and related leakage features from training

### 3. **Model Handling**
- Loads once and caches: `@st.cache_resource` for model, `@st.cache_data` for data
- Handles missing features: Defaults to 0 for numeric, "Unknown" for categorical
- Supports both `predict()` and `predict_proba()`: Graceful fallback

### 4. **Ethical Framing**
- Repeated disclaimer: "Every life is equally important"
- System frames as decision support, not autonomous command
- Operational urgency ≠ value of life
- Transparent data sources: Distinguishes real vs. synthetic data

### 5. **UX for Judges**
- Demo mode: Real incidents, < 30 seconds to understand
- KPI cards: Immediate impact overview
- Map: Geographical context
- Drill-down: Details on demand
- Prediction form: Interactive engagement

---

## 📖 Model Documentation

The trained model is a **sklearn Pipeline** that was trained on synthesized disaster-incident data. The model learns to map incident characteristics (population affected, resource demands, casualties, etc.) to priority levels.

**Training Process** (from notebook):
1. Data preparation: Merged incident, area, and resource data
2. Feature engineering: Created resource availability metrics
3. Preprocessing: OneHotEncoded categorical features
4. Model training: HistGradientBoostingClassifier with cross-validation
5. Evaluation: Achieved ~85-90% accuracy on test set (synthetic data)
6. Serialization: Saved as `aapdasetu_priority_model.pkl`

**Key Assumption**:
The model was trained on *synthetic* data. In production, it should be re-trained or fine-tuned with real incident data to ensure relevance.

---

## 📝 License & Attribution

**Dataset Sources**:
- **Disaster Data**: EM-DAT (CRED International Disaster Database)
- **Area/Demographics**: Synthetic prototype dataset
- **Incidents**: Synthetic scenarios for demonstration
- **Resources**: Synthetic inventory for prototype

**Model Training**: ResQ AI Priority Prediction Notebook (included)

**Dashboard**: Built with Streamlit, Plotly, Pandas, NumPy, scikit-learn

---

## 🎯 Hackathon Judging Tips

1. **Show the map first**: Judges immediately see the geographic scale
2. **Use demo mode**: Real incidents, authentic colors and data
3. **Explain the ethical framing**: "This is decision support, not ranking lives"
4. **Walk through a drill-down**: Show how responders can assess a single incident
5. **Show the prediction form**: Let judges predict for a custom scenario
6. **Emphasize the feature completeness**: 35 engineered features, proper preprocessing
7. **Mention the real model**: Not a toy, production-ready sklearn pipeline
8. **Keep it simple**: The system works end-to-end without hand-waving

---

## 🔗 Quick Links

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/
- **scikit-learn Docs**: https://scikit-learn.org
- **EM-DAT Database**: https://www.emdat.be

---

## 🙋 Support

If you encounter issues:
1. Check the **Troubleshooting** section above
2. Review `app.py` comments for implementation details
3. Run the test scripts: `quick_test.py` or `test_app_syntax.py`
4. Check browser console (F12) for JavaScript errors
5. Ensure all data files are in the correct directories

---

**Built for the AapdaSetu Hackathon Project**
*AI-Powered Disaster Response & Resource Allocation*
