"""
Signal visualization module for real-time biosignal display
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
from collections import deque
from config import SIGNAL_TYPES, SIGNAL_BUFFER_SIZE, COLOR_BG


class SignalPlot(tk.Canvas):
    """Individual signal plot widget"""

    def __init__(self, parent, signal_type, width=600, height=150):
        super().__init__(parent, width=width, height=height, bg='white', highlightthickness=1)
        self.signal_type = signal_type
        self.signal_config = SIGNAL_TYPES[signal_type]
        self.width = width
        self.height = height
        self.padding = 40

        self.data_buffer = deque(maxlen=SIGNAL_BUFFER_SIZE)
        self.time_points = deque(maxlen=SIGNAL_BUFFER_SIZE)
        self.time_counter = 0

        self._setup_plot()

    def _setup_plot(self):
        """Setup plot axes and labels"""
        # Title
        self.create_text(
            self.width // 2, 15,
            text=f"{self.signal_config['name']} ({self.signal_config['unit']})",
            font=('Arial', 12, 'bold'),
            fill=self.signal_config['color']
        )

        # Axes
        self.create_line(
            self.padding, self.height - self.padding,
            self.width - 20, self.height - self.padding,
            fill='gray', width=2
        )
        self.create_line(
            self.padding, 30,
            self.padding, self.height - self.padding,
            fill='gray', width=2
        )

        # Y-axis labels
        y_min, y_max = self.signal_config['range']
        y_range = y_max - y_min
        for i in range(5):
            y_val = y_min + (y_range * i / 4)
            y_pos = self.height - self.padding - ((self.height - self.padding - 30) * i / 4)
            self.create_text(
                self.padding - 10, y_pos,
                text=f"{y_val:.0f}",
                font=('Arial', 8),
                anchor='e'
            )

    def add_data_point(self, value):
        """Add new data point and update plot"""
        self.data_buffer.append(value)
        self.time_points.append(self.time_counter)
        self.time_counter += 1
        self.update_plot()

    def update_plot(self):
        """Redraw the signal plot"""
        # Clear previous plot line (keep axes)
        self.delete('signal_line')
        self.delete('current_value')

        if len(self.data_buffer) < 2:
            return

        # Calculate scaling
        y_min, y_max = self.signal_config['range']
        y_range = max(y_max - y_min, 1)
        plot_height = self.height - self.padding - 30
        plot_width = self.width - self.padding - 20

        # Create line coordinates
        points = []
        for i, (time, value) in enumerate(zip(self.time_points, self.data_buffer)):
            x = self.padding + (i / max(len(self.data_buffer) - 1, 1)) * plot_width
            # Normalize value to plot range
            normalized = (value - y_min) / y_range
            y = self.height - self.padding - (normalized * plot_height)
            points.extend([x, y])

        # Draw signal line
        if len(points) >= 4:
            self.create_line(
                points,
                fill=self.signal_config['color'],
                width=2,
                smooth=True,
                tags='signal_line'
            )

        # Display current value
        if self.data_buffer:
            current_val = self.data_buffer[-1]
            self.create_text(
                self.width - 10, 15,
                text=f"{current_val:.1f}",
                font=('Arial', 11, 'bold'),
                fill=self.signal_config['color'],
                anchor='e',
                tags='current_value'
            )

    def clear(self):
        """Clear all data"""
        self.data_buffer.clear()
        self.time_points.clear()
        self.time_counter = 0
        self.delete('signal_line')
        self.delete('current_value')


class SignalVisualizerPanel(ttk.Frame):
    """Panel containing all signal plots"""

    def __init__(self, parent):
        super().__init__(parent)
        self.plots = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the visualization panel UI"""
        # Title
        title = ttk.Label(
            self,
            text="Real-Time Biosignal Monitoring",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10)

        # Create plots for each signal type
        plots_frame = ttk.Frame(self)
        plots_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for i, signal_type in enumerate(SIGNAL_TYPES.keys()):
            plot = SignalPlot(plots_frame, signal_type, width=650, height=140)
            plot.pack(pady=5, padx=5)
            self.plots[signal_type] = plot

    def update_signals(self, signal_data):
        """Update all signal plots with new data"""
        for signal_type, value in signal_data.items():
            if signal_type in self.plots:
                self.plots[signal_type].add_data_point(value)

    def clear_all(self):
        """Clear all plots"""
        for plot in self.plots.values():
            plot.clear()
