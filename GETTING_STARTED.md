# Getting Started - Wearable Biosignal Analysis System

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Backend Server

```bash
cd /home/administrator/Documents/Wearable/backend
python main.py
```

**Expected Output**:
```
🚀 Starting Wearable Biosignal Analysis Backend...
✓ BLE Simulator started
✓ Timesystems™ layer initialized
✓ iFRS™ layer initialized
✓ Clarity™ layer initialized
✓ LIA Engine initialized
================================================================================
Backend ready to accept connections on http://localhost:8000
================================================================================
```

### Step 2: Test with Demo Client

**Open a new terminal** and run:

```bash
cd /home/administrator/Documents/Wearable/backend
python demo_client.py
```

This will automatically demonstrate all features including:
- ✅ Device connection
- ✅ Real-time data streaming
- ✅ All three proprietary layers (Clarity™, iFRS™, Timesystems™)
- ✅ LIA health insights
- ✅ Processing logs

### Step 3: Explore the API

**Open in your browser**:
- **Interactive API Docs**: http://localhost:8000/docs
- **API Information**: http://localhost:8000

---

## 📱 Client Demonstration Checklist

Use this checklist when demonstrating to your client:

### ✅ 1. Show Backend is Running
```bash
curl http://localhost:8000/api/v1/health
```

**What this demonstrates**:
- All services are operational
- BLE simulator is running
- All three layers are initialized

---

### ✅ 2. Demonstrate Device Connection
```bash
curl -X POST http://localhost:8000/api/v1/connect \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "DEMO_BRACELET_001",
    "device_type": "bracelet",
    "app_version": "1.0.0"
  }'
```

**What this demonstrates**:
- Mobile app/wearable device can connect to backend
- Backend provides session ID
- Device status is tracked (battery, signal strength, firmware)

---

### ✅ 3. Show Real-Time Data Streaming
```bash
curl http://localhost:8000/api/v1/stream
```

**What this demonstrates**:
- Raw biosignals: Heart Rate, SpO2, Temperature, Activity
- **Clarity™ layer**: Signal quality, noise reduction, SNR, artifacts
- **iFRS™ layer**: Frequency analysis, HRV features, rhythm classification
- **Timesystems™ layer**: Temporal patterns, circadian rhythm alignment
- **LIA insights**: Health condition, wellness scores, recommendations

---

### ✅ 4. Demonstrate Layer Processing
```bash
curl http://localhost:8000/api/v1/demo/layers
```

**What this demonstrates**:
- Step-by-step breakdown of data flow
- Raw input → Clarity™ → iFRS™ → Timesystems™ → LIA
- Detailed processing information for each layer
- Algorithms used at each stage

---

### ✅ 5. Show Processing Logs
```bash
curl http://localhost:8000/api/v1/logs/processing?limit=20
```

**What this demonstrates**:
- Real-time logging of layer processing
- Example logs showing:
  - `CLARITY_LAYER | quality=0.92 | snr=38.5dB`
  - `IFRS_LAYER | dominant_freq=1.25Hz | hrv_score=75.2`
  - `TIMESYSTEMS_LAYER | pattern=stable | circadian_phase=afternoon`
  - `LIA_ENGINE | condition=Normal Resting | wellness_score=85.3`

---

### ✅ 6. Use Interactive API Documentation
**Open in browser**: http://localhost:8000/docs

**What this demonstrates**:
- Complete API documentation
- Interactive testing of all endpoints
- Request/response schemas
- Try out features directly in the browser

---

## 🧪 Alternative Testing Methods

### Method 1: Postman

1. Open Postman
2. Import file: `/home/administrator/Documents/Wearable/backend/POSTMAN_COLLECTION.json`
3. Run requests from the collection

**Pre-configured requests include**:
- Health Check
- Connect Mobile App/Bracelet/Clip
- Get Stream Data
- Get Prediction
- Create Sessions (Workout, Meditation, Sleep)
- Layer Processing Demo
- Processing Logs

