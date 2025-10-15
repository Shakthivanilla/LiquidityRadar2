"""
Visualization Functions for Smart Liquidity Monitor
Chart and plot generation utilities
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")  # Suppress ARIMA warnings

def create_liquidity_forecast(selected_member_data, member_name):
    """
    Create ARIMA-based liquidity forecast chart
    
    Args:
        selected_member_data: Series with member data (cash_buffer_usd, credit_headroom_usd)
        member_name: Name of the selected member
    
    Returns:
        matplotlib.figure.Figure: Forecast chart figure
    """
    # Simulate Historical Data for the Selected Member
    np.random.seed(42)
    historical_months = 12
    base_cash = selected_member_data['cash_buffer_usd']
    base_credit = selected_member_data['credit_headroom_usd']
    
    # Generate a series with some trend and noise
    cash_history = pd.Series([base_cash * (1 + 0.01 * i + np.random.normal(0, 0.05)) for i in range(-historical_months, 0)])
    credit_history = pd.Series([base_credit * (1 + 0.008 * i + np.random.normal(0, 0.04)) for i in range(-historical_months, 0)])
    
    # Train ARIMA models and Forecast
    cash_model = ARIMA(cash_history, order=(2, 1, 1)).fit()
    cash_forecast_values = cash_model.forecast(steps=3)
    
    credit_model = ARIMA(credit_history, order=(2, 1, 1)).fit()
    credit_forecast_values = credit_model.forecast(steps=3)
    
    # Combine Current and Forecasted Data for Plotting
    months = ['Current', 'Month 1', 'Month 2', 'Month 3']
    cash_forecast = [base_cash] + list(cash_forecast_values)
    credit_forecast = [base_credit] + list(credit_forecast_values)
    
    # Display the Chart
    fig, ax = plt.subplots()
    ax.plot(months, cash_forecast, marker='o', label='Cash Buffer Forecast')
    ax.plot(months, credit_forecast, marker='o', label='Credit Headroom Forecast')
    ax.set_ylabel('USD')
    ax.set_title(f'Projected Liquidity for {member_name}')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    return fig

def create_confidence_heatmap(df):
    """
    Create AI confidence heatmap
    
    Args:
        df: DataFrame with member data and AI_Confidence column
    
    Returns:
        matplotlib.figure.Figure: Heatmap figure
    """
    fig, ax = plt.subplots(figsize=(6, 2 + len(df) * 0.3))
    ax.barh(df["name"],
            df["AI_Confidence"],
            color=plt.cm.coolwarm(df["AI_Confidence"] / 100))
    ax.set_xlim(0, 100)
    ax.set_xlabel("AI Confidence (%)")
    ax.set_title("Model Certainty in Liquidity Risk Assessment")
    
    return fig

def create_monte_carlo_simulation(df):
    """
    Create Monte Carlo liquidity stress simulation
    
    Args:
        df: DataFrame with risk_ratio column
    
    Returns:
        matplotlib.figure.Figure: Monte Carlo simulation figure
    """
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
    
    return fig
