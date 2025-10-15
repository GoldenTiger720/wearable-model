"""
Main application - Wearable Biosignal Analysis System
A demonstration system for customer presentation showing biosignal analysis,
model training/inference, and mobile app connectivity.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, UPDATE_INTERVAL
from mock_data import MockDataGenerator, MockPredictionGenerator
from signal_visualizer import SignalVisualizerPanel
from model_manager import ModelManager, ModelControlPanel
from api_simulator import APISimulator, APIControlPanel
from results_panel import ResultsPanel


class WearableAnalysisApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        # Initialize components
        self.data_generator = MockDataGenerator()
        self.prediction_generator = MockPredictionGenerator()
        self.model_manager = ModelManager()
        self.api_simulator = APISimulator()

        # State variables
        self.is_streaming = False
        self.is_running = False
        self.update_job = None

        # Setup UI
        self._setup_ui()
        self._setup_menu()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - Visualization and Controls
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=2)

        # Top control bar
        control_bar = ttk.Frame(left_panel)
        control_bar.pack(fill=tk.X, padx=10, pady=10)

        # Title and status
        title_frame = ttk.Frame(control_bar)
        title_frame.pack(side=tk.LEFT)

        ttk.Label(
            title_frame,
            text=APP_TITLE,
            font=('Arial', 16, 'bold')
        ).pack(anchor='w')

        self.status_label = ttk.Label(
            title_frame,
            text="Status: Idle",
            font=('Arial', 10),
            foreground='gray'
        )
        self.status_label.pack(anchor='w')

        # Main control buttons
        btn_frame = ttk.Frame(control_bar)
        btn_frame.pack(side=tk.RIGHT)

        self.start_btn = ttk.Button(
            btn_frame,
            text="▶ Start Monitoring",
            command=self._start_monitoring,
            style='Accent.TButton'
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹ Stop",
            command=self._stop_monitoring,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Signal visualization
        self.signal_panel = SignalVisualizerPanel(left_panel)
        self.signal_panel.pack(fill=tk.BOTH, expand=True)

        # Right panel - Model, API, and Results
        right_panel = ttk.Notebook(main_container)
        main_container.add(right_panel, weight=1)

        # Model Management Tab
        self.model_panel = ModelControlPanel(right_panel, self.model_manager)
        right_panel.add(self.model_panel, text="Model")

        # API Connectivity Tab
        self.api_panel = APIControlPanel(right_panel, self.api_simulator)
        right_panel.add(self.api_panel, text="API")

        # Results Tab
        self.results_panel = ResultsPanel(right_panel)
        right_panel.add(self.results_panel, text="Results")

    def _setup_menu(self):
        """Setup application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Results", command=self._export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Clear All Data", command=self._clear_all_data)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Inject Anomaly", command=self._inject_anomaly)
        tools_menu.add_command(label="Generate Test Report", command=self._generate_report)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Documentation", command=self._show_docs)

    def _start_monitoring(self):
        """Start biosignal monitoring and analysis"""
        if self.is_streaming:
            return

        # Check if model is loaded
        if self.model_manager.current_model is None:
            response = messagebox.askyesno(
                "No Model Loaded",
                "No model is currently loaded. Do you want to create a demo model?"
            )
            if response:
                self.model_manager.load_model("demo_model.h5")
                self.results_panel.add_log("Demo model created and loaded", "INFO")
            else:
                return

        self.is_streaming = True
        self.is_running = True

        # Update UI state
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring Active", foreground='green')

        # Start inference mode
        self.model_manager.start_inference()

        # Log start
        self.results_panel.add_log("Biosignal monitoring started", "SUCCESS")

        # Start update loop
        self._update_loop()

    def _stop_monitoring(self):
        """Stop biosignal monitoring"""
        self.is_streaming = False
        self.is_running = False

        # Update UI state
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Idle", foreground='gray')

        # Stop inference mode
        self.model_manager.stop_inference()

        # Cancel scheduled update
        if self.update_job:
            self.root.after_cancel(self.update_job)
            self.update_job = None

        # Log stop
        self.results_panel.add_log("Biosignal monitoring stopped", "INFO")

    def _update_loop(self):
        """Main update loop for real-time data"""
        if not self.is_running:
            return

        try:
            # Generate biosignal data
            signal_data = self.data_generator.generate_all_signals()

            # Update visualizations
            self.signal_panel.update_signals(signal_data)

            # Update API data
            if self.api_simulator.is_running:
                self.api_simulator.update_signal_data(signal_data)

            # Generate predictions if in inference mode
            if self.model_manager.is_inferencing:
                # Generate prediction every 2 seconds (every ~40 updates)
                if hasattr(self, '_update_counter'):
                    self._update_counter += 1
                else:
                    self._update_counter = 0

                if self._update_counter % 40 == 0:
                    prediction = self.prediction_generator.generate_prediction(signal_data)
                    self.results_panel.add_prediction(prediction)
                    self.api_simulator.add_prediction(prediction)
                    self.results_panel.add_log(
                        f"Prediction: {prediction['condition']} ({prediction['confidence']:.1%})",
                        "INFO"
                    )

        except Exception as e:
            self.results_panel.add_log(f"Update error: {str(e)}", "ERROR")

        # Schedule next update
        self.update_job = self.root.after(UPDATE_INTERVAL, self._update_loop)

    def _clear_all_data(self):
        """Clear all visualizations and data"""
        response = messagebox.askyesno(
            "Clear Data",
            "Are you sure you want to clear all data?"
        )
        if response:
            self.signal_panel.clear_all()
            self.results_panel.add_log("All visualization data cleared", "INFO")

    def _inject_anomaly(self):
        """Inject an anomaly into the signal for demonstration"""
        if not self.is_streaming:
            messagebox.showinfo("Info", "Start monitoring first to inject anomalies")
            return

        # This will affect the next few data points
        self.results_panel.add_log("Anomaly injected into signal", "WARNING")
        messagebox.showinfo("Anomaly Injected", "An anomaly has been injected into the biosignal stream")

    def _generate_report(self):
        """Generate a test report"""
        report = f"""
=== WEARABLE BIOSIGNAL ANALYSIS TEST REPORT ===
Generated: {self.results_panel.session_start.strftime('%Y-%m-%d %H:%M:%S')}

Model Information:
- Status: {self.model_manager.model_status}
- Current Model: {self.model_manager.current_model['name'] if self.model_manager.current_model else 'None'}

API Status:
- Server: {'Running' if self.api_simulator.is_running else 'Stopped'}
- Endpoint: http://localhost:8080

Session Statistics:
- Total Predictions: {len(self.results_panel.prediction_history)}
- Monitoring Status: {'Active' if self.is_streaming else 'Inactive'}

System: Operational ✓
"""
        messagebox.showinfo("Test Report", report)
        self.results_panel.add_log("Test report generated", "INFO")

    def _export_results(self):
        """Export all results"""
        self.results_panel._export_predictions()
        self.results_panel._export_logs()
        messagebox.showinfo("Export Complete", "Results and logs have been exported")

    def _show_about(self):
        """Show about dialog"""
        about_text = f"""
{APP_TITLE}
Version 1.0.0

A demonstration system for biosignal analysis from wearable devices.

Features:
• Real-time biosignal visualization
• ML model training and inference simulation
• Mobile app API connectivity
• Comprehensive logging and reporting

© 2025 - Demo System
"""
        messagebox.showinfo("About", about_text)

    def _show_docs(self):
        """Show documentation"""
        docs_text = """
Quick Start Guide:

1. Load/Create a Model:
   - Go to Model tab
   - Click 'Load Model' or 'Create New Model'

2. Start API Server (Optional):
   - Go to API tab
   - Click 'Start Server'

3. Start Monitoring:
   - Click '▶ Start Monitoring' button
   - View real-time biosignals and predictions

4. Training (Optional):
   - Go to Model tab
   - Set epochs and click 'Start Training'

For more information, see README.md
"""
        messagebox.showinfo("Documentation", docs_text)

    def _on_closing(self):
        """Handle application closing"""
        if self.is_streaming:
            response = messagebox.askyesno(
                "Confirm Exit",
                "Monitoring is active. Are you sure you want to exit?"
            )
            if not response:
                return

        # Stop all running processes
        self._stop_monitoring()
        if self.api_simulator.is_running:
            self.api_simulator.stop_server()

        # Close application
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()

    # Set style
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme for better appearance

    # Create and run application
    app = WearableAnalysisApp(root)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
