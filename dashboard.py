import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime
import os
import dash_auth
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Data loading functions
def load_jsonl_data(filepath):
    """Load JSONL data into a list of dictionaries."""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except FileNotFoundError:
        logging.warning(f"Data file not found: {filepath}")
    return data

def load_website_metrics():
    """Load website metrics data."""
    data = load_jsonl_data('data/instana/website_metrics.jsonl')
    if data:
        df = pd.DataFrame(data)
        # Expand points into separate rows
        rows = []
        for _, row in df.iterrows():
            website_id = row['website_id']
            for point in row['points']:
                rows.append({
                    'website_id': website_id,
                    'timestamp': datetime.fromtimestamp(point['timestamp'] / 1000),
                    'value': point['value']
                })
        return pd.DataFrame(rows)
    return pd.DataFrame()

def load_synthetic_runs():
    """Load synthetic check runs data."""
    data = load_jsonl_data('data/instana/synthetic_runs.jsonl')
    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    return pd.DataFrame()

def load_logs():
    """Load logs data."""
    data = load_jsonl_data('data/instana/logs.jsonl')
    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    return pd.DataFrame()

def load_mobile_metrics():
    """Load mobile metrics data."""
    data = load_jsonl_data('data/instana/mobile_metrics.jsonl')
    if data:
        rows = []
        for record in data:
            mobile_app_id = record['mobile_app_id']
            for point in record['points']:
                rows.append({
                    'mobile_app_id': mobile_app_id,
                    'timestamp': pd.to_datetime(point['timestamp'], unit='ms'),
                    'crash_rate': point['crash_rate'],
                    'response_time_ms': point['response_time_ms']
                })
        return pd.DataFrame(rows)
    return pd.DataFrame()

def load_mobile_analyze():
    """Load mobile analyze data."""
    data = load_jsonl_data('data/instana/mobile_analyze.jsonl')
    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    return pd.DataFrame()

# Initialize Dash app
app = dash.Dash(__name__, title="Instana Monitoring Dashboard v1.3.0")
server = app.server

# --- Add Authentication from Environment Variables ---
# In production, set these on your hosting platform (e.g., Heroku config vars)
# Example: heroku config:set DASH_USERNAME=myuser DASH_PASSWORD=mypassword
DASH_USERNAME = os.environ.get('DASH_USERNAME', 'admin')
DASH_PASSWORD = os.environ.get('DASH_PASSWORD', 'instana')

VALID_USERNAME_PASSWORD_PAIRS = {DASH_USERNAME: DASH_PASSWORD}

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

# Layout
app.layout = html.Div([
    html.H1("Instana APM Synthetic Monitoring Dashboard", style={'textAlign': 'center'}),

    # Interval component for automatic refresh
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds (60 seconds)
        n_intervals=0
    ),

    # Navigation tabs
    dcc.Tabs(id='tabs', value='overview', children=[
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='Website Monitoring', value='website'),
        dcc.Tab(label='Mobile Monitoring', value='mobile'),
        dcc.Tab(label='Synthetic Checks', value='synthetic'),
        dcc.Tab(label='Logging Analysis', value='logs'),
    ]),

    html.Div(id='tab-content')
])

