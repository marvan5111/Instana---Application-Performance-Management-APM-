import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime
import os
import dash_auth
import logging
from anomaly_detector import load_timeseries_with_anomalies
from predictive_analytics import forecast_timeseries
from audit_logger import audit_logger
from sso_connector import sso_connector
from flask import Flask, request, redirect, session, url_for

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Session management for v1.7.0
user_sessions = {}
current_user = {'user_id': 'admin', 'role': 'admin', 'tenant_id': 'default'}

# RBAC Permissions
ROLE_PERMISSIONS = {
    'admin': {'read': True, 'write': True, 'delete': True, 'admin': True},
    'editor': {'read': True, 'write': True, 'delete': False, 'admin': False},
    'viewer': {'read': True, 'write': False, 'delete': False, 'admin': False},
    'operator': {'read': True, 'write': True, 'delete': False, 'admin': False}
}

# Sample users for role switching
SAMPLE_USERS = {
    'admin_user': {'user_id': 'admin_user', 'role': 'admin', 'tenant_id': 'default'},
    'editor_user': {'user_id': 'editor_user', 'role': 'editor', 'tenant_id': 'tenant-1'},
    'viewer_user': {'user_id': 'viewer_user', 'role': 'viewer', 'tenant_id': 'tenant-2'},
    'operator_user': {'user_id': 'operator_user', 'role': 'operator', 'tenant_id': 'default'}
}

def check_permission(user, permission):
    """Check if user has the required permission."""
    if not user:
        return False
    role = user.get('role', 'viewer')
    return ROLE_PERMISSIONS.get(role, {}).get(permission, False)

def get_available_tenants():
    """Get list of available tenants."""
    return ['default', 'tenant-1', 'tenant-2', 'tenant-3']

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

def load_website_metrics(tenant_id=None):
    """Load website metrics data."""
    data = load_jsonl_data('data/instana/website_metrics.jsonl')
    if data:
        df = pd.DataFrame(data)
        # Filter by tenant if specified
        if tenant_id:
            df = df[df.get('tenant_id') == tenant_id]
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

def load_synthetic_runs(tenant_id=None):
    """Load synthetic check runs data."""
    data = load_jsonl_data('data/instana/synthetic_runs.jsonl')
    if data:
        df = pd.DataFrame(data)
        # Filter by tenant if specified
        if tenant_id:
            df = df[df.get('tenant_id') == tenant_id]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    return pd.DataFrame()

def load_logs(tenant_id=None):
    """Load logs data."""
    data = load_jsonl_data('data/instana/logs.jsonl')
    if data:
        df = pd.DataFrame(data)
        # Filter by tenant if specified
        if tenant_id:
            df = df[df.get('tenant_id') == tenant_id]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    return pd.DataFrame()

def load_mobile_metrics(tenant_id=None):
    """Load mobile metrics data."""
    data = load_jsonl_data('data/instana/mobile_metrics.jsonl')
    if data:
        rows = []
        for record in data:
            # Filter by tenant if specified
            if tenant_id and record.get('tenant_id') != tenant_id:
                continue
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

def load_mobile_analyze(tenant_id=None):
    """Load mobile analyze data."""
    data = load_jsonl_data('data/instana/mobile_analyze.jsonl')
    if data:
        df = pd.DataFrame(data)
        # Filter by tenant if specified
        if tenant_id:
            df = df[df.get('tenant_id') == tenant_id]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    return pd.DataFrame()

# Initialize Dash app
app = dash.Dash(__name__, title="Instana Monitoring Dashboard v1.7.0")
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

    # User and Tenant Controls
    html.Div([
        html.Div([
            html.Label("Current User:"),
            dcc.Dropdown(
                id='user-selector',
                options=[{'label': k, 'value': k} for k in SAMPLE_USERS.keys()],
                value='admin_user',
                style={'width': '200px', 'marginRight': '20px'}
            ),
            html.Label("Current Tenant:"),
            dcc.Dropdown(
                id='tenant-selector',
                options=[{'label': t, 'value': t} for t in get_available_tenants()],
                value='default',
                style={'width': '150px', 'marginRight': '20px'}
            ),
            html.Label("Role:"),
            html.Span(id='current-role-display', style={'marginRight': '20px', 'fontWeight': 'bold'}),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
    ]),

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
        dcc.Tab(label='Audit Logs', value='audit', disabled=True),  # Will enable based on permissions
        dcc.Tab(label='Anomaly Detection', value='anomalies'),
        dcc.Tab(label='Predictive Analytics', value='predictions'),
        dcc.Tab(label='Cloud Native', value='cloud'),
    ]),

    html.Div(id='tab-content')
])

