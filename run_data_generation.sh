#!/bin/bash

# Instana Synthetic Data Generation Script
# This script generates all synthetic monitoring data for the Instana platform

echo "Starting Instana synthetic data generation..."

# Set Python path
export PYTHONPATH="${PYTHONPATH}:."

# Generate all data
python scripts/generate_instana_all.py

# Export metrics to Prometheus format
echo "Exporting metrics to Prometheus format..."
python -c "from prometheus_exporter import export_all_metrics_to_prometheus; export_all_metrics_to_prometheus('data/exports/all_metrics.prom')"

echo "Data generation and export complete!"
