# gui.py

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import threading
import time
import os
import json

# Import Paho MQTT client
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

# Import application components and settings
import config
from data_processor import RealTimeProcessor, process_dataframe_for_batch_prediction

# ==============================================================================
# == 🚀 UNIFIED GUI APPLICATION
# ==============================================================================

class UnifiedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Unified Crack Detection Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f2f5")

        try:
            self.model = joblib.load(config.MODEL_PATH)
            self.scaler = joblib.load(config.SCALER_PATH)
        except FileNotFoundError as e:
            messagebox.showerror("Fatal Error", f"Could not find required file: {e.filename}.")
            root.destroy()
            return

        self.datasets = {}
        self._build_ui()

    def _build_ui(self):
        content = tk.Frame(self.root, bg="#f0f2f5")
        content.pack(side="top", fill="both", expand=True)
        tk.Label(content, text="🛠 Crack Detection System (Multi-Mode)", font=("Arial", 22, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=10)

        systems_frame = tk.Frame(content, bg="#f0f2f5")
        systems_frame.pack(pady=10, expand=True)
        for name in ["System 1", "System 2", "System 3"]:
            self.create_system_frame(systems_frame, name)

        status_bar = tk.Label(self.root, text="🔎 Ready", bd=1, relief=tk.SUNKEN, anchor="w", font=("Arial", 10), bg="#e0e0e0")
        status_bar.pack(side="bottom", fill="x")

    def create_system_frame(self, parent, system_name):
        system_frame = tk.Frame(parent, bg="#f0f2f5", padx=10, pady=10)
        system_frame.pack(side="left", padx=20, fill="y", expand=True)
        tk.Label(system_frame, text=system_name, font=("Arial", 16, "bold"), bg="#f0f2f5").pack(pady=5)

        tk.Button(system_frame, text="Upload Data (Batch)", command=lambda: self.upload_batch_data(system_name), font=("Arial", 12)).pack(pady=5, fill="x")
        tk.Button(system_frame, text="Monitor Batch Data", command=lambda: self.start_batch_monitoring(system_name), font=("Arial", 12)).pack(pady=5, fill="x")
        
        # --- MODIFIED: Real-time buttons ---
        connect_btn = tk.Button(system_frame, text="Connect Live Sensor", command=lambda: self.start_live_monitoring(system_name), font=("Arial", 12, "bold"), bg="#27ae60", fg="white")
        connect_btn.pack(pady=10, fill="x")
        disconnect_btn = tk.Button(system_frame, text="Disconnect Sensor", command=lambda: self.stop_live_monitoring(system_name), font=("Arial", 12), bg="#c0392b", fg="white", state="disabled")
        disconnect_btn.pack(pady=5, fill="x")
        # ------------------------------------

        result_label = tk.Label(system_frame, text="No data loaded.", font=("Arial", 12), bg="#f0f2f5", fg="#34495e")
        result_label.pack(pady=10)

        fig, ax = plt.subplots(figsize=(5, 3))
        canvas = FigureCanvasTkAgg(fig, master=system_frame)
        canvas.get_tk_widget().pack(pady=5, fill="x")
        
        log_text = tk.Text(system_frame, height=10, width=50, font=("Courier", 10), state="disabled")
        log_text.pack(pady=5, fill="both", expand=True)

        self.datasets[system_name] = {
            "result_label": result_label, "ax": ax, "canvas": canvas, "log_text": log_text,
            "batch_data": None, "processor": RealTimeProcessor(self.model, self.scaler), 
            "simulation_running": False, "plot_data": {'stress': [], 'strain': []},
            "mqtt_client": None, "connect_btn": connect_btn, "disconnect_btn": disconnect_btn
        }
        self.setup_plot(system_name)

    def setup_plot(self, system_name):
        ax = self.datasets[system_name]["ax"]
        ax.clear()
        legend_labels = [plt.Line2D([0], [0], color=config.COLOR_MAPPING[i], lw=2, label=config.CRACK_CONDITIONS[i]) for i in range(5)]
        ax.legend(handles=legend_labels, loc='upper left', fontsize='small')
        ax.set_title(f"Stress-Strain - {system_name}")
        ax.set_xlabel("Strain")
        ax.set_ylabel("Stress (MPa)")
        self.datasets[system_name]["canvas"].draw()

    # --- Batch Processing Methods (Unchanged) ---
    def upload_batch_data(self, system_name):
        file_path = filedialog.askopenfilename(filetypes=[("Excel/CSV Files", "*.xlsx *.csv")])
        if not file_path: return
        try:
            df_raw = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            processed_df = process_dataframe_for_batch_prediction(df_raw)
            feature_columns = ['STRESS', 'STRAIN', 'SLOPE', 'STRESS DIFFERENCE', 'STRAIN DIFFERENCE', 'SUDDEN DROP FLAG', 'SUDDEN RISE FLAG', 'STRESS CURVE']
            predictions = self.model.predict(processed_df[feature_columns])
            processed_df['Status'] = predictions
            
            self.datasets[system_name]["batch_data"] = processed_df
            self.datasets[system_name]["result_label"].config(text="✅ Batch data processed.")
            self.log_result(system_name, f"Batch file loaded: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process batch file: {e}")

    def start_batch_monitoring(self, system_name):
        if self.datasets[system_name]["batch_data"] is None:
            messagebox.showwarning("No Data", "Please upload batch data first.")
            return
        threading.Thread(target=self._run_batch_visualization, args=(system_name,), daemon=True).start()

    def _run_batch_visualization(self, system_name):
        info = self.datasets[system_name]
        self.root.after(0, self.setup_plot, system_name)
        plot_data = {'stress': [], 'strain': []}
        for _, row in info["batch_data"].iterrows():
            stress, strain, status = row['Original_Stress'], row['Original_Strain'], row['Status']
            self.root.after(0, self.update_gui_elements, system_name, stress, strain, status, plot_data)
            time.sleep(0.1)
        self.root.after(0, self.log_result, system_name, "Batch monitoring complete.")

    # --- NEW: Real-Time MQTT Monitoring Methods ---
    def start_live_monitoring(self, system_name):
        info = self.datasets[system_name]
        if info["simulation_running"]:
            messagebox.showwarning("Warning", "Live monitoring is already active.")
            return

        info["simulation_running"] = True
        info["connect_btn"].config(state="disabled")
        info["disconnect_btn"].config(state="normal")
        info["processor"].buffer.clear()
        info["plot_data"] = {'stress': [], 'strain': []}
        self.setup_plot(system_name)
        self.log_result(system_name, "🚀 Attempting to connect to live sensor...")

        try:
            client = mqtt.Client(CallbackAPIVersion.VERSION2)
            info["mqtt_client"] = client
            
            # Assign callbacks with context using lambda
            client.on_connect = lambda c, u, f, rc, p: self._on_mqtt_connect(c, u, f, rc, p, system_name)
            client.on_message = lambda c, u, msg: self._on_mqtt_message(c, u, msg, system_name)
            
            client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)
            client.tls_set()
            client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
            client.loop_start()
        except Exception as e:
            self.log_result(system_name, f"❌ MQTT Connection Error: {e}")
            messagebox.showerror("Connection Error", f"Could not connect to MQTT broker: {e}")
            self.stop_live_monitoring(system_name) # Reset GUI state

    def _on_mqtt_connect(self, client, userdata, flags, rc, properties, system_name):
        if rc == 0:
            self.root.after(0, self.log_result, system_name, "✅ Connected to MQTT Broker!")
            self.root.after(0, self.log_result, system_name, f"   Subscribing to topic: {config.MQTT_TOPIC}")
            client.subscribe(config.MQTT_TOPIC)
            
            self.root.after(0, self.log_result, system_name, f"--> Sending 'START' command...")
            client.publish(config.MQTT_COMMAND_TOPIC, "START", qos=1)
        else:
            self.root.after(0, self.log_result, system_name, f"❌ Failed to connect, return code {rc}")
            self.root.after(0, self.stop_live_monitoring, system_name)

    def _on_mqtt_message(self, client, userdata, msg, system_name):
        try:
            payload = json.loads(msg.payload.decode())
            load_kn = payload.get("load_cell")
            lvdt_mm = payload.get("strain_gauge")

            if load_kn is not None and lvdt_mm is not None:
                info = self.datasets[system_name]
                processor = info["processor"]
                plot_data = info["plot_data"]
                
                stress, strain, status = processor.process_new_reading(load_kn, lvdt_mm)
                self.root.after(0, self.update_gui_elements, system_name, stress, strain, status, plot_data)
            else:
                self.root.after(0, self.log_result, system_name, f"⚠️ Received malformed data: {msg.payload.decode()}")
        except Exception as e:
            self.root.after(0, self.log_result, system_name, f"Error processing message: {e}")
            
    def stop_live_monitoring(self, system_name):
        info = self.datasets[system_name]
        if info["mqtt_client"]:
            info["mqtt_client"].loop_stop()
            info["mqtt_client"].disconnect()
            self.log_result(system_name, "⏹️ Sensor connection closed.")
        
        info["simulation_running"] = False
        info["mqtt_client"] = None
        info["connect_btn"].config(state="normal")
        info["disconnect_btn"].config(state="disabled")

    # --- Unified GUI Update Methods (Unchanged) ---
    def update_gui_elements(self, system_name, stress, strain, status_code, plot_data):
        info = self.datasets[system_name]
        status_text = config.CRACK_CONDITIONS.get(status_code, "Unknown")
        status_color = config.COLOR_MAPPING.get(status_code, "black")
        
        info["result_label"].config(text=f"Current Status: {status_text}", fg=status_color)
        self.log_result(system_name, f"Stress: {stress:.2f}, Strain: {strain:.4f} -> {status_text}")
        self._update_plot(system_name, stress, strain, status_code, plot_data)

    def _update_plot(self, system_name, stress, strain, status_code, plot_data):
        info = self.datasets[system_name]
        plot_data['stress'].append(stress)
        plot_data['strain'].append(strain)

        if len(plot_data['stress']) > 1:
            # For live data, the previous status is derived from the processor's last step.
            # We get the prediction and then plot the segment leading to it.
            # The color of a line segment is determined by the status of its STARTING point.
            
            # Get the previous status code to color the line segment correctly.
            # This logic needs to be robust. We can peek at the processor's buffer state if needed,
            # but for simplicity, we assume the previous point's status led to the current one.
            # Let's find the status of the previous point.
            # A simple way is to track the last status.
            
            prev_status = status_code # Fallback
            if 'last_status' in info:
                prev_status = info['last_status']
            
            if prev_status != -1:
                info["ax"].plot(plot_data['strain'][-2:], plot_data['stress'][-2:],
                               color=config.COLOR_MAPPING.get(prev_status, 'black'),
                               marker='o', markersize=4, linestyle='-')
                info["canvas"].draw()
        
        info['last_status'] = status_code


    def log_result(self, system_name, result):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_text = self.datasets[system_name]["log_text"]
        log_text.config(state="normal")
        log_text.insert("end", f"[{timestamp}] {result}\n")
        log_text.see("end")
        log_text.config(state="disabled")
