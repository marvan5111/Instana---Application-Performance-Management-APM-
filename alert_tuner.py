import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging
from typing import List, Dict, Optional
import json

log = logging.getLogger("alert_tuner")

class AlertTuner:
    def __init__(self, contamination=0.1):
        """
        Initialize alert tuner for ML-based threshold adjustment and suppression.

        Args:
            contamination: Expected proportion of outliers for anomaly detection
        """
        self.contamination = contamination
        self.baseline_stats = {}
        self.anomaly_detector = None
        self.scaler = StandardScaler()

    def fit_baseline(self, historical_data: List[float]) -> None:
        """
        Fit the tuner on historical data to establish baseline behavior.

        Args:
            historical_data: List of historical metric values
        """
        if len(historical_data) < 10:
            log.warning("Insufficient historical data for alert tuning")
            return

        # Calculate baseline statistics
        self.baseline_stats = {
            'mean': np.mean(historical_data),
            'std': np.std(historical_data),
            'q1': np.percentile(historical_data, 25),
            'q3': np.percentile(historical_data, 75),
            'median': np.median(historical_data),
            'min': np.min(historical_data),
            'max': np.max(historical_data)
        }

        # Fit anomaly detector for suppression logic
        data_array = np.array(historical_data).reshape(-1, 1)
        scaled_data = self.scaler.fit_transform(data_array)

        self.anomaly_detector = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_estimators=50
        )
        self.anomaly_detector.fit(scaled_data)

        log.info(f"Alert tuner fitted on {len(historical_data)} data points")

    def tune_threshold(self, recent_data: List[float], current_threshold: float,
                      method="adaptive") -> float:
        """
        Tune alert threshold based on recent data patterns.

        Args:
            recent_data: Recent metric values
            current_threshold: Current alert threshold
            method: Tuning method ('adaptive', 'percentile', 'iqr')

        Returns:
            Tuned threshold value
        """
        if not self.baseline_stats:
            log.warning("Baseline not fitted, returning current threshold")
            return current_threshold

        if len(recent_data) < 5:
            return current_threshold

        if method == "adaptive":
            # Adaptive threshold based on recent trend
            recent_mean = np.mean(recent_data)
            baseline_mean = self.baseline_stats['mean']
            baseline_std = self.baseline_stats['std']

            # Adjust threshold based on how much the mean has shifted
            shift_factor = abs(recent_mean - baseline_mean) / baseline_std if baseline_std > 0 else 0
            adjustment = min(shift_factor * 0.1, 0.5)  # Cap adjustment at 50%

            if recent_mean > baseline_mean:
                # Data is trending higher, increase threshold
                new_threshold = current_threshold * (1 + adjustment)
            else:
                # Data is trending lower, decrease threshold slightly
                new_threshold = current_threshold * (1 - adjustment * 0.5)

            return max(new_threshold, baseline_mean + baseline_std)  # Don't go below 1 std dev

        elif method == "percentile":
            # Set threshold at 95th percentile of recent data
            return np.percentile(recent_data, 95)

        elif method == "iqr":
            # Use IQR method
            q3 = np.percentile(recent_data, 75)
            iqr = np.subtract(*np.percentile(recent_data, [75, 25]))
            return q3 + 1.5 * iqr

        return current_threshold

    def should_suppress_alert(self, alert_value: float, context_data: List[float],
                             threshold: float = None) -> bool:
        """
        Determine if an alert should be suppressed based on context.

        Args:
            alert_value: The value that triggered the alert
            context_data: Recent data points for context
            threshold: Alert threshold (optional)

        Returns:
            True if alert should be suppressed, False otherwise
        """
        if not self.baseline_stats or self.anomaly_detector is None:
            return False

        # Check if the alert value is within expected range
        baseline_mean = self.baseline_stats['mean']
        baseline_std = self.baseline_stats['std']

        # If alert value is within 2 standard deviations, likely not anomalous
        if abs(alert_value - baseline_mean) <= 2 * baseline_std:
            return True

        # Use anomaly detector to check if this is a false positive
        if len(context_data) >= 5:
            data_array = np.array(context_data + [alert_value]).reshape(-1, 1)
            scaled_data = self.scaler.transform(data_array)

            # Check if the alert value is predicted as anomaly by the model
            predictions = self.anomaly_detector.predict(scaled_data)
            if predictions[-1] == 1:  # Not an anomaly according to the model
                return True

        # Check for alert fatigue - if we've had many alerts recently
        if threshold and len(context_data) > 0:
            recent_alerts = sum(1 for val in context_data if val > threshold)
            if recent_alerts > len(context_data) * 0.3:  # More than 30% of recent values triggered alerts
                return True

        return False

    def get_alert_confidence(self, alert_value: float, context_data: List[float]) -> float:
        """
        Get confidence score for an alert (0-1, higher is more confident).

        Args:
            alert_value: The value that triggered the alert
            context_data: Recent data points for context

        Returns:
            Confidence score between 0 and 1
        """
        if not self.baseline_stats:
            return 0.5

        baseline_mean = self.baseline_stats['mean']
        baseline_std = self.baseline_stats['std']

        if baseline_std == 0:
            return 1.0 if alert_value != baseline_mean else 0.0

        # Confidence based on how many standard deviations away
        z_score = abs(alert_value - baseline_mean) / baseline_std

        # Convert z-score to confidence (higher z-score = higher confidence)
        confidence = min(z_score / 3.0, 1.0)  # Cap at 3 std devs = 100% confidence

        return confidence

