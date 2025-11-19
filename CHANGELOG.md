 # Changelog
 
 All notable changes to this project will be documented in this file.
 
 ## [1.3.0] - 2025-11-19
 
 ### ✨ Added
 - **Full Monitoring Dashboard**: Interactive, multi-tab dashboard built with Plotly Dash to visualize all monitoring data.
 - **Overview Tab**: At-a-glance KPIs for uptime, crash rates, and system health gauges.
 - **Website & Mobile Monitoring Tabs**: Dedicated views for website and mobile application performance metrics.
 - **Synthetic & Logging Tabs**: In-depth analysis of synthetic check results and log data.
 - **Authentication**: Added Basic Auth to secure the dashboard, with credentials configurable via environment variables.
 - **Automatic Data Refresh**: Implemented a `dcc.Interval` to refresh dashboard data every 60 seconds.
 - **Deployment Configurations**: Added `Procfile`, `requirements.txt`, and `.ebextensions` for seamless deployment to Heroku and AWS.
 - **Alerting System**: A configurable `AlertManager` to send notifications for threshold breaches.
 
 ### ⚙️ Changed
 - Refactored all data loading functions in `dashboard.py` for better error handling and robustness.
 - Updated `README_INSTANA.md` to reflect the project's transformation into a full operational intelligence platform.
 - All data generation scripts now save files directly to the `data/instana/` directory.
 
 ### 🐛 Fixed
 - Corrected file loading logic in `validate_all.py` and `README_INSTANA.md` to handle JSON vs. JSONL formats correctly.
 - Fixed incorrect column name assertions in `test_dashboard.py`.
 
 ## [1.2.0] - 2025-11-18
 ### Added
 - Data generation scripts for Website, Mobile, Logging, and Synthetic Check monitoring.
 - `v1.2.0_CHECKLIST.md` to track feature completion.
 
 ## [1.1.0] - 2025-11-17
 ### Added
 - Initial data generators for core APM datasets, including topologies, alert configs, and catalogs.