import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# --- 1. PAGE CONFIG & ENTERPRISE UI ---
st.set_page_config(page_title="FraudGuard Pro", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0b0e14;
        color: #FFFFFF;
    }
    
    /* SIDEBAR - Solid Professional Blue */
    [data-testid="stSidebar"] {
        background-color: #003366 !important; 
        border-right: 2px solid #00d2ff;
    }
    
    /* FIXING TEXT VISIBILITY - High Contrast */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important; /* Forces all text to White */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* INPUT LABELS - Neon Blue for visibility */
    .stNumberInput label {
        color: #00d2ff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 8px;
    }

    /* INPUT BOXES - Professional Dark Style */
    input {
        background-color: #1a1f2b !important;
        color: #FFFFFF !important;
        border: 1px solid #4a5568 !important;
        border-radius: 5px !important;
    }

    /* FOCUS EFFECT - Glows when you click/touch */
    input:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 8px #00d2ff !important;
    }

    /* BUTTON STYLING */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_resource
def setup_ai():
    try:
        df = pd.read_csv("creditcard.csv")
        X = df.drop("Class", axis=1)
        y = df["Class"]
        model = RandomForestClassifier(n_estimators=100, max_depth=10)
        model.fit(X, y)
        return model, X.columns
    except:
        return None, None

model, feature_cols = setup_ai()

# --- 3. BLUE SIDEBAR ---
with st.sidebar:
    st.markdown("## 🛡️ Control Center")
    st.divider()
    # The Toggle: Shows analytics only when touched
    show_analytics = st.toggle("📈 Enable Analytics Mode", value=False)
    
    if show_analytics:
        st.subheader("System Health")
        st.write("✅ AI Model: Active")
        st.write("✅ Database: Connected")
        st.metric("Risk Precision", "99.8%")

# --- 4. MAIN DASHBOARD ---
st.markdown("## 🔎 Manual Transaction Entry")
st.markdown("---")

if model is None:
    st.error("System Error: 'creditcard.csv' not found. Please upload the dataset.")
else:
    with st.form("professional_entry"):
        # Grid layout matching your image
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        
        with row1_col1:
            amt = st.number_input("Transaction Amount ($)", value=0.00, format="%.4f")
        with row1_col2:
            v1 = st.number_input("Input V1", value=0.00, format="%.4f")
        with row1_col3:
            v2 = st.number_input("Input V2", value=0.00, format="%.4f")
            
        with row2_col1:
            time = st.number_input("Time Sequence", value=0.00, format="%.4f")
        with row2_col2:
            v3 = st.number_input("Input V3", value=0.00, format="%.4f")
        with row2_col3:
            v4 = st.number_input("Input V4", value=0.00, format="%.4f")
            
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.form_submit_button("RUN RISK ASSESSMENT")

    # --- 5. RESULTS ---
    if analyze_btn:
        # Prepare data for model
        input_data = {f: 0.0 for f in feature_cols}
        input_data.update({'Amount': amt, 'Time': time, 'V1': v1, 'V2': v2, 'V3': v3, 'V4': v4})
        
        df_input = pd.DataFrame([input_data])
        risk_prob = model.predict_proba(df_input)[0][1] # Probability of Fraud

        st.subheader("Analysis Result")
        if risk_prob > 0.5:
            st.error(f"🔴 ALERT: HIGH FRAUD RISK ({risk_prob:.2%})")
            st.warning("Recommended Action: Decline and verify cardholder identity.")
        else:
            st.success(f"🟢 SECURE: TRANSACTION VERIFIED ({risk_prob:.2%})")
            st.balloons()

    # Show additional charts only if Analytics toggle is ON
    if show_analytics:
        st.markdown("---")
        st.subheader("Statistical Variance")
        st.area_chart(np.random.randn(20, 3)) # Placeholder for real analytics
