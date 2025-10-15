"""
API endpoint simulation module for mobile app connectivity
"""
import tkinter as tk
from tkinter import ttk
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
from config import API_HOST, API_PORT, API_ENDPOINTS


class MockAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock API endpoints"""

    # Class variables to store shared data
    signal_data = {}
    predictions = []
    connected_clients = []

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/v1/status':
            self._send_json_response({
                'status': 'online',
                'timestamp': datetime.now().isoformat(),
                'connected_clients': len(self.connected_clients),
                'version': '1.0.0'
            })
        elif self.path == '/api/v1/stream':
            self._send_json_response({
                'signal_data': self.signal_data,
                'timestamp': datetime.now().isoformat()
            })
        else:
            self._send_json_response({'error': 'Endpoint not found'}, 404)

    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json_response({'error': 'Invalid JSON'}, 400)
            return

        if self.path == '/api/v1/connect':
            client_id = data.get('client_id', 'unknown')
            self.connected_clients.append({
                'client_id': client_id,
                'connected_at': datetime.now().isoformat()
            })
            self._send_json_response({
                'status': 'connected',
                'client_id': client_id,
                'session_token': f"token_{len(self.connected_clients)}"
            })
        elif self.path == '/api/v1/predict':
            # Return latest prediction
            if self.predictions:
                self._send_json_response({
                    'prediction': self.predictions[-1],
                    'timestamp': datetime.now().isoformat()
                })
            else:
                self._send_json_response({
                    'message': 'No predictions available',
                    'timestamp': datetime.now().isoformat()
                })
        else:
            self._send_json_response({'error': 'Endpoint not found'}, 404)

    def _send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass  # Suppress default logging


class APISimulator:
    """Manages the mock API server"""

    def __init__(self):
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.request_log = []

    def start_server(self):
        """Start the mock API server"""
        if self.is_running:
            return False

        try:
            self.server = HTTPServer((API_HOST, API_PORT), MockAPIHandler)
            self.is_running = True

            def run_server():
                while self.is_running:
                    self.server.handle_request()

            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()

            self._log_request('Server started', f'http://{API_HOST}:{API_PORT}')
            return True
        except Exception as e:
            self._log_request('Server error', str(e))
            return False

    def stop_server(self):
        """Stop the mock API server"""
        if self.is_running:
            self.is_running = False
            if self.server:
                self.server.server_close()
            self._log_request('Server stopped', '')
            return True
        return False

    def update_signal_data(self, signal_data):
        """Update signal data for API responses"""
        MockAPIHandler.signal_data = signal_data

    def add_prediction(self, prediction):
        """Add prediction to API responses"""
        MockAPIHandler.predictions.append(prediction)
        if len(MockAPIHandler.predictions) > 100:
            MockAPIHandler.predictions = MockAPIHandler.predictions[-100:]

    def _log_request(self, event, details):
        """Log API events"""
        log_entry = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'event': event,
            'details': details
        }
        self.request_log.append(log_entry)
        if len(self.request_log) > 100:
            self.request_log = self.request_log[-100:]

    def get_log(self):
        """Get request log"""
        return self.request_log


class APIControlPanel(ttk.Frame):
    """UI panel for API control and monitoring"""

    def __init__(self, parent, api_simulator):
        super().__init__(parent)
        self.api_simulator = api_simulator
        self._setup_ui()

    def _setup_ui(self):
        """Setup the API control panel UI"""
        # Title
        title = ttk.Label(
            self,
            text="Mobile App API Connectivity",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10)

        # Server Control
        control_frame = ttk.LabelFrame(self, text="Server Control", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Server info
        info_frame = ttk.Frame(control_frame)
        info_frame.pack(fill=tk.X, pady=5)

        ttk.Label(info_frame, text="API Server:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.server_url = ttk.Label(
            info_frame,
            text=f"http://{API_HOST}:{API_PORT}",
            font=('Courier', 10),
            foreground='blue'
        )
        self.server_url.pack(side=tk.LEFT, padx=5)

        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.start_btn = ttk.Button(
            btn_frame,
            text="Start Server",
            command=self._start_server
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(
            btn_frame,
            text="Stop Server",
            command=self._stop_server,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Status indicator
        self.status_indicator = tk.Canvas(btn_frame, width=20, height=20)
        self.status_indicator.pack(side=tk.LEFT, padx=10)
        self.status_circle = self.status_indicator.create_oval(2, 2, 18, 18, fill='gray')

        self.status_text = ttk.Label(btn_frame, text="Offline", foreground='gray')
        self.status_text.pack(side=tk.LEFT)

        # Endpoints Section
        endpoints_frame = ttk.LabelFrame(self, text="Available Endpoints", padding=10)
        endpoints_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Endpoints list
        endpoints_text = tk.Text(endpoints_frame, height=8, width=50, font=('Courier', 9))
        endpoints_text.pack(fill=tk.BOTH, expand=True)

        endpoints_info = """Available API Endpoints:

GET  /api/v1/status     - Server status
GET  /api/v1/stream     - Real-time signal data
POST /api/v1/connect    - Connect mobile client
POST /api/v1/predict    - Get predictions

Example mobile app connection:
POST http://localhost:8080/api/v1/connect
Body: {"client_id": "mobile_app_001"}"""

        endpoints_text.insert('1.0', endpoints_info)
        endpoints_text.config(state=tk.DISABLED)

        # Activity Log
        log_frame = ttk.LabelFrame(self, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar for log
        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(
            log_frame,
            height=10,
            width=50,
            font=('Courier', 8),
            yscrollcommand=log_scroll.set
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)

        # Start log update
        self._update_log()

    def _start_server(self):
        """Start API server"""
        if self.api_simulator.start_server():
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_indicator.itemconfig(self.status_circle, fill='green')
            self.status_text.config(text="Online", foreground='green')
            self._add_log("✓ Server started successfully")
        else:
            self._add_log("✗ Failed to start server")

    def _stop_server(self):
        """Stop API server"""
        if self.api_simulator.stop_server():
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_indicator.itemconfig(self.status_circle, fill='gray')
            self.status_text.config(text="Offline", foreground='gray')
            self._add_log("✓ Server stopped")

    def _add_log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def _update_log(self):
        """Update activity log from API simulator"""
        logs = self.api_simulator.get_log()

        # Check for new log entries
        current_lines = self.log_text.get('1.0', tk.END).count('\n')
        if len(logs) > current_lines - 1:
            for log in logs[current_lines - 1:]:
                self._add_log(f"{log['event']}: {log['details']}")

        # Schedule next update
        self.after(500, self._update_log)