### Method 2: Python Demo Client

```bash
cd /home/administrator/Documents/Wearable/backend
python demo_client.py
```

**Automatically runs**:
- Complete system demonstration
- All endpoints tested
- Formatted output showing all layers
- Optional 10-second continuous streaming

### Method 3: Browser (Swagger UI)

1. Start backend: `python main.py`
2. Open: http://localhost:8000/docs
3. Click on any endpoint
4. Click "Try it out"
5. Fill in parameters (if needed)
6. Click "Execute"
7. View response

---

## 📊 What Each Layer Does

### Clarity™ Layer
**Purpose**: Signal quality and noise reduction

**Output**:
- Quality Score: 0.0 - 1.0
- SNR: Typical 20-50 dB
- Quality Assessment: Excellent, Good, Fair, Poor
- Artifacts Detected: Motion, electrode noise, saturation
- Noise Reduction: Applied when quality < 0.7

**Example Output**:
```json
{
  "quality_score": 0.92,
  "signal_to_noise_ratio": 38.5,
  "quality_assessment": "excellent",
  "noise_reduction_applied": false,
  "artifacts_detected": []
}
```

---

### iFRS™ Layer
**Purpose**: Frequency domain analysis

**Output**:
- Dominant Frequency (Hz)
- HRV Features: RMSSD, SDNN, pNN50, HRV Score
- Frequency Bands: VLF, LF, HF power distribution
- Rhythm Classification: Normal Sinus, Athletic, Elevated, etc.
- Respiratory Rate estimation

**Example Output**:
```json
{
  "dominant_frequency": 1.25,
  "hrv_features": {
    "rmssd": 42.3,
    "sdnn": 68.1,
    "pnn50": 28.5,
    "hrv_score": 75.2
  },
  "rhythm_classification": "normal_sinus",
  "respiratory_rate": 16.2
}
```

---

### Timesystems™ Layer
**Purpose**: Temporal patterns and circadian rhythm

**Output**:
- Pattern Type: Stable, Increasing, Decreasing, etc.
- Circadian Phase: Morning, Afternoon, Evening, Night
- Temporal Consistency: 0.0 - 1.0
- Circadian Alignment Score
- Rhythm Score: 0 - 100

**Example Output**:
```json
{
  "pattern_type": "stable",
  "circadian_phase": "afternoon",
  "temporal_consistency": 0.88,
  "rhythm_score": 82.5,
  "circadian_alignment": {
    "expected_heart_rate": 75.0,
    "actual_heart_rate": 75.2,
    "alignment_score": 0.95
  }
}
```

---

### LIA Engine
**Purpose**: Comprehensive health insights

**Output**:
- Condition (10 types): Normal Resting, Exercise, Sleep, Stress, etc.
- Confidence: 0.70 - 0.99
- Wellness Score: 0 - 100
- Multi-dimensional wellness: Cardio, Respiratory, Activity, Stress
- Risk Factors
- Positive Indicators
- Personalized Recommendations

**Example Output**:
```json
{
  "condition": "Normal Resting",
  "confidence": 0.92,
  "wellness_score": 85.3,
  "wellness_assessment": {
    "cardiovascular_health": 88.5,
    "respiratory_health": 92.1,
    "activity_level": 78.3,
    "stress_level": 82.0,
    "overall_wellness": 85.3
  },
  "recommendation": "Maintain current activity levels and hydration",
  "positive_indicators": [
    "Excellent heart rate variability",
    "Optimal blood oxygen saturation"
  ]
}
```

---

## 📱 Mobile App Integration

### Update Mobile App Configuration

