import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import logging
from typing import List, Dict, Tuple, Optional
import json

log = logging.getLogger("anomaly_detector")

class AnomalyDetector:
    def __init__(self, method="isolation_forest", contamination=0.1):
        """
        Initialize anomaly detector.

        Args:
            method: Detection method ('isolation_forest', 'one_class_svm', 'zscore', 'iqr')
            contamination: Expected proportion of outliers (for ML methods)
        """
        self.method = method
        self.contamination = contamination
        self.model = None
        self.scaler = StandardScaler()
        self.baseline_stats = {}

    def fit(self, data: List[float]) -> None:
        """Fit the anomaly detection model on baseline data."""
        if len(data) < 10:
            log.warning("Insufficient data for anomaly detection training")
            return

        data_array = np.array(data).reshape(-1, 1)

        if self.method in ["isolation_forest", "one_class_svm"]:
            # ML-based methods
            scaled_data = self.scaler.fit_transform(data_array)

            if self.method == "isolation_forest":
                self.model = IsolationForest(
                    contamination=self.contamination,
                    random_state=42,
                    n_estimators=100
                )
            else:  # one_class_svm
                self.model = OneClassSVM(
                    nu=self.contamination,
                    kernel='rbf',
                    gamma='scale'
                )

            self.model.fit(scaled_data)

        elif self.method in ["zscore", "iqr"]:
            # Statistical methods - compute baseline statistics
            self.baseline_stats = {
                'mean': np.mean(data),
                'std': np.std(data),
                'q1': np.percentile(data, 25),
                'q3': np.percentile(data, 75)
            }

        log.info(f"Anomaly detector fitted with method: {self.method}")

    def detect_anomalies(self, data: List[float], threshold: float = None) -> List[Tuple[int, float, bool]]:
        """
        Detect anomalies in data.

        Args:
            data: List of metric values
            threshold: Threshold for statistical methods (z-score or IQR multiplier)

        Returns:
            List of tuples: (index, value, is_anomaly)
        """
        if len(data) == 0:
            return []

        if self.method in ["isolation_forest", "one_class_svm"] and self.model is None:
            log.warning("Model not fitted, cannot detect anomalies")
            return [(i, val, False) for i, val in enumerate(data)]

        results = []

        if self.method == "isolation_forest":
            data_array = np.array(data).reshape(-1, 1)
            scaled_data = self.scaler.transform(data_array)
            predictions = self.model.predict(scaled_data)
            scores = self.model.decision_function(scaled_data)

            for i, (val, pred, score) in enumerate(zip(data, predictions, scores)):
                is_anomaly = pred == -1  # -1 indicates anomaly
                anomaly_score = -score  # Convert to positive anomaly score
                results.append((i, val, is_anomaly))

        elif self.method == "one_class_svm":
            data_array = np.array(data).reshape(-1, 1)
            scaled_data = self.scaler.transform(data_array)
            predictions = self.model.predict(scaled_data)

            for i, (val, pred) in enumerate(zip(data, predictions)):
                is_anomaly = pred == -1
                results.append((i, val, is_anomaly))

        elif self.method == "zscore":
            threshold = threshold or 3.0
            mean = self.baseline_stats.get('mean', np.mean(data))
            std = self.baseline_stats.get('std', np.std(data))

            for i, val in enumerate(data):
                z_score = abs((val - mean) / std) if std > 0 else 0
                is_anomaly = z_score > threshold
                results.append((i, val, is_anomaly))

        elif self.method == "iqr":
            threshold = threshold or 1.5
            q1 = self.baseline_stats.get('q1', np.percentile(data, 25))
            q3 = self.baseline_stats.get('q3', np.percentile(data, 75))
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr

            for i, val in enumerate(data):
                is_anomaly = val < lower_bound or val > upper_bound
                results.append((i, val, is_anomaly))

        return results

    def get_anomaly_score(self, value: float) -> float:
        """Get anomaly score for a single value."""
        if self.method in ["isolation_forest", "one_class_svm"] and self.model is not None:
            data_array = np.array([value]).reshape(-1, 1)
            scaled_data = self.scaler.transform(data_array)

            if self.method == "isolation_forest":
                score = self.model.decision_function(scaled_data)[0]
                return -score  # Convert to positive score
            else:
                pred = self.model.predict(scaled_data)[0]
                return 1.0 if pred == -1 else 0.0

        elif self.method == "zscore":
            mean = self.baseline_stats.get('mean', 0)
            std = self.baseline_stats.get('std', 1)
            z_score = abs((value - mean) / std) if std > 0 else 0
            return z_score

        elif self.method == "iqr":
            q1 = self.baseline_stats.get('q1', 0)
            q3 = self.baseline_stats.get('q3', 1)
            iqr = q3 - q1
            if iqr == 0:
                return 0.0
            distance = max(abs(value - q1), abs(value - q3))
            return distance / iqr

        return 0.0

def detect_anomalies_in_timeseries(timeseries_data: List[Dict], method="isolation_forest") -> List[Dict]:
    """
    Detect anomalies in timeseries data.

    Args:
        timeseries_data: List of timeseries records from JSONL
        method: Anomaly detection method

    Returns:
        Enhanced timeseries data with anomaly flags
    """
    if not timeseries_data:
        return []

    # Group by entity and metric
    grouped_data = {}
    for record in timeseries_data:
        key = f"{record['entity_id']}_{record['metric_name']}"
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(record)

    enhanced_data = []

    for key, records in grouped_data.items():
        # Sort by timestamp
        records.sort(key=lambda x: x['timeframe']['from'])

        # Extract values for anomaly detection
        values = []
        for record in records:
            if record['points']:
                values.extend([point['value'] for point in record['points']])

        if len(values) < 10:
            # Not enough data, mark all as non-anomalous
            for record in records:
                record['anomalies'] = []
                enhanced_data.append(record)
            continue

        # Fit detector on first 70% of data
        train_size = int(len(values) * 0.7)
        train_data = values[:train_size]

        detector = AnomalyDetector(method=method)
        detector.fit(train_data)

        # Detect anomalies in all data
        anomaly_results = detector.detect_anomalies(values)

        # Map back to records
        value_idx = 0
        for record in records:
            record_anomalies = []
            for point in record['points']:
                if value_idx < len(anomaly_results):
                    idx, val, is_anomaly = anomaly_results[value_idx]
                    if is_anomaly:
                        record_anomalies.append({
                            'timestamp': point['timestamp'],
                            'value': point['value'],
                            'anomaly_score': detector.get_anomaly_score(point['value'])
                        })
                value_idx += 1

            record['anomalies'] = record_anomalies
            enhanced_data.append(record)

    return enhanced_data

def load_timeseries_with_anomalies(filepath: str, method="isolation_forest") -> List[Dict]:
    """Load timeseries data and detect anomalies."""
    try:
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))

        return detect_anomalies_in_timeseries(data, method)
    except FileNotFoundError:
        log.warning(f"Timeseries file not found: {filepath}")
        return []

if __name__ == "__main__":
    # Example usage
    import random

    # Generate sample data with anomalies
    normal_data = [100 + random.gauss(0, 10) for _ in range(100)]
    anomalous_data = normal_data + [200, 250, 300]  # Add anomalies

    detector = AnomalyDetector(method="isolation_forest")
    detector.fit(normal_data)

    results = detector.detect_anomalies(anomalous_data)
    anomalies = [r for r in results if r[2]]

    print(f"Detected {len(anomalies)} anomalies out of {len(anomalous_data)} points")
    for idx, val, is_anomaly in anomalies:
        print(f"Anomaly at index {idx}: value = {val:.2f}")
