"""
Results and logging display module
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import json


class ResultsPanel(ttk.Frame):
    """Panel for displaying prediction results and logs"""

    def __init__(self, parent):
        super().__init__(parent)
        self.prediction_history = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the results panel UI"""
        # Title
        title = ttk.Label(
            self,
            text="Prediction Results & System Logs",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Predictions Tab
        predictions_frame = ttk.Frame(notebook)
        notebook.add(predictions_frame, text="Predictions")
        self._setup_predictions_tab(predictions_frame)

        # Logs Tab
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="System Logs")
        self._setup_logs_tab(logs_frame)

        # Statistics Tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        self._setup_stats_tab(stats_frame)

    def _setup_predictions_tab(self, parent):
        """Setup predictions display tab"""
        # Current prediction display
        current_frame = ttk.LabelFrame(parent, text="Latest Prediction", padding=10)
        current_frame.pack(fill=tk.X, padx=10, pady=5)

        self.current_prediction_text = tk.Text(
            current_frame,
            height=8,
            width=60,
            font=('Courier', 10),
            bg='#f0f0f0'
        )
        self.current_prediction_text.pack(fill=tk.X)
        self.current_prediction_text.insert('1.0', 'No predictions yet')
        self.current_prediction_text.config(state=tk.DISABLED)

        # Prediction history
        history_frame = ttk.LabelFrame(parent, text="Prediction History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar
        scroll = ttk.Scrollbar(history_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_text = tk.Text(
            history_frame,
            height=15,
            width=60,
            font=('Courier', 9),
            yscrollcommand=scroll.set
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.history_text.yview)

        # Control buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            btn_frame,
            text="Clear History",
            command=self._clear_predictions
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Export Results",
            command=self._export_predictions
        ).pack(side=tk.LEFT, padx=5)

    def _setup_logs_tab(self, parent):
        """Setup system logs tab"""
        # Log display
        log_frame = ttk.Frame(parent)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar
        scroll = ttk.Scrollbar(log_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(
            log_frame,
            height=25,
            width=70,
            font=('Courier', 9),
            yscrollcommand=scroll.set
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.log_text.yview)

        # Configure tags for different log levels
        self.log_text.tag_config('INFO', foreground='blue')
        self.log_text.tag_config('WARNING', foreground='orange')
        self.log_text.tag_config('ERROR', foreground='red')
        self.log_text.tag_config('SUCCESS', foreground='green')

        # Control buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            btn_frame,
            text="Clear Logs",
            command=self._clear_logs
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Export Logs",
            command=self._export_logs
        ).pack(side=tk.LEFT, padx=5)

        # Add initial log
        self.add_log("System initialized", "INFO")

    def _setup_stats_tab(self, parent):
        """Setup statistics tab"""
        # Statistics display
        stats_container = ttk.Frame(parent)
        stats_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create statistics labels
        self.stats_labels = {}

        stats_items = [
            ('Total Predictions', 'total_predictions'),
            ('Average Confidence', 'avg_confidence'),
            ('Most Common Condition', 'common_condition'),
            ('Session Duration', 'session_duration'),
            ('Data Points Processed', 'data_points'),
            ('API Requests', 'api_requests')
        ]

        for i, (label, key) in enumerate(stats_items):
            frame = ttk.Frame(stats_container)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(
                frame,
                text=f"{label}:",
                font=('Arial', 10, 'bold'),
                width=25,
                anchor='w'
            ).pack(side=tk.LEFT)

            value_label = ttk.Label(
                frame,
                text="0",
                font=('Arial', 10),
                foreground='blue'
            )
            value_label.pack(side=tk.LEFT, padx=10)
            self.stats_labels[key] = value_label

        # Refresh button
        ttk.Button(
            stats_container,
            text="Refresh Statistics",
            command=self._refresh_stats
        ).pack(pady=20)

        self.session_start = datetime.now()

    def add_prediction(self, prediction):
        """Add a new prediction result"""
        self.prediction_history.append(prediction)

        # Update current prediction display
        pred_text = f"""Timestamp: {prediction['timestamp']}
Condition: {prediction['condition']}
Confidence: {prediction['confidence']:.1%}
Signal Quality: {prediction['signal_quality']}
Recommendation: {prediction['recommendation']}

Top 3 Probabilities:"""

        # Sort probabilities and get top 3
        sorted_probs = sorted(
            prediction['probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        for condition, prob in sorted_probs:
            pred_text += f"\n  {condition}: {prob:.1%}"

        self.current_prediction_text.config(state=tk.NORMAL)
        self.current_prediction_text.delete('1.0', tk.END)
        self.current_prediction_text.insert('1.0', pred_text)
        self.current_prediction_text.config(state=tk.DISABLED)

        # Add to history
        history_entry = f"[{prediction['timestamp']}] {prediction['condition']} (conf: {prediction['confidence']:.1%})\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)

        # Update statistics
        self._refresh_stats()

    def add_log(self, message, level="INFO"):
        """Add a log message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        self.log_text.insert(tk.END, log_entry, level)
        self.log_text.see(tk.END)

    def _clear_predictions(self):
        """Clear prediction history"""
        self.prediction_history.clear()
        self.history_text.delete('1.0', tk.END)
        self.current_prediction_text.config(state=tk.NORMAL)
        self.current_prediction_text.delete('1.0', tk.END)
        self.current_prediction_text.insert('1.0', 'No predictions yet')
        self.current_prediction_text.config(state=tk.DISABLED)
        self.add_log("Prediction history cleared", "INFO")

    def _clear_logs(self):
        """Clear system logs"""
        self.log_text.delete('1.0', tk.END)
        self.add_log("Logs cleared", "INFO")

    def _export_predictions(self):
        """Export predictions to file"""
        if not self.prediction_history:
            self.add_log("No predictions to export", "WARNING")
            return

        filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(self.prediction_history, f, indent=2)
            self.add_log(f"Predictions exported to {filename}", "SUCCESS")
        except Exception as e:
            self.add_log(f"Export failed: {str(e)}", "ERROR")

    def _export_logs(self):
        """Export logs to file"""
        filename = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(self.log_text.get('1.0', tk.END))
            self.add_log(f"Logs exported to {filename}", "SUCCESS")
        except Exception as e:
            self.add_log(f"Export failed: {str(e)}", "ERROR")

    def _refresh_stats(self):
        """Refresh statistics display"""
        # Total predictions
        self.stats_labels['total_predictions'].config(
            text=str(len(self.prediction_history))
        )

        # Average confidence
        if self.prediction_history:
            avg_conf = sum(p['confidence'] for p in self.prediction_history) / len(self.prediction_history)
            self.stats_labels['avg_confidence'].config(text=f"{avg_conf:.1%}")

            # Most common condition
            conditions = [p['condition'] for p in self.prediction_history]
            most_common = max(set(conditions), key=conditions.count)
            self.stats_labels['common_condition'].config(text=most_common)
        else:
            self.stats_labels['avg_confidence'].config(text="N/A")
            self.stats_labels['common_condition'].config(text="N/A")

        # Session duration
        duration = datetime.now() - self.session_start
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.stats_labels['session_duration'].config(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

        # Data points (mock)
        self.stats_labels['data_points'].config(
            text=str(len(self.prediction_history) * 100)
        )

        # API requests (mock)
        self.stats_labels['api_requests'].config(
            text=str(len(self.prediction_history) * 5)
        )