**File**: `BLE-wearable-App/src/services/api.ts` (or create if doesn't exist)

```typescript
export const API_CONFIG = {
  // Choose one based on your testing environment:
  BASE_URL: 'http://localhost:8000',        // iOS Simulator
  // BASE_URL: 'http://10.0.2.2:8000',      // Android Emulator
  // BASE_URL: 'http://192.168.1.X:8000',   // Physical Device (use your computer's IP)

  WS_URL: 'ws://localhost:8000/ws/stream',
  TIMEOUT: 10000,
};
```

### Example Integration Code

```typescript
import { API_CONFIG } from './config';

// Connect to backend
async function connectDevice() {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/connect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      device_id: 'MOBILE_APP_001',
      device_type: 'mobile_app',
      app_version: '1.0.0',
    }),
  });

  return await response.json();
}

// Get stream data
async function getStreamData() {
  const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/stream`);
  const data = await response.json();

  // Access data
  const heartRate = data.raw_signals.heart_rate;
  const wellness = data.lia_insights.wellness_score;
  const condition = data.lia_insights.condition;

  return data;
}

// WebSocket streaming
const ws = new WebSocket(API_CONFIG.WS_URL);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'stream_data') {
    // Update UI with real-time data
    console.log('Wellness:', message.data.lia_insights.wellness_score);
  }
};
```

---

## 🐛 Troubleshooting

### Backend won't start

**Check Python version**:
```bash
python3 --version
# Should be 3.10 or higher
```

**Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

### Port 8000 already in use

**Use different port**:
```bash
uvicorn main:app --port 8001
```

### Cannot connect from mobile app

**For Physical Device**:
1. Find your computer's IP address:
   ```bash
   # Linux/Mac
   ifconfig | grep "inet "
   # Look for IP like 192.168.1.x
   ```

2. Update mobile app config:
   ```typescript
   BASE_URL: 'http://192.168.1.X:8000'  // Use your actual IP
   ```

3. Ensure firewall allows port 8000

### Demo client fails

**Ensure backend is running first**:
```bash
# Terminal 1: Start backend
cd backend && python main.py

# Terminal 2: Run demo (after backend starts)
cd backend && python demo_client.py
```

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| `PROJECT_SUMMARY.md` | Complete project overview and client requirements |
| `backend/README.md` | Backend quick start guide |
| `backend/TECHNICAL_DOCUMENTATION.md` | Complete technical documentation (500+ lines) |
| `backend/POSTMAN_COLLECTION.json` | Postman API test collection |
| `GETTING_STARTED.md` | This file - quick start instructions |

---

## 🎯 For Client Demonstration

### Recommended Demonstration Flow:

1. **Start Backend** (Terminal 1)
   ```bash
   cd backend && python main.py
   ```

2. **Run Demo Client** (Terminal 2)
   ```bash
   cd backend && python demo_client.py
   ```

   This automatically demonstrates ALL features.

3. **Show Interactive Docs** (Browser)
   - Open http://localhost:8000/docs
   - Try the `/api/v1/stream` endpoint
   - Show complete response with all layers

4. **Explain Layer Processing**
   - Show `/api/v1/demo/layers` response
   - Explain data flow through each layer
   - Show processing logs

5. **Mobile Integration**
   - Show connection code
   - Explain API endpoints available
   - Demonstrate WebSocket streaming capability

---

## ✅ Success Indicators

You'll know everything is working when:

- ✅ Backend starts without errors
- ✅ Health endpoint returns "healthy" status
- ✅ Stream endpoint returns data with all layers
- ✅ Demo client completes all tests successfully
- ✅ Swagger UI shows all endpoints
- ✅ Processing logs show layer activity

---

## 🆘 Need Help?

1. Check the logs in terminal where backend is running
2. Review `TECHNICAL_DOCUMENTATION.md` for detailed information
3. Test individual endpoints using Swagger UI at http://localhost:8000/docs
4. Run health check: `curl http://localhost:8000/api/v1/health`

---

## 🎉 You're Ready!

The system is fully implemented and ready to demonstrate. All client requirements are met:

1. ✅ LIA integration
2. ✅ BLE connectivity (simulated)
3. ✅ Three proprietary layers (Clarity™, iFRS™, Timesystems™)
4. ✅ Complete technical documentation

Simply run `python backend/main.py` and you're good to go!
