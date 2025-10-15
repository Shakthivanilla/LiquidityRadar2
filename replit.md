# Smart Liquidity Monitor — AI Hackathon Edition

## Overview

Smart Liquidity Monitor is an AI-powered liquidity risk monitoring and forecasting application built for financial institutions. The system analyzes member liquidity positions, provides predictive early warnings for liquidity risks, and generates time-series forecasts using machine learning models. The application combines real-time data analytics with AI-driven insights to help financial teams make informed decisions about liquidity management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Code Structure (Modular Multi-Page Architecture)
The application follows a modular multi-page architecture with separation of concerns:
- **app.py**: Landing page with branding and navigation
- **pages/**: Multi-page Streamlit structure
  - **1_Overview.py**: Dashboard with metrics and forecasts
  - **2_Risk_Analysis.py**: Detailed risk analysis with filters
  - **3_AI_Insights.py**: AI-powered insights and natural language queries
  - **4_Stress_Test.py**: Monte Carlo simulations and stress testing
  - **5_Reports.py**: Report generation and data export
  - **6_Settings.py**: Configuration and preferences management
- **data.py**: Snowflake connection management and data processing utilities (auto-creates connections internally)
- **ai_utils.py**: Centralized Gemini AI helper functions (get_ai_response, run_liquidity_agent) for all AI interactions
- **prompts.py**: Centralized AI prompt templates for consistency and maintainability
- **visualizations.py**: Reusable chart and plot generation functions (ARIMA forecasts, heatmaps, Monte Carlo simulations)
- **redis_cache.py**: User preferences caching with Redis fallback to local JSON file
- **assets/**: Static assets (logo, CSS, Lottie animations, background images)

### Frontend Architecture
- **Framework**: Streamlit multi-page web application with sci-fi themed UI
- **Layout**: Wide layout configuration for dashboard-style data visualization
- **UI Theme**: Custom sci-fi/futuristic design with:
  - Custom CSS styling (assets/style.css)
  - Lottie animations for interactive headers (streamlit-lottie)
  - Background images and custom logo
  - Sci-fi color scheme and visual effects
- **UI Components**: Interactive data tables, charts, member selection dropdowns, and risk visualization panels
- **Visualization**: Matplotlib and NumPy for chart generation and data plotting
- **Page Navigation**: Sidebar-based navigation between Overview, Risk Analysis, AI Insights, Stress Tests, Reports, and Settings

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
- **Caching & Preferences**:
  - Redis for user preferences (when REDIS_URL is configured)
  - Fallback to local JSON file (assets/preferences.json) when Redis unavailable
  - Streamlit @st.cache_data (5-min TTL) for database queries
  - Streamlit @st.cache_resource for Snowflake connections

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
- **Web Framework**: 
  - streamlit: Multi-page web application development
  - streamlit-lottie: Lottie animation integration for UI enhancement
- **Caching**: 
  - redis: User preferences persistence (optional, falls back to JSON)

### Development Notes
- The application simulates historical data for demonstration purposes when actual historical data is unavailable
- ARIMA model parameters (2,1,1) are baseline settings that can be tuned for production accuracy
- Risk classification uses simulated training data (500 samples) to demonstrate ML capabilities
- Environment-based configuration enables seamless deployment across development and production environments
- Multi-page architecture provides modular separation of concerns and improved user navigation
- Custom sci-fi UI theme with Lottie animations creates an engaging, futuristic user experience
- Redis caching is optional - application automatically falls back to local JSON file for preferences

## Recent Changes (October 14, 2025)

### SciFi UI Transformation
- **Multi-Page Structure**: Converted from monolithic to multi-page Streamlit app with 6 pages
- **Sci-Fi Theme**: Added futuristic UI with custom CSS, background images, and logo
- **Lottie Animations**: Integrated streamlit-lottie for animated headers
- **Redis Caching**: Added redis_cache.py for user preferences with JSON fallback
- **Data Module Update**: Updated fetch_member_data() to create connections internally
- **Page Features**:
  - Overview: Dashboard with key metrics and liquidity forecasts
  - Risk Analysis: Detailed filtering and data tables
  - AI Insights: Natural language queries with Gemini AI
  - Stress Test: Monte Carlo simulations for risk scenarios
  - Reports: CSV export functionality
  - Settings: User preferences and configuration management

### Dark Theme Implementation
- **Color Palette**: Deep dark theme with vibrant cyan/blue accents
  - Background: #0a0e1a to #000000 (dark gradients)
  - Text: #e0e5ea (light gray for readability)
  - Primary Accent: #00f5ff (cyan)
  - Secondary Accent: #0077ff (blue)
- **Components**: All UI elements styled for dark theme
  - Dark metric cards with light text
  - Dark data tables with bright risk indicators
  - Dark charts with vibrant data visualization
  - Transparent overlays for risk levels (red, amber, green)
- **Typography**: Orbitron font with sci-fi aesthetic and cyan glow effects