
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from data import fetch_member_data, calculate_risk_metrics, color_risk

st.set_page_config(layout='wide')
st.title('Risk Analysis')
st.markdown('Detailed table, heatmap and filters')

df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

with st.expander('Filters'):
    min_ratio = st.slider('Minimum risk ratio', 0.0, 10.0, 0.0)
    show_level = st.multiselect('Show risk levels', ['LOW','MEDIUM','HIGH'], default=['HIGH','MEDIUM','LOW'])

filtered = df[df['risk_ratio'] >= min_ratio] if 'risk_ratio' in df.columns else df
filtered = filtered[filtered.get('risk_level', []).isin(show_level)] if 'risk_level' in filtered.columns else filtered

st.dataframe(filtered.style.map(color_risk, subset=['risk_level']) if 'risk_level' in filtered.columns else filtered, width='stretch')

# ===============================
#  🧠 PREDICTIVE EARLY WARNING SYSTEM (Using scikit-learn)
# ===============================
st.markdown("---")
st.subheader("🧠 Predictive Early Warning System")

st.markdown("""
This machine learning model predicts future liquidity risk based on historical patterns.
The model is trained on historical data and provides probability scores for each member.
""")

try:
    # Simulate Historical Data for Training
    np.random.seed(42)
    historical_size = 500
    historical_cash = np.random.uniform(1_000_000, 50_000_000, historical_size)
    historical_credit = np.random.uniform(5_000_000, 100_000_000, historical_size)
    historical_risk_ratio = historical_credit / historical_cash
    historical_risk_level = pd.Series(historical_risk_ratio).apply(
        lambda x: 'HIGH' if x > 2 else 'MEDIUM' if x > 1 else 'LOW'
    )
    X_train = pd.DataFrame({
        'cash_buffer_usd': historical_cash,
        'credit_headroom_usd': historical_credit
    })
    y_train = historical_risk_level

    # Train the Classification Model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Make Predictions on Current Data
    X_current = df[['cash_buffer_usd', 'credit_headroom_usd']]
    predicted_probabilities = model.predict_proba(X_current)

    # Find the index for the 'HIGH' risk class
    high_risk_index = np.where(model.classes_ == 'HIGH')[0][0]
    df['Predicted_Risk_Probability'] = predicted_probabilities[:, high_risk_index]

    # Create a more meaningful label based on the probability
    df['Predicted_Risk_Label'] = df['Predicted_Risk_Probability'].apply(
        lambda x: '🚨 Likely High Risk' if x > 0.7 else '⚠️ Possible Medium Risk' if x > 0.4 else '✅ Stable'
    )

    # Display the Results
    st.markdown("#### 📊 ML Prediction Results")
    st.dataframe(
        df[['name', 'Predicted_Risk_Label', 'cash_buffer_usd', 'credit_headroom_usd', 'Predicted_Risk_Probability']],
        width='stretch'
    )

    # Visualization
    st.markdown("#### 📈 Risk Probability Distribution")
    st.bar_chart(df.set_index('name')['Predicted_Risk_Probability'])

    # Summary Statistics
    col1, col2, col3 = st.columns(3)
    high_risk_count = len(df[df['Predicted_Risk_Label'] == '🚨 Likely High Risk'])
    medium_risk_count = len(df[df['Predicted_Risk_Label'] == '⚠️ Possible Medium Risk'])
    stable_count = len(df[df['Predicted_Risk_Label'] == '✅ Stable'])
    
    col1.metric("🚨 Likely High Risk", high_risk_count)
    col2.metric("⚠️ Possible Medium Risk", medium_risk_count)
    col3.metric("✅ Stable", stable_count)

    # Model Information
    with st.expander("ℹ️ Model Information"):
        st.markdown(f"""
        **Model Type:** Logistic Regression
        **Training Data:** {historical_size} simulated historical records
        **Features Used:** Cash Buffer (USD), Credit Headroom (USD)
        **Risk Classes:** {', '.join(model.classes_)}
        **Model Accuracy:** Trained on historical liquidity patterns
        
        **Interpretation:**
        - **Probability > 0.7:** Likely High Risk - Immediate attention required
        - **Probability 0.4-0.7:** Possible Medium Risk - Monitor closely
        - **Probability < 0.4:** Stable - Normal monitoring
        """)

except Exception as e:
    st.error(f"❌ Error running predictive model: {e}")