def tune_alerts_for_entity(entity_id: str, metric_name: str, timeseries_data: List[Dict],
                          current_threshold: float) -> Dict:
    """
    Tune alerts for a specific entity and metric.

    Args:
        entity_id: Entity identifier
        metric_name: Metric name
        timeseries_data: Timeseries data records
        current_threshold: Current alert threshold

    Returns:
        Dictionary with tuned parameters
    """
    # Extract values from timeseries
    values = []
    for record in timeseries_data:
        if record.get('entity_id') == entity_id and record.get('metric_name') == metric_name:
            for point in record.get('points', []):
                values.append(point['value'])

    if len(values) < 20:
        return {
            'entity_id': entity_id,
            'metric_name': metric_name,
            'tuned_threshold': current_threshold,
            'suppression_enabled': False,
            'confidence': 0.5
        }

    # Fit tuner on historical data
    tuner = AlertTuner()
    train_size = int(len(values) * 0.7)
    tuner.fit_baseline(values[:train_size])

    # Tune threshold on recent data
    recent_data = values[train_size:]
    tuned_threshold = tuner.tune_threshold(recent_data, current_threshold)

    # Test suppression on a sample alert
    sample_alert_value = max(recent_data) if recent_data else current_threshold + 10
    should_suppress = tuner.should_suppress_alert(sample_alert_value, recent_data[-10:], current_threshold)

    confidence = tuner.get_alert_confidence(sample_alert_value, recent_data[-10:])

    return {
        'entity_id': entity_id,
        'metric_name': metric_name,
        'original_threshold': current_threshold,
        'tuned_threshold': tuned_threshold,
        'threshold_change_percent': ((tuned_threshold - current_threshold) / current_threshold) * 100 if current_threshold > 0 else 0,
        'suppression_recommended': should_suppress,
        'average_confidence': confidence
    }

if __name__ == "__main__":
    # Example usage
    tuner = AlertTuner()
    historical_data = [100, 102, 98, 105, 99, 101, 103, 97, 104, 100] * 10  # Normal data
    tuner.fit_baseline(historical_data)

    # Test threshold tuning
    recent_data = [110, 115, 108, 112, 109]  # Trending higher
    tuned = tuner.tune_threshold(recent_data, 120)
    print(f"Tuned threshold: {tuned}")

    # Test suppression
    suppress = tuner.should_suppress_alert(125, recent_data, 120)
    print(f"Should suppress alert: {suppress}")

    confidence = tuner.get_alert_confidence(125, recent_data)
    print(f"Alert confidence: {confidence:.2f}")
