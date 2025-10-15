"""
Model management module for simulating ML model operations
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import random
from datetime import datetime
from config import MODEL_TYPES, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER


class ModelManager:
    """Manages model operations (loading, training, inference)"""

    def __init__(self):
        self.current_model = None
        self.model_status = 'Idle'
        self.is_training = False
        self.is_inferencing = False
        self.training_progress = 0
        self.training_metrics = {}

    def load_model(self, filepath):
        """Simulate loading a model file"""
        time.sleep(1)  # Simulate loading time
        model_name = filepath.split('/')[-1] if filepath else 'default_model.h5'
        self.current_model = {
            'name': model_name,
            'type': random.choice(MODEL_TYPES),
            'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'parameters': random.randint(100000, 5000000),
            'accuracy': round(random.uniform(0.85, 0.98), 3)
        }
        self.model_status = 'Ready'
        return self.current_model

    def start_training(self, epochs=10):
        """Simulate model training"""
        self.is_training = True
        self.model_status = 'Training'
        self.training_progress = 0

        def train():
            for epoch in range(epochs):
                if not self.is_training:
                    break

                # Simulate training metrics
                self.training_metrics = {
                    'epoch': epoch + 1,
                    'loss': round(1.0 - (epoch / epochs) * 0.7 + random.uniform(-0.05, 0.05), 4),
                    'accuracy': round((epoch / epochs) * 0.85 + 0.15 + random.uniform(-0.02, 0.02), 4),
                    'val_loss': round(1.0 - (epoch / epochs) * 0.6 + random.uniform(-0.05, 0.05), 4),
                    'val_accuracy': round((epoch / epochs) * 0.80 + 0.20 + random.uniform(-0.02, 0.02), 4)
                }
                self.training_progress = int((epoch + 1) / epochs * 100)
                time.sleep(2)  # Simulate epoch time

            self.is_training = False
            self.model_status = 'Ready'
            self.training_progress = 100

        thread = threading.Thread(target=train, daemon=True)
        thread.start()

    def stop_training(self):
        """Stop training simulation"""
        self.is_training = False
        self.model_status = 'Ready'

    def start_inference(self):
        """Start inference mode"""
        if self.current_model is None:
            return False
        self.is_inferencing = True
        self.model_status = 'Inference'
        return True

    def stop_inference(self):
        """Stop inference mode"""
        self.is_inferencing = False
        self.model_status = 'Ready'

    def get_model_info(self):
        """Get current model information"""
        return self.current_model

    def get_status(self):
        """Get current model status"""
        return {
            'status': self.model_status,
            'is_training': self.is_training,
            'is_inferencing': self.is_inferencing,
            'training_progress': self.training_progress,
            'training_metrics': self.training_metrics,
            'model': self.current_model
        }


class ModelControlPanel(ttk.Frame):
    """UI panel for model control and management"""

    def __init__(self, parent, model_manager):
        super().__init__(parent)
        self.model_manager = model_manager
        self._setup_ui()

    def _setup_ui(self):
        """Setup the model control panel UI"""
        # Title
        title = ttk.Label(
            self,
            text="Model Management",
            font=('Arial', 14, 'bold')
        )
        title.pack(pady=10)

        # Model Info Section
        info_frame = ttk.LabelFrame(self, text="Model Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.model_info_text = tk.Text(info_frame, height=6, width=40, font=('Courier', 9))
        self.model_info_text.pack(fill=tk.X)
        self.model_info_text.insert('1.0', 'No model loaded')
        self.model_info_text.config(state=tk.DISABLED)

        # Model Selection
        selection_frame = ttk.Frame(self)
        selection_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(
            selection_frame,
            text="Load Model",
            command=self._load_model
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            selection_frame,
            text="Create New Model",
            command=self._create_model
        ).pack(side=tk.LEFT, padx=5)

        # Training Section
        training_frame = ttk.LabelFrame(self, text="Training", padding=10)
        training_frame.pack(fill=tk.X, padx=10, pady=5)

        # Epochs selection
        epochs_frame = ttk.Frame(training_frame)
        epochs_frame.pack(fill=tk.X, pady=5)
        ttk.Label(epochs_frame, text="Epochs:").pack(side=tk.LEFT)
        self.epochs_var = tk.IntVar(value=10)
        epochs_spinbox = ttk.Spinbox(
            epochs_frame,
            from_=1,
            to=100,
            textvariable=self.epochs_var,
            width=10
        )
        epochs_spinbox.pack(side=tk.LEFT, padx=5)

        # Training buttons
        btn_frame = ttk.Frame(training_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.train_btn = ttk.Button(
            btn_frame,
            text="Start Training",
            command=self._start_training
        )
        self.train_btn.pack(side=tk.LEFT, padx=5)

        self.stop_train_btn = ttk.Button(
            btn_frame,
            text="Stop Training",
            command=self._stop_training,
            state=tk.DISABLED
        )
        self.stop_train_btn.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            training_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Training metrics
        self.metrics_text = tk.Text(training_frame, height=5, width=40, font=('Courier', 9))
        self.metrics_text.pack(fill=tk.X, pady=5)

        # Inference Section
        inference_frame = ttk.LabelFrame(self, text="Inference", padding=10)
        inference_frame.pack(fill=tk.X, padx=10, pady=5)

        self.inference_btn = ttk.Button(
            inference_frame,
            text="Start Inference",
            command=self._start_inference
        )
        self.inference_btn.pack(side=tk.LEFT, padx=5)

        self.stop_inference_btn = ttk.Button(
            inference_frame,
            text="Stop Inference",
            command=self._stop_inference,
            state=tk.DISABLED
        )
        self.stop_inference_btn.pack(side=tk.LEFT, padx=5)

        # Status indicator
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.status_label = ttk.Label(
            status_frame,
            text="Idle",
            font=('Arial', 10),
            foreground='gray'
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Start update loop
        self._update_status()

    def _load_model(self):
        """Handle load model button"""
        filepath = filedialog.askopenfilename(
            title="Select Model File",
            filetypes=[
                ("Model files", "*.h5 *.pt *.pth *.pkl"),
                ("All files", "*.*")
            ]
        )
        if filepath:
            # Simulate loading in background
            def load():
                model = self.model_manager.load_model(filepath)
                self._update_model_info(model)
                messagebox.showinfo("Success", f"Model loaded: {model['name']}")

            thread = threading.Thread(target=load, daemon=True)
            thread.start()

    def _create_model(self):
        """Create a new mock model"""
        model = self.model_manager.load_model("new_model.h5")
        self._update_model_info(model)
        messagebox.showinfo("Success", "New model created successfully")

    def _update_model_info(self, model):
        """Update model information display"""
        if model:
            info = f"""Name: {model['name']}
