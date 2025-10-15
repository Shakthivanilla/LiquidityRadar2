
import streamlit as st
import re
import numpy as np
import matplotlib.pyplot as plt
from data import fetch_member_data, calculate_risk_metrics
from visualizations import create_monte_carlo_simulation
from ai_utils import get_ai_response
from prompts import get_aquamind_agent_prompt

st.set_page_config(layout='wide')
st.title('Stress Tests & Scenarios')

df = fetch_member_data()
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()
df = calculate_risk_metrics(df)

st.markdown('Simulate shocks to liquidity buffers and view Monte Carlo outcomes.')
shock = st.slider('Stress shock multiplier', 0.5, 3.0, 1.2)
if st.button('Run Stress Simulation'):
    st.info('Running simulation...')
    fig = create_monte_carlo_simulation(df, shock)
    st.pyplot(fig)
    st.caption(f"Simulation run with shock multiplier: {shock}")

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
        try:
            df_string = df.to_string(index=False)
            agent_prompt = get_aquamind_agent_prompt(df_string)
            ai_agent_output = get_ai_response(agent_prompt)

            if ai_agent_output:
                st.success("✅ AquaMind Agent Report Ready")
                st.markdown(ai_agent_output)

                # Extract confidence for visualization
                match = re.search(r"(\d{2,3})\s*%|confidence[:\s]+(\d{1,3})",
                                  ai_agent_output.lower())
                confidence_score = int(match.group(1) or match.group(2)) if match else 85
                st.progress(confidence_score / 100)
                st.caption(f"🧭 AquaMind Confidence Level: {confidence_score}%")

                # Optional: auto-generate quick Monte Carlo visualization
                st.subheader("🎲 Monte Carlo Liquidity Stress Snapshot")
                sims = np.random.normal(df["risk_ratio"].mean(), 0.5, 5000)
                fig, ax = plt.subplots()
                ax.hist(sims, bins=40, color="skyblue", edgecolor="black")
                ax.axvline(2,
                           color="red",
                           linestyle="--",
                           label="High Risk Threshold (2x)")
                ax.set_title("Monte Carlo Simulated Risk Ratios")
                ax.set_xlabel("Simulated Risk Ratio")
                ax.set_ylabel("Frequency")
                ax.legend()
                st.pyplot(fig)
            else:
                st.error("❌ AquaMind could not generate a response.")

        except Exception as e:
            st.error(f"❌ Error running AquaMind Agent: {e}")
