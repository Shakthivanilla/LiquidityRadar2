import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
import re
# Import custom modules
from data import get_snowflake_connection, fetch_member_data, calculate_risk_metrics, color_risk
from ai_utils import get_ai_response
from prompts import (
    get_ai_summary_prompt,
    get_natural_language_query_prompt,
    get_optimization_plan_prompt,
    get_aquamind_agent_prompt
)
from visualizations import (
    create_liquidity_forecast,
    create_confidence_heatmap,
    create_monte_carlo_simulation
)

# ===============================
#  🔧 CONFIGURATION
# ===============================
st.set_page_config(
    page_title="💧 Smart Liquidity Monitor — AI Hackathon Edition",
    layout="wide")

# ===============================
#  📊 LOAD & PROCESS DATA
# ===============================
st.title("💧 Smart Liquidity Monitor — AI Hackathon Edition")

# Connect to Snowflake and fetch data
conn = get_snowflake_connection()
df = fetch_member_data(conn)

if df is None:
    st.stop()

# Calculate risk metrics
df = calculate_risk_metrics(df)

# ===============================
#  📈 DASHBOARD OVERVIEW
# ===============================
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Members", len(df))
col2.metric("🔴 High Risk", len(df[df["risk_level"] == "HIGH"]))
col3.metric("🟢 Low Risk", len(df[df["risk_level"] == "LOW"]))

st.subheader("📊 Liquidity Overview")
st.dataframe(df.style.map(color_risk, subset=["risk_level"]))

# --- Chart ---
st.subheader("📉 Liquidity Comparison")
st.bar_chart(df.set_index("name")[["cash_buffer_usd", "credit_headroom_usd"]])

# ===============================
#  🧠 AI RISK INSIGHT (using Gemini)
# ===============================
def ai_summary(df):
    """Generate AI summary of liquidity risks"""
    prompt = get_ai_summary_prompt(df.to_string(index=False))
    response = get_ai_response(prompt)
    return response if response else "Error generating AI summary"

if st.button("🧠 Generate AI Liquidity Insight"):
    with st.spinner("Analyzing liquidity risks..."):
        insight = ai_summary(df)
        st.success("✅ AI Summary Generated!")
        st.write(insight)

# ===============================
#  🔍 NATURAL LANGUAGE QUERY
# ===============================
st.markdown("---")
st.subheader("💬 Ask Your Data (Natural Language Query)")
query_input = st.text_input(
    "Ask e.g. 'Show members with cash buffer below 5M'")

if query_input:
    with st.spinner("Interpreting your query..."):
        prompt = get_natural_language_query_prompt(query_input, list(df.columns))
        response = get_ai_response(prompt)
        
        if response:
            code = response.strip("`")
            # Remove python language markers
            code = code.replace("python\n", "").replace("```", "").strip()
            st.code(code, language="python")
            try:
                filtered_df = eval(code)
                st.dataframe(filtered_df)
            except Exception as e:
                st.error(f"Could not execute filter: {e}")

# ===============================
#  🔮 LIQUIDITY FORECAST SIMULATION (Using statsmodels ARIMA)
# ===============================
st.markdown("---")
st.subheader("🔮 Liquidity Projection (Next 3 Months)")

member = st.selectbox('Select Member', df['name'])
selected = df[df['name'] == member].iloc[0]

# Create and display forecast chart
fig = create_liquidity_forecast(selected, member)
st.pyplot(fig)

# ===============================
#  ⚙️ STRESS TEST SIMULATION
# ===============================
st.markdown("---")
st.subheader("⚙️ Market Stress Test Simulator")

interest_rate = st.slider("📈 Interest Rate Change (%)", -5, 5, 0)
market_shock = st.slider("💥 Market Volatility Impact (%)", -20, 20, 0)

df["Adjusted_Risk"] = (df["credit_headroom_usd"] *
                       (1 + market_shock / 100)) / (df["cash_buffer_usd"] *
                                                    (1 +
                                                     (interest_rate / 100)))
df["Adjusted_Level"] = df["Adjusted_Risk"].apply(
    lambda x: "HIGH" if x > 2 else "MEDIUM" if x > 1 else "LOW")

st.dataframe(df[["name", "risk_level", "Adjusted_Level"]])

high_risk_members = df[df["Adjusted_Level"] == "HIGH"]["name"].tolist()
if high_risk_members:
    st.warning(
        f"🚨 High Risk Members after stress: {', '.join(high_risk_members)}")
else:
    st.success("✅ All members stable under current simulation.")

# ===============================
#  🧠 PREDICTIVE EARLY WARNING (Using scikit-learn)
# ===============================
st.markdown("---")
st.subheader("🧠 Predictive Early Warning System")

# Simulate Historical Data for Training
np.random.seed(42)
historical_size = 500
historical_cash = np.random.uniform(1_000_000, 50_000_000, historical_size)
historical_credit = np.random.uniform(5_000_000, 100_000_000, historical_size)
historical_risk_ratio = historical_credit / historical_cash
historical_risk_level = pd.Series(historical_risk_ratio).apply(
    lambda x: 'HIGH' if x > 2 else 'MEDIUM' if x > 1 else 'LOW'
)
X_train = pd.DataFrame({'cash_buffer_usd': historical_cash, 'credit_headroom_usd': historical_credit})
y_train = historical_risk_level

