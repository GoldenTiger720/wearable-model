"""
Configuration settings for the Wearable Biosignal Analysis System
"""

# Application Settings
APP_TITLE = "Wearable Biosignal Analysis System"
APP_WIDTH = 1400
APP_HEIGHT = 900

# Signal Settings
SAMPLING_RATE = 100  # Hz
UPDATE_INTERVAL = 50  # ms
SIGNAL_BUFFER_SIZE = 500  # Number of data points to display

# Biosignal Types
SIGNAL_TYPES = {
    'heart_rate': {'name': 'Heart Rate', 'unit': 'BPM', 'color': '#FF6B6B', 'range': (60, 100)},
    'spo2': {'name': 'SpO2', 'unit': '%', 'color': '#4ECDC4', 'range': (95, 100)},
    'temperature': {'name': 'Temperature', 'unit': '°C', 'color': '#45B7D1', 'range': (36.0, 37.5)},
    'activity': {'name': 'Activity Level', 'unit': 'steps/min', 'color': '#96CEB4', 'range': (0, 150)}
}

# Model Settings
MODEL_TYPES = ['CNN', 'LSTM', 'Transformer', 'Random Forest']
MODEL_STATUS = ['Idle', 'Training', 'Inference', 'Ready']

# API Settings
API_HOST = 'localhost'
API_PORT = 8080
API_ENDPOINTS = [
    '/api/v1/connect',
    '/api/v1/stream',
    '/api/v1/predict',
    '/api/v1/status'
]

# Colors
COLOR_PRIMARY = '#2C3E50'
COLOR_SECONDARY = '#34495E'
COLOR_SUCCESS = '#27AE60'
COLOR_WARNING = '#F39C12'
COLOR_DANGER = '#E74C3C'
COLOR_BG = '#ECF0F1'
COLOR_TEXT = '#2C3E50'
