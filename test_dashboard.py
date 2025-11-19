#!/usr/bin/env python3
"""
Test script for dashboard functionality.
Tests data loading functions and basic chart generation.
"""

import sys
import os
sys.path.append(os.getcwd())
import pandas as pd

from dashboard import (
    load_mobile_metrics,
    load_mobile_analyze,
    load_website_metrics,
    load_synthetic_runs,
    load_logs
)

def test_load_mobile_metrics():
    """Test loading mobile metrics data."""
    print("Testing load_mobile_metrics...")
    mobile_df = load_mobile_metrics()
    assert isinstance(mobile_df, pd.DataFrame)
    if not mobile_df.empty:
        print(f"Mobile metrics loaded: {len(mobile_df)} rows")
        expected_cols = ['mobile_app_id', 'timestamp', 'crash_rate', 'response_time_ms'] # Corrected expected columns
        assert all(col in mobile_df.columns for col in expected_cols)
    else:
        print("No mobile metrics data to test.")

def test_load_mobile_analyze():
    """Test loading mobile analyze data."""
    print("Testing load_mobile_analyze...")
    analyze_df = load_mobile_analyze()
    assert isinstance(analyze_df, pd.DataFrame)
    if not analyze_df.empty:
        print(f"Mobile analyze loaded: {len(analyze_df)} rows")
        expected_cols = ['mobile_app_id', 'timestamp', 'battery_drain_percent', 'memory_usage_mb'] # Corrected expected columns
        assert all(col in analyze_df.columns for col in expected_cols)
    else:
        print("No mobile analyze data to test.")

def test_load_website_metrics():
    """Test loading website metrics data."""
    print("Testing load_website_metrics...")
    website_df = load_website_metrics()
    assert isinstance(website_df, pd.DataFrame)
    if not website_df.empty:
        print(f"Website metrics loaded: {len(website_df)} rows")
        expected_cols = ['website_id', 'timestamp', 'value']
        assert all(col in website_df.columns for col in expected_cols)
    else:
        print("No website metrics data to test.")

def test_load_synthetic_runs():
    """Test loading synthetic runs data."""
    print("Testing load_synthetic_runs...")
    synthetic_df = load_synthetic_runs()
    assert isinstance(synthetic_df, pd.DataFrame)
    if not synthetic_df.empty:
        print(f"Synthetic runs loaded: {len(synthetic_df)} rows")
        expected_cols = ['check_id', 'timestamp', 'status', 'duration_ms']
        assert all(col in synthetic_df.columns for col in expected_cols)
    else:
        print("No synthetic runs data to test.")

def test_load_logs():
    """Test loading logs data."""
    print("Testing load_logs...")
    logs_df = load_logs()
    assert isinstance(logs_df, pd.DataFrame)
    if not logs_df.empty:
        print(f"Logs loaded: {len(logs_df)} rows")
        expected_cols = ['timestamp', 'severity', 'message', 'correlation_id']
        assert all(col in logs_df.columns for col in expected_cols)
    else:
        print("No logs data to test.")

if __name__ == "__main__":
    test_load_mobile_metrics()
    test_load_mobile_analyze()
    test_load_website_metrics()
    test_load_synthetic_runs()
    test_load_logs()
    print("\nAll data loading tests completed.")
