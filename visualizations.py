"""
Visualization Functions for Smart Liquidity Monitor
Chart and plot generation utilities
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
from typing import Tuple
from matplotlib.figure import Figure

warnings.filterwarnings("ignore")  # Suppress ARIMA warnings

def create_liquidity_forecast(selected_member_data: pd.Series, member_name: str) -> Figure:
    """
    Create ARIMA-based liquidity forecast chart with dark theme
    
    Args:
        selected_member_data: Series with member data (cash_buffer_usd, credit_headroom_usd)
        member_name: Name of the selected member
    
    Returns:
        matplotlib.figure.Figure: Forecast chart figure
    """
    # Set dark theme for matplotlib
    import matplotlib
    matplotlib.rcParams.update({
        'figure.facecolor': '#0a0e1a',
        'axes.facecolor': '#0a1520',
        'axes.edgecolor': '#00f5ff',
        'axes.labelcolor': '#e0e5ea',
        'text.color': '#e0e5ea',
        'xtick.color': '#e0e5ea',
        'ytick.color': '#e0e5ea',
        'grid.color': '#1a2530',
        'grid.alpha': 0.3
    })
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
    
    # Display the Chart with dark theme
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, cash_forecast, marker='o', label='Cash Buffer Forecast', color='#00f5ff', linewidth=2, markersize=8)
    ax.plot(months, credit_forecast, marker='s', label='Credit Headroom Forecast', color='#ffc107', linewidth=2, markersize=8)
    ax.set_ylabel('USD', color='#e0e5ea', fontsize=11)
    ax.set_title(f'Projected Liquidity for {member_name}', color='#00f5ff', fontsize=14, pad=15)
    ax.legend(facecolor='#0a1520', edgecolor='#00f5ff', framealpha=0.9, labelcolor='#e0e5ea')
    ax.grid(True, linestyle='--', alpha=0.3, color='#1a2530')
    
    return fig

def create_confidence_heatmap(df: pd.DataFrame) -> Figure:
    """
    Create AI confidence heatmap with dark theme
    
    Args:
        df: DataFrame with member data and AI_Confidence column
    
    Returns:
        matplotlib.figure.Figure: Heatmap figure
    """
    fig, ax = plt.subplots(figsize=(6, 2 + len(df) * 0.3))
    fig.patch.set_facecolor('#0a0e1a')
    ax.set_facecolor('#0a1520')
    ax.barh(df["name"],
            df["AI_Confidence"],
            color=plt.cm.coolwarm(df["AI_Confidence"] / 100))
    ax.set_xlim(0, 100)
    ax.set_xlabel("AI Confidence (%)", color='#e0e5ea')
    ax.set_title("Model Certainty in Liquidity Risk Assessment", color='#00f5ff', fontsize=12)
    ax.tick_params(colors='#e0e5ea')
    
    return fig

def create_monte_carlo_simulation(df: pd.DataFrame, shock_multiplier: float = 1.0) -> Figure:
    """
    Create Monte Carlo liquidity stress simulation with dark theme
    
    Args:
        df: DataFrame with risk_ratio column
        shock_multiplier: Stress shock multiplier to apply to mean (default: 1.0)
    
    Returns:
        matplotlib.figure.Figure: Monte Carlo simulation figure
    """
    sims = np.random.normal(df["risk_ratio"].mean() * shock_multiplier, 0.5, 5000)
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0a0e1a')
    ax.set_facecolor('#0a1520')
    ax.hist(sims, bins=40, color="#00f5ff", edgecolor="#0077ff", alpha=0.7)
    ax.axvline(2,
               color="#ff6666",
               linestyle="--",
               linewidth=2,
               label="High Risk Threshold (2x)")
    ax.set_title("Monte Carlo Simulated Risk Ratios", color='#00f5ff', fontsize=14, pad=15)
    ax.set_xlabel("Simulated Risk Ratio", color='#e0e5ea', fontsize=11)
    ax.set_ylabel("Frequency", color='#e0e5ea', fontsize=11)
    ax.legend(facecolor='#0a1520', edgecolor='#00f5ff', framealpha=0.9, labelcolor='#e0e5ea')
    ax.tick_params(colors='#e0e5ea')
    ax.grid(True, linestyle='--', alpha=0.3, color='#1a2530')
    
    return fig