Type: {model['type']}
Loaded: {model['loaded_at']}
Parameters: {model['parameters']:,}
Accuracy: {model['accuracy']:.1%}"""
            self.model_info_text.config(state=tk.NORMAL)
            self.model_info_text.delete('1.0', tk.END)
            self.model_info_text.insert('1.0', info)
            self.model_info_text.config(state=tk.DISABLED)

    def _start_training(self):
        """Start training"""
        if self.model_manager.current_model is None:
            messagebox.showwarning("Warning", "Please load a model first")
            return

        epochs = self.epochs_var.get()
        self.model_manager.start_training(epochs)
        self.train_btn.config(state=tk.DISABLED)
        self.stop_train_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Training Started", f"Training for {epochs} epochs")

    def _stop_training(self):
        """Stop training"""
        self.model_manager.stop_training()
        self.train_btn.config(state=tk.NORMAL)
        self.stop_train_btn.config(state=tk.DISABLED)

    def _start_inference(self):
        """Start inference"""
        if not self.model_manager.start_inference():
            messagebox.showwarning("Warning", "Please load a model first")
            return

        self.inference_btn.config(state=tk.DISABLED)
        self.stop_inference_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Inference Started", "Model is now running inference")

    def _stop_inference(self):
        """Stop inference"""
        self.model_manager.stop_inference()
        self.inference_btn.config(state=tk.NORMAL)
        self.stop_inference_btn.config(state=tk.DISABLED)

    def _update_status(self):
        """Update status display"""
        status = self.model_manager.get_status()

        # Update status label
        self.status_label.config(text=status['status'])

        # Update color based on status
        if status['status'] == 'Training':
            self.status_label.config(foreground='orange')
        elif status['status'] == 'Inference':
            self.status_label.config(foreground='green')
        elif status['status'] == 'Ready':
            self.status_label.config(foreground='blue')
        else:
            self.status_label.config(foreground='gray')

        # Update training progress
        if status['is_training']:
            self.progress_var.set(status['training_progress'])

            # Update metrics
            if status['training_metrics']:
                metrics = status['training_metrics']
                metrics_text = f"""Epoch: {metrics['epoch']}
Loss: {metrics['loss']:.4f}  |  Accuracy: {metrics['accuracy']:.4f}
Val Loss: {metrics['val_loss']:.4f}  |  Val Acc: {metrics['val_accuracy']:.4f}"""
                self.metrics_text.delete('1.0', tk.END)
                self.metrics_text.insert('1.0', metrics_text)

        # Schedule next update
        self.after(100, self._update_status)