# Callback to render tab content
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'website':
        return html.Div([
            html.H2("Website Monitoring Dashboard"),
            html.Div([
                dcc.Graph(id='website-uptime-chart'),
                dcc.Graph(id='website-response-time-chart'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Div([
                dcc.Graph(id='website-error-distribution'),
            ])
        ])
    elif tab == 'synthetic':
        return html.Div([
            html.H2("Synthetic Checks Dashboard"),
            html.Div([
                dcc.Graph(id='synthetic-pass-fail-chart'),
                dcc.Graph(id='synthetic-response-time-chart'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Div([
                dcc.Graph(id='synthetic-failure-trends'),
                dcc.Graph(id='synthetic-error-rates'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Div([
                dcc.Graph(id='synthetic-error-threshold'),
            ])
        ])
    elif tab == 'mobile':
        return html.Div([
            html.H2("Mobile Monitoring Dashboard"),
            html.Div([
                dcc.Graph(id='mobile-crash-rate-chart'),
                dcc.Graph(id='mobile-response-time-chart'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Div([
                dcc.Graph(id='mobile-battery-memory-chart'),
            ])
        ])
    elif tab == 'overview':
        return html.Div([
            html.H2("Monitoring Overview Dashboard"),
            html.Div([
                html.Div([
                    html.H3("Website Uptime %"),
                    html.P(id='overview-kpi-uptime', style={'fontSize': '24px', 'color': 'green'})
                ], style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
                html.Div([
                    html.H3("Average Response Time"),
                    html.P(id='overview-kpi-avg-response', style={'fontSize': '24px', 'color': 'blue'})
                ], style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
                html.Div([
                    html.H3("Mobile Crash Rate"),
                    html.P(id='overview-kpi-crash-rate', style={'fontSize': '24px', 'color': 'red'})
                ], style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
                html.Div([
                    html.H3("Synthetic Error Rate"),
                    html.P(id='overview-kpi-error-rate', style={'fontSize': '24px', 'color': 'orange'})
                ], style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
            ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around'}),
            html.Div([
                dcc.Graph(id='overview-website-mobile-comparison'),
                dcc.Graph(id='overview-alert-summary'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Div([
                dcc.Graph(id='overview-system-health'),
                dcc.Graph(id='overview-quick-gauges'),
            ], style={'display': 'flex', 'flexDirection': 'row'})
        ])
    elif tab == 'logs':
        return html.Div([
            html.H2("Logging Analysis Dashboard"),
            dcc.Dropdown(
                id='severity-filter',
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'ERROR', 'value': 'ERROR'},
                    {'label': 'WARN', 'value': 'WARN'},
                    {'label': 'INFO', 'value': 'INFO'},
                    {'label': 'DEBUG', 'value': 'DEBUG'}
                ],
                value='all',
                style={'width': '200px', 'marginBottom': '20px'}
            ),
            html.Div([
                dcc.Graph(id='log-severity-distribution'),
                dcc.Graph(id='log-correlation-analysis'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            dcc.Graph(id='log-timeline'),
            dcc.Graph(id='log-correlation-scatter')
        ])

# Website monitoring callbacks
@app.callback(
    [Output('website-uptime-chart', 'figure'),
     Output('website-response-time-chart', 'figure'),
     Output('website-error-distribution', 'figure')],
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_website_charts(tab, n):
    if tab != 'website':
        return {}, {}, {}

    df = load_website_metrics()
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No website metrics data available", showarrow=False)
        return empty_fig, empty_fig, empty_fig

    # Uptime chart (simplified - assuming response time < 5000ms means up)
    df['status'] = df['value'].apply(lambda x: 'Up' if x < 5000 else 'Down')
    uptime_df = df.groupby([df['timestamp'].dt.date, 'website_id'])['status'].apply(lambda x: (x == 'Up').mean() * 100).reset_index()

    uptime_fig = px.line(uptime_df, x='timestamp', y='status', color='website_id',
                        title='Website Uptime Percentage', labels={'status': 'Uptime %'})

    # Response time chart
    response_fig = px.line(df, x='timestamp', y='value', color='website_id',
                          title='Response Time Trends (ms)', labels={'value': 'Response Time (ms)'})

    # Error distribution (response time > 3000ms considered error)
    df['error'] = df['value'] > 3000
    error_dist = df.groupby('website_id')['error'].mean().reset_index()
    error_fig = px.bar(error_dist, x='website_id', y='error',
                      title='Error Rate by Website', labels={'error': 'Error Rate'})

    return uptime_fig, response_fig, error_fig

# Synthetic checks callbacks
@app.callback(
    [Output('synthetic-pass-fail-chart', 'figure'),
     Output('synthetic-response-time-chart', 'figure'),
     Output('synthetic-failure-trends', 'figure'),
     Output('synthetic-error-rates', 'figure'),
     Output('synthetic-error-threshold', 'figure')],
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_synthetic_charts(tab, n):
    if tab != 'synthetic':
        return {}, {}, {}, {}, {}

    df = load_synthetic_runs()
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No synthetic runs data available", showarrow=False)
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # Pass/Fail chart
    pass_fail = df.groupby(df['timestamp'].dt.date)['status'].value_counts().unstack().fillna(0)
    pass_fail_fig = px.bar(pass_fail, title='Synthetic Check Pass/Fail Counts',
                          labels={'value': 'Count', 'timestamp': 'Date'})

    # Response time chart
    success_df = df[df['status'] == 'success']
    response_fig = px.line(success_df, x='timestamp', y='duration_ms', color='check_id',
                          title='Synthetic Check Response Times')

    # Failure trends (rolling failure count)
    failure_df = df[df['status'] == 'failure']
    failure_trends = failure_df.groupby([failure_df['timestamp'].dt.date, 'check_id']).size().reset_index(name='failures')
    failure_fig = px.line(failure_trends, x='timestamp', y='failures', color='check_id',
                         title='Synthetic Check Failure Windows')

    # Error rates (failure rate over time)
    error_rates = df.groupby(df['timestamp'].dt.date)['status'].apply(lambda x: (x == 'failure').mean()).reset_index(name='error_rate')
    error_fig = px.line(error_rates, x='timestamp', y='error_rate',
                       title='Synthetic Check Error Rates Over Time', labels={'error_rate': 'Error Rate'})

    # Error rate threshold gauge
    current_error_rate = df['status'].apply(lambda x: 1 if x == 'failure' else 0).mean() * 100
    threshold_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_error_rate,
        title={'text': "Current Error Rate %"},
        gauge={'axis': {'range': [0, 100]}, 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 5}}
    ))

    return pass_fail_fig, response_fig, failure_fig, error_fig, threshold_fig

# Logging callbacks
@app.callback(
    [Output('log-severity-distribution', 'figure'),
     Output('log-correlation-analysis', 'figure'),
     Output('log-timeline', 'figure'),
     Output('log-correlation-scatter', 'figure')],
    [Input('tabs', 'value'),
     Input('severity-filter', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_log_charts(tab, severity, n):
    if tab != 'logs':
        return {}, {}, {}, {}

    df = load_logs()
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No logs data available", showarrow=False)
        return empty_fig, empty_fig, empty_fig, empty_fig

    if severity != 'all':
        df = df[df['severity'] == severity]

    # Severity distribution
    severity_counts = df['severity'].value_counts()
    severity_fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                         title='Log Severity Distribution')

    # Correlation analysis (correlation IDs)
    corr_counts = df['correlation_id'].value_counts().head(10)
    corr_fig = px.bar(x=corr_counts.index, y=corr_counts.values,
                     title='Top Correlation IDs', labels={'x': 'Correlation ID', 'y': 'Count'})

    # Log timeline
    timeline_df = df.groupby([df['timestamp'].dt.hour, 'severity']).size().reset_index(name='count')
    timeline_fig = px.line(timeline_df, x='timestamp', y='count', color='severity',
                          title='Log Events by Hour and Severity')

    # Correlation scatter plot (linking synthetic runs to logs)
    # For simplicity, we'll plot correlation_id vs timestamp
    scatter_fig = px.scatter(df, x='timestamp', y='correlation_id', color='severity',
                            title='Correlation IDs Over Time', labels={'correlation_id': 'Correlation ID'})
    return severity_fig, corr_fig, timeline_fig, scatter_fig

# Mobile monitoring callbacks
@app.callback(
    [Output('mobile-crash-rate-chart', 'figure'),
     Output('mobile-response-time-chart', 'figure'),
     Output('mobile-battery-memory-chart', 'figure')],
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_mobile_charts(tab, n):
    if tab != 'mobile':
        return {}, {}, {}

    df = load_mobile_metrics()
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No mobile metrics data available", showarrow=False)
        return empty_fig, empty_fig, empty_fig

    # Crash rate chart
    crash_fig = px.line(df, x='timestamp', y='crash_rate', color='mobile_app_id',
                       title='Mobile App Crash Rate Trends', labels={'crash_rate': 'Crash Rate'})

    # Response time chart
    response_fig = px.line(df, x='timestamp', y='response_time_ms', color='mobile_app_id',
                          title='Mobile App Response Time Trends (ms)', labels={'response_time_ms': 'Response Time (ms)'})

    # Battery and memory usage chart (stacked bar for consumption trends)
    analyze_df = load_mobile_analyze()
    if not analyze_df.empty:
        battery_memory_fig = go.Figure()
        battery_memory_fig.add_trace(go.Bar(name='Battery Drain %', x=analyze_df['mobile_app_id'], y=analyze_df['battery_drain_percent'], marker_color='orange'))
        battery_memory_fig.add_trace(go.Bar(name='Memory Usage (MB)', x=analyze_df['mobile_app_id'], y=analyze_df['memory_usage_mb'], marker_color='blue'))
        battery_memory_fig.update_layout(
            title='Mobile App Battery and Memory Consumption',
            barmode='stack',
            xaxis_title='Mobile App ID',
            yaxis_title='Consumption'
        )
    else:
        battery_memory_fig = go.Figure()
        battery_memory_fig.add_annotation(text="No mobile analyze data available", showarrow=False)

    return crash_fig, response_fig, battery_memory_fig

# Callback for Overview KPIs
@app.callback(
    [Output('overview-kpi-uptime', 'children'),
     Output('overview-kpi-avg-response', 'children'),
     Output('overview-kpi-crash-rate', 'children'),
     Output('overview-kpi-error-rate', 'children')],
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_overview_kpis(tab, n):
    if tab != 'overview':
        return "...", "...", "...", "..."

    # Load data
    website_df = load_website_metrics()
    mobile_df = load_mobile_metrics()
    synthetic_df = load_synthetic_runs()

    # Calculate KPIs
    uptime = "N/A"
    if not website_df.empty:
        uptime_val = (website_df['value'] < 5000).mean() * 100
        uptime = f"{uptime_val:.2f}%"

    avg_response = "N/A"
    if not website_df.empty:
        avg_response = f"{website_df['value'].mean():.0f} ms"

    crash_rate = "N/A"
    if not mobile_df.empty:
        crash_rate = f"{mobile_df['crash_rate'].mean() * 100:.3f}%"

    error_rate = "N/A"
    if not synthetic_df.empty:
        error_rate = f"{(synthetic_df['status'] == 'failure').mean() * 100:.2f}%"

    return uptime, avg_response, crash_rate, error_rate

# Overview callbacks
@app.callback(
    [Output('overview-website-mobile-comparison', 'figure'),
     Output('overview-alert-summary', 'figure'),
     Output('overview-system-health', 'figure'),
     Output('overview-quick-gauges', 'figure')],
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_overview_charts(tab, n):
    if tab != 'overview':
        return {}, {}, {}, {}

    # Load data
    website_df = load_website_metrics()
    mobile_df = load_mobile_metrics()
    synthetic_df = load_synthetic_runs()
    logs_df = load_logs()

    # Website vs Mobile comparison
    comparison_fig = go.Figure()

    if not website_df.empty:
        website_avg = website_df.groupby(website_df['timestamp'].dt.date)['value'].mean().reset_index()
        comparison_fig.add_trace(go.Scatter(x=website_avg['timestamp'], y=website_avg['value'],
                                          mode='lines+markers', name='Website Response Time'))

    if not mobile_df.empty:
        mobile_avg = mobile_df.groupby(mobile_df['timestamp'].dt.date)['response_time_ms'].mean().reset_index()
        comparison_fig.add_trace(go.Scatter(x=mobile_avg['timestamp'], y=mobile_avg['response_time_ms'],
                                          mode='lines+markers', name='Mobile Response Time'))

    comparison_fig.update_layout(title='Website vs Mobile Response Time Comparison',
                               xaxis_title='Date', yaxis_title='Response Time (ms)')

    # Alert summary (simplified - count failures)
    alert_fig = go.Figure()

    if not synthetic_df.empty:
        failure_count = len(synthetic_df[synthetic_df['status'] == 'failure'])
        success_count = len(synthetic_df[synthetic_df['status'] == 'success'])
        alert_fig.add_trace(go.Bar(x=['Success', 'Failure'], y=[success_count, failure_count],
                                 marker_color=['green', 'red']))

    alert_fig.update_layout(title='Synthetic Check Alert Summary')

    # System health overview
    health_fig = go.Figure()

    # Website health
    if not website_df.empty:
        website_health = (website_df['value'] < 5000).mean() * 100
        health_fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=website_health,
            title={'text': "Website Uptime %"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}},
            domain={'x': [0, 0.5], 'y': [0, 1]}
        ))

    # Mobile health (crash rate < 0.05)
    if not mobile_df.empty:
        mobile_health = (mobile_df['crash_rate'] < 0.05).mean() * 100
        health_fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=mobile_health,
            title={'text': "Mobile Stability %"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "blue"}},
            domain={'x': [0.5, 1], 'y': [0, 1]}
        ))

    health_fig.update_layout(title='System Health Overview')

    # Quick Gauges for Synthetic Success and Log Errors
    quick_gauges_fig = go.Figure()

    # Synthetic Success Rate
    if not synthetic_df.empty:
        synthetic_success_rate = (synthetic_df['status'] == 'success').mean() * 100
        quick_gauges_fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=synthetic_success_rate,
            title={'text': "Synthetic Success %"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "purple"}},
            domain={'x': [0, 0.5], 'y': [0, 1]}
        ))

    # Log Error Count
    if not logs_df.empty:
        log_error_count = len(logs_df[logs_df['severity'] == 'ERROR'])
        quick_gauges_fig.add_trace(go.Indicator(
            mode="number",
            value=log_error_count,
            title={'text': "Log Errors (Total)"},
            domain={'x': [0.5, 1], 'y': [0, 1]}
        ))

    quick_gauges_fig.update_layout(
        title='Additional Health Indicators',
        grid={'rows': 1, 'columns': 2, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=100, b=10)
    )

    return comparison_fig, alert_fig, health_fig, quick_gauges_fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
