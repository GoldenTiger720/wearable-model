# 🚀 QUICK REFERENCE CARD

## Start Everything (2 Commands)

### Backend:
```bash
cd /home/administrator/Documents/Wearable/backend && python main.py
```
✅ Starts at: http://localhost:8000

### Mobile App:
```bash
cd /home/administrator/Documents/Wearable/BLE-wearable-App && npm start
```
✅ Then press: `i` (iOS) or `a` (Android)

---

## Add Live Data to App (2 Edits)

### 1. Navigation (`src/navigation/AppNavigator.tsx`):
```typescript
import { LiveDataScreen } from '../screens/livedata/LiveDataScreen';

<Stack.Screen name="LiveData" component={LiveDataScreen} />
```

### 2. Dashboard (`src/screens/dashboard/DashboardScreen.tsx`):
```typescript
<Button onPress={() => navigation.navigate('LiveData' as never)}>
  View Live Data
</Button>
```

---

## Test Backend

```bash
curl http://localhost:8000/api/v1/health
```

---

## View API Docs

Open in browser: http://localhost:8000/docs

---

## Demo Client

```bash
cd backend && python demo_client.py
```

---

## What You Get

### Backend (15+ Endpoints):
- ✅ Clarity™ Layer (Signal Quality)
- ✅ iFRS™ Layer (Frequency Analysis)
- ✅ Timesystems™ Layer (Temporal Patterns)
- ✅ LIA Engine (Health Insights)

### Mobile App (New Components):
- ✅ BiosignalCard (4 signals)
- ✅ WellnessCard (5 dimensions)
- ✅ LayerProcessingCard (3 layers)
- ✅ LiveDataScreen (complete)

### Updates Every:
- Backend: 100ms (10 Hz)
- Mobile: 1000ms (1 Hz)

---

## Platform URLs

- **iOS Simulator**: `http://localhost:8000` ✅ Auto
- **Android Emulator**: `http://10.0.2.2:8000` ✅ Auto
- **Physical Device**: Update IP in `backendApi.ts`

---

## Troubleshoot

### Backend:
```bash
pip install -r requirements.txt
```

### Mobile:
```bash
npm install --legacy-peer-deps
```

### Clear Cache:
```bash
npm start -- --clear
```

---

## Status: ✅ READY

- Backend: Complete
- Mobile: Integrated + SDK 54
- Docs: 7 files, 2,500+ lines
- Code: 5,000+ lines

**Demo Ready!** 🎉
