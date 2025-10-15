# Smart Liquidity Monitor — AI Hackathon Edition

## Overview

Smart Liquidity Monitor is an AI-powered liquidity risk monitoring and forecasting application built for financial institutions. The system analyzes member liquidity positions, provides predictive early warnings for liquidity risks, and generates time-series forecasts using machine learning models. The application combines real-time data analytics with AI-driven insights to help financial teams make informed decisions about liquidity management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Code Structure (Modular Architecture)
The application follows a modular architecture with separation of concerns:
- **app.py**: Main Streamlit application UI and orchestration
- **data.py**: Snowflake connection management and data processing utilities
- **ai_utils.py**: Centralized Gemini AI helper function (get_ai_response) for all AI interactions
- **prompts.py**: Centralized AI prompt templates for consistency and maintainability
- **visualizations.py**: Reusable chart and plot generation functions (ARIMA forecasts, heatmaps, Monte Carlo simulations)

### Frontend Architecture
- **Framework**: Streamlit-based web application
- **Layout**: Wide layout configuration for dashboard-style data visualization
- **UI Components**: Interactive data tables, charts, member selection dropdowns, and risk visualization panels
- **Visualization**: Matplotlib and NumPy for chart generation and data plotting

### Backend Architecture
- **Data Processing**: Pandas for data manipulation and analysis
- **Machine Learning Models**:
  - **Time-Series Forecasting**: ARIMA (AutoRegressive Integrated Moving Average) from statsmodels for liquidity projections
  - **Risk Classification**: Logistic Regression from scikit-learn for early warning predictions
- **AI Integration**: Google Gemini AI client (gemini-2.5-flash model) for natural language processing and advanced analytics
  - Centralized through get_ai_response() helper function
  - All prompts managed in prompts.py for easy refinement
- **Report Generation**: FPDF library for PDF report creation

### Data Storage Solutions
- **Primary Database**: Snowflake cloud data warehouse
- **Database Configuration**:
  - Warehouse: COMPUTE_WH
  - Database: LIQUIDITY_RADAR
  - Schema: HACKATHON
- **Data Model**: Members table containing:
  - member_id: Unique member identifier
  - name: Member name
  - cash_buffer_usd: Available cash reserves
  - exposure_usd: Credit exposure amount
  - updated_at: Last update timestamp
- **Derived Metrics**: credit_headroom_usd (calculated from exposure), risk ratios, and predicted risk probabilities

### Authentication and Authorization
- **Snowflake Credentials**: Environment variable-based authentication
  - SF_USER: Snowflake username
  - SF_PASS: Snowflake password
  - SF_ACCOUNT: Snowflake account identifier
  - SF_DB: Database name (default: LIQUIDITY_RADAR)
  - SF_SCHEMA: Schema name (default: HACKATHON)
- **API Authentication**: GEMINI_API_KEY stored as environment variable for Google Gemini AI access
- **Security Pattern**: All sensitive credentials externalized to environment variables for secure deployment

## External Dependencies

### Cloud Data Warehouse
- **Snowflake**: Primary data storage and query engine
- **Connection**: snowflake-connector-python library for database connectivity
- **Purpose**: Stores member liquidity data, transaction history, and real-time updates

### AI/ML Services
- **Google Gemini AI**: Advanced AI capabilities for natural language understanding and insights generation
- **SDK**: google-genai client library
- **Use Cases**: Conversational analytics, automated report narratives, risk interpretation

### Python Libraries
- **Data Science Stack**:
  - pandas: Data manipulation and analysis
  - numpy: Numerical computing and array operations
  - matplotlib: Data visualization and charting
- **Machine Learning**:
  - scikit-learn: Logistic regression for risk classification
  - statsmodels: ARIMA models for time-series forecasting
- **Reporting**: fpdf for PDF document generation
- **Web Framework**: Streamlit for rapid web application development

### Development Notes
- The application simulates historical data for demonstration purposes when actual historical data is unavailable
- ARIMA model parameters (2,1,1) are baseline settings that can be tuned for production accuracy
- Risk classification uses simulated training data (500 samples) to demonstrate ML capabilities
- Environment-based configuration enables seamless deployment across development and production environments