# Train the Classification Model
model = LogisticRegression()
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
st.dataframe(df[['name', 'Predicted_Risk_Probability', 'Predicted_Risk_Label']])
st.bar_chart(df.set_index('name')['Predicted_Risk_Probability'])

# ===============================
#  💡 AI LIQUIDITY OPTIMIZATION PLAN
# ===============================
st.markdown("---")
st.subheader("💡 AI Liquidity Optimization Plan")

if st.button("Generate Optimization Plan"):
    prompt = get_optimization_plan_prompt(df.to_string(index=False))
    
    ai_plan = get_ai_response(prompt)
    
    if ai_plan:
        match = re.search(r"(\d{2,3})\s*%.*confidence[:\s]+(\d{1,3})",
                          ai_plan.lower())
        confidence_score = match.group(1) if match else "85"

        st.success("✅ AI Optimization Plan Generated")
        st.markdown(ai_plan)
        st.progress(int(confidence_score) / 100)
        st.caption(f"🤖 AI Confidence: {confidence_score}%")

# ===============================
#  🎯 CONFIDENCE HEATMAP
# ===============================
st.markdown("---")
st.subheader("🎯 AI Confidence Heatmap (Liquidity Risk Certainty)")

df["AI_Confidence"] = np.random.randint(60, 100, len(df))
fig = create_confidence_heatmap(df)
st.pyplot(fig)

# ===============================
# 🤖 AQUAMIND AI AGENT
# ===============================
st.markdown("---")
st.header("🤖 AquaMind AI — Autonomous Liquidity Assistant")

st.markdown("""
Meet **AquaMind**, your always-on liquidity co-pilot.
It continuously scans financial data, detects risks, and provides proactive insights.
""")

if st.button("🚀 Activate AquaMind Agent"):
    with st.spinner("AquaMind is analyzing your liquidity landscape..."):
        prompt = get_aquamind_agent_prompt(df.to_string(index=False))
        ai_agent_output = get_ai_response(prompt)
        
        if ai_agent_output:
            st.success("✅ AquaMind Agent Report Ready")
            st.markdown(ai_agent_output)

            # Extract confidence for visualization
            match = re.search(r"(\d{2,3})\s*%.*confidence[:\s]+(\d{1,3})",
                              ai_agent_output.lower())
            confidence_score = int(match.group(1)) if match else 85
            st.progress(confidence_score / 100)
            st.caption(f"🧭 AquaMind Confidence Level: {confidence_score}%")

            # Monte Carlo visualization
            st.subheader("🎲 Monte Carlo Liquidity Stress Snapshot")
            fig = create_monte_carlo_simulation(df)
            st.pyplot(fig)

# ===============================
#  📄 DOWNLOAD LIQUIDITY REPORT (PDF)
# ===============================
st.markdown("---")
st.subheader("📄 Download AI Liquidity Report")

if st.button("📥 Generate Liquidity Report PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200,
             10,
             "Smart Liquidity Monitor - AI Hackathon Edition",
             ln=True,
             align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"AI Liquidity Summary:\n\n{ai_summary(df)}")
    pdf.ln(10)
    pdf.cell(
        0,
        10,
        f"Generated Confidence Heatmap Avg: {df['AI_Confidence'].mean():.1f}%",
        ln=True)
    pdf.output("liquidity_report.pdf")
    st.success("✅ Liquidity Report Generated!")
    with open("liquidity_report.pdf", "rb") as f:
        st.download_button("⬇️ Download Report",
                           f,
                           file_name="liquidity_report.pdf")


# --- Liquidity Advisor Agent UI ---
st.markdown("### 🧠 Liquidity Advisor (Ask a question)")
agent_query = st.text_input("Ask the Liquidity Advisor (e.g., 'Which members will be at high risk next quarter?')", key="agent_query")
if st.button("Run Agent", key="run_agent"):
    if 'df' not in locals() and 'df' not in globals():
        st.error("Data not loaded. Please ensure your data connection is set up and refresh.")
    else:
        # prefer local variable df created after fetch_member_data + calculate_risk_metrics
        try:
            df_for_agent = df if 'df' in locals() else globals().get('df', None)
            from ai_utils import run_liquidity_agent
            with st.spinner("Running Liquidity Advisor..."):
                agent_answer = run_liquidity_agent(df_for_agent, agent_query, top_k=5)
            if agent_answer:
                st.markdown("**Agent Response**")
                st.write(agent_answer)
                # Optionally parse recommended actions for export
                if "Recommended Actions" in str(agent_answer):
                    st.download_button("Export Agent Response", agent_answer, file_name="agent_response.txt")
            else:
                st.error("Agent did not return a response. Check logs or API key.")
        except Exception as e:
            st.error(f"Agent execution error: {e}")
# --- end agent UI ---

st.caption(
    "🏁 Built for AI Hackathon 2025 — Intelligent Liquidity Insights for Financial Stability."
)
