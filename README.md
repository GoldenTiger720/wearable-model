# Wearable Biosignal Analysis System

A comprehensive demonstration system for analyzing biosignals from wearable devices. This system simulates real-time biosignal monitoring, machine learning model operations, and mobile app connectivity - perfect for customer presentations and demonstrations.

## Features

### 1. Real-Time Biosignal Visualization
- **Heart Rate (BPM)**: Continuous heart rate monitoring
- **SpO2 (%)**: Blood oxygen saturation levels
- **Temperature (°C)**: Body temperature tracking
- **Activity Level (steps/min)**: Physical activity monitoring

All signals are displayed with smooth, real-time graphs that update continuously.

### 2. Model Management
- **Load/Create Models**: Select existing models or create new ones
- **Training Simulation**: Simulate model training with:
  - Configurable epochs
  - Real-time training metrics (loss, accuracy, validation)
  - Progress tracking
- **Inference Mode**: Run live predictions on incoming biosignal data
- **Model Information Display**: View model parameters and statistics

### 3. API Connectivity Simulation
- **Local API Server**: Simulated REST API on `http://localhost:8080`
- **Available Endpoints**:
  - `GET /api/v1/status` - Server status
  - `GET /api/v1/stream` - Real-time signal data
  - `POST /api/v1/connect` - Connect mobile client
  - `POST /api/v1/predict` - Get predictions
- **Activity Logging**: Track all API requests and responses
- **Mobile App Integration Demo**: Show how mobile apps connect to the system

### 4. Results & Analytics
- **Prediction Results**: Real-time condition detection with confidence scores
- **System Logs**: Comprehensive logging with different severity levels
- **Statistics Dashboard**:
  - Total predictions
  - Average confidence
  - Session duration
  - Data points processed
- **Export Functionality**: Export results and logs to JSON/text files

## Project Structure

```
Wearable/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── mock_data.py           # Mock data generator for biosignals
├── signal_visualizer.py   # Real-time signal visualization
├── model_manager.py       # Model operations (load/train/inference)
├── api_simulator.py       # API server simulation
├── results_panel.py       # Results and logging display
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)
- numpy

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install numpy
```

Note: `tkinter` is included with most Python installations. If you need to install it:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Included with Python from python.org
- **Windows**: Included with Python installer

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### Quick Start Guide

1. **Create or Load a Model**
   - Go to the "Model" tab
   - Click "Create New Model" for a demo model, or
   - Click "Load Model" to select an existing model file

2. **Start the API Server (Optional)**
   - Go to the "API" tab
   - Click "Start Server"
   - Server will run on `http://localhost:8080`

3. **Start Biosignal Monitoring**
   - Click the "▶ Start Monitoring" button
   - Real-time biosignals will appear in the graphs
   - If a model is loaded, predictions will start automatically

4. **View Results**
   - Go to the "Results" tab
   - View predictions, logs, and statistics
   - Export data as needed

### Advanced Features

#### Model Training Simulation
1. Go to the "Model" tab
2. Set the number of epochs (1-100)
3. Click "Start Training"
4. Watch real-time training metrics update
5. Stop training at any time or let it complete

#### Injecting Anomalies
- Use **Tools > Inject Anomaly** to demonstrate anomaly detection
- The system will show irregular patterns in the signals

#### Generating Reports
- Use **Tools > Generate Test Report** for a quick system overview
- Use **File > Export Results** to save detailed data

### Testing Mobile App Connectivity

The API server can be tested using curl or any HTTP client:

```bash
# Check server status
curl http://localhost:8080/api/v1/status

# Connect as a mobile client
curl -X POST http://localhost:8080/api/v1/connect \
  -H "Content-Type: application/json" \
  -d '{"client_id": "mobile_app_001"}'

# Get real-time signal data
curl http://localhost:8080/api/v1/stream

# Get latest prediction
curl -X POST http://localhost:8080/api/v1/predict
```

## Customer Demonstration Script

### Opening (2 minutes)
1. Launch the application
2. Show the clean, professional interface
3. Explain the purpose: "This system analyzes biosignals from wearable devices in real-time"

### Model Management (3 minutes)
1. Create a new model: "Our system supports various ML architectures"
2. Start training simulation: "Watch as the model trains with real-time metrics"
3. Show training progress and metrics

### Real-Time Monitoring (5 minutes)
1. Start monitoring: "Let's see live biosignal data"
2. Point out the four different biosignal types
3. Start inference: "The model is now analyzing these signals in real-time"
4. Show prediction results appearing in the Results tab

### API Integration (3 minutes)
1. Start the API server
2. Show available endpoints
3. Demonstrate a curl request (have it prepared)
4. Explain: "This is how your mobile app would connect"

### Results & Analytics (2 minutes)
1. Show prediction history
2. Display statistics dashboard
3. Export results to show data persistence

### Closing
- Answer questions
- Offer to customize for specific needs

## Configuration

Edit `config.py` to customize:
- Signal types and ranges
- Update intervals
- API endpoints and ports
- Visual styling (colors, sizes)

Example customization:
```python
# Change update speed
UPDATE_INTERVAL = 100  # milliseconds

# Change API port
API_PORT = 9000

# Adjust signal ranges
SIGNAL_TYPES = {
    'heart_rate': {'range': (50, 120)},  # Custom range
}
```

## Troubleshooting

### Issue: Application won't start
- **Solution**: Ensure Python 3.7+ is installed and tkinter is available

### Issue: API server fails to start
- **Solution**: Check if port 8080 is already in use. Change `API_PORT` in config.py

### Issue: Graphs not updating smoothly
- **Solution**: Increase `UPDATE_INTERVAL` in config.py for slower updates

### Issue: "No model loaded" warning
- **Solution**: Click "Create New Model" before starting monitoring

## Technical Details

### Mock Data Generation
The system uses sinusoidal patterns with added noise to simulate realistic biosignals:
- Each signal has configurable frequency and amplitude
- Values are clamped to medically realistic ranges
- Random variations simulate real-world conditions

### Model Simulation
- Model operations are simulated using threading
- Training metrics follow realistic learning curves
- Predictions use probability distributions across condition classes

### Performance
- Optimized for smooth 60 FPS visualization
- Minimal CPU usage (~5-10% on modern systems)
- Memory efficient with circular buffers

## Future Enhancements (Not Yet Implemented)

This is a demonstration system. For production, consider adding:
- Real wearable device integration
- Actual machine learning models (TensorFlow/PyTorch)
- Database persistence
- User authentication
- Cloud deployment
- Advanced analytics and reporting

## License

This is a demonstration system for customer presentations.

## Support

For questions or customization requests, please contact your technical team.

---

**Note**: This system uses simulated data and mock models. All predictions and results are for demonstration purposes only and should not be used for actual medical decisions.
