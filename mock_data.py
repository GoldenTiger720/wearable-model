"""
Mock data generator for simulating wearable device biosignals
"""
import numpy as np
import random
from datetime import datetime
from config import SIGNAL_TYPES


class MockDataGenerator:
    """Generates realistic mock biosignal data"""

    def __init__(self):
        self.time_offset = 0
        self.base_values = {
            'heart_rate': 75,
            'spo2': 98,
            'temperature': 36.8,
            'activity': 30
        }
        # Add some variability patterns
        self.patterns = {
            'heart_rate': {'freq': 0.1, 'amplitude': 10},
            'spo2': {'freq': 0.05, 'amplitude': 2},
            'temperature': {'freq': 0.02, 'amplitude': 0.3},
            'activity': {'freq': 0.15, 'amplitude': 40}
        }

    def generate_sample(self, signal_type):
        """Generate a single sample for a given signal type"""
        if signal_type not in SIGNAL_TYPES:
            raise ValueError(f"Unknown signal type: {signal_type}")

        base = self.base_values[signal_type]
        pattern = self.patterns[signal_type]

        # Generate sinusoidal pattern with noise
        sine_wave = pattern['amplitude'] * np.sin(2 * np.pi * pattern['freq'] * self.time_offset)
        noise = np.random.normal(0, pattern['amplitude'] * 0.2)

        value = base + sine_wave + noise

        # Clamp to reasonable ranges
        signal_range = SIGNAL_TYPES[signal_type]['range']
        value = np.clip(value, signal_range[0] - 5, signal_range[1] + 5)

        self.time_offset += 0.01

        return round(value, 2)

    def generate_batch(self, signal_type, n_samples):
        """Generate multiple samples"""
        return [self.generate_sample(signal_type) for _ in range(n_samples)]

    def generate_all_signals(self):
        """Generate one sample for each signal type"""
        return {signal: self.generate_sample(signal) for signal in SIGNAL_TYPES.keys()}

    def add_anomaly(self, signal_type, anomaly_type='spike'):
        """Inject an anomaly into the signal"""
        if anomaly_type == 'spike':
            return self.base_values[signal_type] * random.uniform(1.3, 1.5)
        elif anomaly_type == 'drop':
            return self.base_values[signal_type] * random.uniform(0.6, 0.8)
        else:
            return self.generate_sample(signal_type)


class MockPredictionGenerator:
    """Generates mock prediction results"""

    def __init__(self):
        self.conditions = [
            'Normal Activity',
            'Light Exercise',
            'Intense Exercise',
            'Resting',
            'Sleeping',
            'Stress Detected',
            'Irregular Pattern'
        ]
        self.confidence_base = 0.85

    def generate_prediction(self, signal_data):
        """Generate a mock prediction based on signal data"""
        # Simulate model prediction
        condition = random.choice(self.conditions)
        confidence = round(self.confidence_base + random.uniform(-0.1, 0.15), 3)
        confidence = min(0.99, max(0.70, confidence))

        # Generate class probabilities
        probabilities = self._generate_probabilities()

        prediction = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'condition': condition,
            'confidence': confidence,
            'probabilities': probabilities,
            'signal_quality': random.choice(['Excellent', 'Good', 'Fair']),
            'recommendation': self._generate_recommendation(condition)
        }

        return prediction

    def _generate_probabilities(self):
        """Generate probability distribution for all classes"""
        probs = np.random.dirichlet(np.ones(len(self.conditions)) * 2)
        return {cond: round(float(prob), 3) for cond, prob in zip(self.conditions, probs)}

    def _generate_recommendation(self, condition):
        """Generate recommendation based on detected condition"""
        recommendations = {
            'Normal Activity': 'Continue monitoring',
            'Light Exercise': 'Maintain current activity level',
            'Intense Exercise': 'Consider rest if prolonged',
            'Resting': 'Normal state',
            'Sleeping': 'Good sleep pattern',
            'Stress Detected': 'Consider relaxation exercises',
            'Irregular Pattern': 'Recommend medical consultation'
        }
        return recommendations.get(condition, 'Continue monitoring')