# Callback to render tab content
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    # Check permissions for tab access
    if not check_permission(current_user, 'read'):
        return html.Div([
            html.H2("Access Denied"),
            html.P("You do not have permission to view this dashboard.")
        ])

    # Enforce RBAC for specific tabs
    if tab == 'audit' and not check_permission(current_user, 'admin'):
        return html.Div([
            html.H2("Access Denied"),
            html.P("Only administrators can view audit logs.")
        ])

    if tab == 'cloud' and not check_permission(current_user, 'write'):
        return html.Div([
            html.H2("Access Denied"),
            html.P("You need write permissions to access cloud native features.")
        ])

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
    elif tab == 'audit':
        if not check_permission(current_user, 'admin'):
            return html.Div([
                html.H2("Access Denied"),
                html.P("Only administrators can view audit logs.")
            ])
        return html.Div([
            html.H2("Audit Logs Dashboard"),
            dcc.Dropdown(
                id='audit-user-filter',
                options=[{'label': 'All Users', 'value': 'all'}],
                value='all',
                style={'width': '200px', 'marginBottom': '20px'}
            ),
            dcc.Dropdown(
                id='audit-action-filter',
                options=[
                    {'label': 'All Actions', 'value': 'all'},
                    {'label': 'Login', 'value': 'login'},
                    {'label': 'Logout', 'value': 'logout'},
                    {'label': 'View Data', 'value': 'view'},
                    {'label': 'Export Data', 'value': 'export'}
                ],
                value='all',
                style={'width': '200px', 'marginBottom': '20px'}
            ),
            html.Div(id='audit-logs-table'),
            html.Button('Refresh Audit Logs', id='refresh-audit-btn', n_clicks=0)
        ])
    elif tab == 'cloud':
        return html.Div([
            html.H2("Cloud Native Monitoring Dashboard"),
            html.Div([
                dcc.Graph(id='kubernetes-cluster-status'),
                dcc.Graph(id='kubernetes-pod-metrics'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Div([
                dcc.Graph(id='kubernetes-deployment-health'),
                dcc.Graph(id='prometheus-export-status'),
            ], style={'display': 'flex', 'flexDirection': 'row'}),
            html.Button('Export to Prometheus', id='export-prometheus-btn', n_clicks=0,
                       disabled=not check_permission(current_user, 'write')),
            html.Div(id='export-status')
        ])

# This callback was moved to the end

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

    df = load_website_metrics(current_user.get('tenant_id'))
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

    df = load_synthetic_runs(current_user.get('tenant_id'))
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

    df = load_logs(current_user.get('tenant_id'))
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

    df = load_mobile_metrics(current_user.get('tenant_id'))
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
    analyze_df = load_mobile_analyze(current_user.get('tenant_id'))
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
    website_df = load_website_metrics(current_user.get('tenant_id'))
    mobile_df = load_mobile_metrics(current_user.get('tenant_id'))
    synthetic_df = load_synthetic_runs(current_user.get('tenant_id'))

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
    website_df = load_website_metrics(current_user.get('tenant_id'))
    mobile_df = load_mobile_metrics(current_user.get('tenant_id'))
    synthetic_df = load_synthetic_runs(current_user.get('tenant_id'))
    logs_df = load_logs(current_user.get('tenant_id'))

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

# Anomaly detection callbacks
@app.callback(
    [Output('anomaly-entity-filter', 'options'),
     Output('anomaly-timeseries-chart', 'figure'),
     Output('anomaly-score-distribution', 'figure'),
     Output('anomaly-heatmap', 'figure'),
     Output('anomaly-summary-stats', 'figure')],
    [Input('tabs', 'value'),
     Input('anomaly-entity-filter', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_anomaly_charts(tab, selected_entity, n):
    if tab != 'anomalies':
        return [], {}, {}, {}, {}

    anomalous_data = load_anomalous_timeseries()
    if anomalous_data.empty:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No anomaly data available", showarrow=False)
        return [], empty_fig, empty_fig, empty_fig, empty_fig

    # Create entity options
    entities = []
    for record in anomalous_data:
        entity_key = f"{record['entity_id']}_{record['metric_name']}"
        entities.append({'label': entity_key, 'value': entity_key})
    entities = list(set(tuple(e.items()) for e in entities))
    entity_options = [dict(e) for e in entities]

    if not selected_entity and entity_options:
        selected_entity = entity_options[0]['value']

    # Filter data for selected entity
    if selected_entity:
        entity_id, metric_name = selected_entity.split('_', 1)
        filtered_data = [r for r in anomalous_data if r['entity_id'] == entity_id and r['metric_name'] == metric_name]
    else:
        filtered_data = anomalous_data[:1] if anomalous_data else []

    if not filtered_data:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No data for selected entity", showarrow=False)
        return entity_options, empty_fig, empty_fig, empty_fig, empty_fig

    record = filtered_data[0]

    # Timeseries with anomalies
    timeseries_fig = go.Figure()

    # Normal data points
    timestamps = []
    values = []
    for point in record['points']:
        timestamps.append(datetime.fromtimestamp(point['timestamp'] / 1000))
        values.append(point['value'])

    timeseries_fig.add_trace(go.Scatter(
        x=timestamps,
        y=values,
        mode='lines+markers',
        name='Metric Values',
        line=dict(color='blue')
    ))

    # Anomaly points
    if record.get('anomalies'):
        anomaly_timestamps = [datetime.fromtimestamp(a['timestamp'] / 1000) for a in record['anomalies']]
        anomaly_values = [a['value'] for a in record['anomalies']]
        anomaly_scores = [a['anomaly_score'] for a in record['anomalies']]

        timeseries_fig.add_trace(go.Scatter(
            x=anomaly_timestamps,
            y=anomaly_values,
            mode='markers',
            name='Anomalies',
            marker=dict(color='red', size=10, symbol='x')
        ))

    timeseries_fig.update_layout(
        title=f'Anomaly Detection: {selected_entity}',
        xaxis_title='Time',
        yaxis_title='Value'
    )

    # Anomaly score distribution
    if record.get('anomalies'):
        scores = [a['anomaly_score'] for a in record['anomalies']]
        score_fig = px.histogram(scores, nbins=20, title='Anomaly Score Distribution')
        score_fig.update_layout(xaxis_title='Anomaly Score', yaxis_title='Frequency')
    else:
        score_fig = go.Figure()
        score_fig.add_annotation(text="No anomalies detected", showarrow=False)

    # Anomaly heatmap (simplified)
    heatmap_fig = go.Figure()
    heatmap_fig.add_annotation(text="Anomaly Heatmap - Coming Soon", showarrow=False)

    # Summary statistics
    total_points = len(record['points'])
    anomaly_count = len(record.get('anomalies', []))
    anomaly_rate = anomaly_count / total_points if total_points > 0 else 0

    summary_fig = go.Figure()
    summary_fig.add_trace(go.Indicator(
        mode="number",
        value=anomaly_rate * 100,
        title={"text": "Anomaly Rate %"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': 'red'}}
    ))

    return entity_options, timeseries_fig, score_fig, heatmap_fig, summary_fig

# Predictive analytics callbacks
@app.callback(
    [Output('forecast-entity-filter', 'options'),
     Output('forecast-chart', 'figure'),
     Output('forecast-accuracy', 'figure'),
     Output('forecast-trends', 'figure'),
     Output('forecast-confidence', 'figure')],
    [Input('tabs', 'value'),
     Input('forecast-entity-filter', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_forecast_charts(tab, selected_entity, n):
    if tab != 'predictions':
        return [], {}, {}, {}, {}

    forecast_data = load_forecast_data()

    if not forecast_data:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No forecast data available", showarrow=False)
        return [], empty_fig, empty_fig, empty_fig, empty_fig

    # Create entity options
    entity_options = [{'label': k, 'value': k} for k in forecast_data.keys()]

    if not selected_entity and entity_options:
        selected_entity = entity_options[0]['value']

    if selected_entity not in forecast_data:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No forecast data for selected entity", showarrow=False)
        return entity_options, empty_fig, empty_fig, empty_fig, empty_fig

    entity_forecast = forecast_data[selected_entity]

    # Forecast chart
    forecast_fig = go.Figure()

    # Historical data
    if 'historical' in entity_forecast:
        hist_times = [datetime.fromtimestamp(t / 1000) for t in entity_forecast['historical']['timestamps']]
        forecast_fig.add_trace(go.Scatter(
            x=hist_times,
            y=entity_forecast['historical']['values'],
            mode='lines',
            name='Historical',
            line=dict(color='blue')
        ))

    # Forecast data
    if 'forecast' in entity_forecast:
        forecast_times = [datetime.fromtimestamp(t / 1000) for t in entity_forecast['forecast']['timestamps']]
        forecast_fig.add_trace(go.Scatter(
            x=forecast_times,
            y=entity_forecast['forecast']['values'],
            mode='lines',
            name='Forecast',
            line=dict(color='orange', dash='dash')
        ))

        # Confidence intervals
        if 'lower_bound' in entity_forecast['forecast'] and 'upper_bound' in entity_forecast['forecast']:
            forecast_fig.add_trace(go.Scatter(
                x=forecast_times + forecast_times[::-1],
                y=entity_forecast['forecast']['upper_bound'] + entity_forecast['forecast']['lower_bound'][::-1],
                fill='toself',
                fillcolor='rgba(255,165,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval'
            ))

    forecast_fig.update_layout(
        title=f'Predictive Forecast: {selected_entity}',
        xaxis_title='Time',
        yaxis_title='Value'
    )

    # Forecast accuracy (placeholder)
    accuracy_fig = go.Figure()
    accuracy_fig.add_annotation(text="Forecast Accuracy Metrics - Coming Soon", showarrow=False)

    # Forecast trends
    trends_fig = go.Figure()
    trends_fig.add_annotation(text="Trend Analysis - Coming Soon", showarrow=False)

    # Forecast confidence
    confidence_fig = go.Figure()
    confidence_fig.add_annotation(text="Confidence Analysis - Coming Soon", showarrow=False)

    return entity_options, forecast_fig, accuracy_fig, trends_fig, confidence_fig

# Cloud Native callbacks
@app.callback(
    [Output('kubernetes-cluster-status', 'figure'),
     Output('kubernetes-pod-metrics', 'figure'),
     Output('kubernetes-deployment-health', 'figure'),
     Output('prometheus-export-status', 'figure')],
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_cloud_charts(tab, n):
    if tab != 'cloud':
        return {}, {}, {}, {}

    clusters_df = load_kubernetes_clusters()
    deployments_df = load_kubernetes_deployments()
    pods_df = load_kubernetes_pods()

    # Cluster status chart
    if not clusters_df.empty:
        cluster_status = clusters_df['status'].value_counts()
        cluster_fig = px.pie(values=cluster_status.values, names=cluster_status.index,
                           title='Kubernetes Cluster Status Distribution')
    else:
        cluster_fig = go.Figure()
        cluster_fig.add_annotation(text="No Kubernetes cluster data available", showarrow=False)

    # Pod metrics chart
    if not pods_df.empty:
        pod_metrics_fig = go.Figure()
        pod_metrics_fig.add_trace(go.Bar(name='CPU Usage (cores)', x=pods_df['pod_id'], y=pods_df['metrics'].apply(lambda x: x['cpu_usage_cores']), marker_color='blue'))
        pod_metrics_fig.add_trace(go.Bar(name='Memory Usage (MB)', x=pods_df['pod_id'], y=pods_df['metrics'].apply(lambda x: x['memory_usage_mb']), marker_color='green'))
        pod_metrics_fig.update_layout(title='Pod Resource Usage', barmode='group')
    else:
        pod_metrics_fig = go.Figure()
        pod_metrics_fig.add_annotation(text="No Kubernetes pod data available", showarrow=False)

    # Deployment health chart
    if not deployments_df.empty:
        deployment_health = deployments_df['rollout_status'].value_counts()
        deployment_fig = px.bar(x=deployment_health.index, y=deployment_health.values,
                              title='Deployment Rollout Status', labels={'x': 'Status', 'y': 'Count'})
    else:
        deployment_fig = go.Figure()
        deployment_fig.add_annotation(text="No Kubernetes deployment data available", showarrow=False)

    # Prometheus export status (placeholder)
    prometheus_fig = go.Figure()
    prometheus_fig.add_annotation(text="Prometheus Export Status - Ready", showarrow=False)

    return cluster_fig, pod_metrics_fig, deployment_fig, prometheus_fig

@app.callback(
    Output('export-status', 'children'),
    Input('export-prometheus-btn', 'n_clicks')
)
def export_to_prometheus(n_clicks):
    if n_clicks and n_clicks > 0:
        try:
            from prometheus_exporter import export_metrics_to_prometheus
            # Export some sample metrics
            timeseries_data = load_jsonl_data('data/instana/metrics_timeseries.jsonl')
            if timeseries_data:
                export_metrics_to_prometheus(timeseries_data[:10], "data/exports/metrics.prom")
                return "Successfully exported metrics to Prometheus format!"
            else:
                return "No metrics data available for export."
        except Exception as e:
            return f"Export failed: {str(e)}"
    return ""

# Callback for user and tenant switching
@app.callback(
    [Output('tabs', 'children'),
     Output('current-role-display', 'children')],
    [Input('user-selector', 'value'),
     Input('tenant-selector', 'value')]
)
def switch_user_and_tenant(selected_user, selected_tenant):
    global current_user
    if selected_user in SAMPLE_USERS:
        current_user = SAMPLE_USERS[selected_user].copy()
        current_user['tenant_id'] = selected_tenant

    # Log the user switch
    audit_logger.log_action(
        user_id=current_user['user_id'],
        action='user_switch',
        resource_type='dashboard',
        resource_id='user_tenant_switch',
        details={'new_user': current_user['user_id'], 'new_tenant': current_user['tenant_id']},
        tenant_id=current_user['tenant_id']
    )

    # Return updated tabs based on permissions
    tabs = [
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='Website Monitoring', value='website'),
        dcc.Tab(label='Mobile Monitoring', value='mobile'),
        dcc.Tab(label='Synthetic Checks', value='synthetic'),
        dcc.Tab(label='Logging Analysis', value='logs'),
    ]

    if check_permission(current_user, 'admin'):
        tabs.append(dcc.Tab(label='Audit Logs', value='audit'))

    tabs.extend([
        dcc.Tab(label='Anomaly Detection', value='anomalies'),
        dcc.Tab(label='Predictive Analytics', value='predictions'),
        dcc.Tab(label='Cloud Native', value='cloud'),
    ])

    role_display = current_user.get('role', 'viewer').capitalize()

    return tabs, role_display

# Callback for audit logs
@app.callback(
    Output('audit-logs-table', 'children'),
    [Input('tabs', 'value'),
     Input('audit-user-filter', 'value'),
     Input('audit-action-filter', 'value'),
     Input('refresh-audit-btn', 'n_clicks')]
)
def update_audit_logs_table(tab, user_filter, action_filter, n_clicks):
    if tab != 'audit':
        return ""

    # Get audit trail
    audit_trail = audit_logger.get_audit_trail(limit=50)

    # Filter by user and action
    if user_filter != 'all':
        audit_trail = [entry for entry in audit_trail if entry['user_id'] == user_filter]
    if action_filter != 'all':
        audit_trail = [entry for entry in audit_trail if entry['action'] == action_filter]

    # Create table
    if not audit_trail:
        return html.P("No audit logs found.")

    table_header = [
        html.Thead(html.Tr([
            html.Th("Timestamp"),
            html.Th("User"),
            html.Th("Action"),
            html.Th("Resource Type"),
            html.Th("Resource ID"),
            html.Th("Details")
        ]))
    ]

    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(datetime.fromtimestamp(entry['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')),
                html.Td(entry.get('user_id', 'N/A')),
                html.Td(entry.get('action', 'N/A')),
                html.Td(entry.get('resource_type', 'N/A')),
                html.Td(entry.get('resource_id', 'N/A')),
                html.Td(str(entry.get('details', {})))
            ]) for entry in audit_trail
        ])
    ]

    return html.Table(table_header + table_body, style={'width': '100%', 'border': '1px solid #ddd'})

# Add audit logging to tab switches
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content_with_audit(tab):
    # Log tab access
    audit_logger.log_action(
        user_id=current_user['user_id'],
        action='view_tab',
        resource_type='dashboard',
        resource_id=tab,
        tenant_id=current_user['tenant_id']
    )

    # Call the original render_content function
    return render_content(tab)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
