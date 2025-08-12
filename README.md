# Sensor-Based Automatic Crack Detection System (ACDS)

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)

ACDS: An IoT-based system for real-time, automatic crack detection in concrete using machine learning . It leverages sensor data (stress/strain) to classify crack severity and provide early warnings for structural health monitoring, moving beyond traditional visual inspection.

![ACDS GUI](https://github.com/AnshuMohanan/Automatic-Crack-Detection-System-/blob/main/GUI/dashboard.png)

---

## Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [The Machine Learning Model](#the-machine-learning-model)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Mode 1: Batch Processing](#mode-1-batch-processing)
  - [Mode 2: Real-Time Simulation](#mode-2-real-time-simulation)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

---

## About The Project

Traditional methods for inspecting civil structures like bridges and buildings are often manual, subjective, and unsafe. They typically only identify surface-level cracks after they have already formed. This project, the **Automatic Crack Detection System (ACDS)**, addresses these limitations by providing an automated, real-time solution for structural health monitoring.

Instead of relying on cameras, ACDS uses data from physical sensors (like **strain gauges** and **load cells**) to capture the stress and strain on a concrete structure. This data is fed into a machine learning model that can predict the structural integrity *before* cracks become visible to the naked eye. The system is designed to be low-cost, scalable, and deployable for both laboratory testing and on-site field monitoring.

---

## Key Features

- **🧠 Real-Time Prediction**: Classifies the health of a concrete structure into five severity levels, from "No Crack" to "Large Crack Formed."
- **📊 Multi-System Dashboard**: A user-friendly GUI built with Tkinter allows for the simultaneous monitoring of up to three independent systems.
- **📂 Batch Data Processing**: Analyze pre-recorded datasets from CSV or Excel files to visualize crack formation over time.
- **📈 Dynamic Visualization**: Plots a color-coded stress-strain curve in real-time, providing an intuitive visual representation of the structure's current state.
- **⚡ High Performance**: Powered by a lightweight Logistic Regression model that achieves **93.75% accuracy** with an extremely fast inference time, making it ideal for real-time applications.
- **🔌 Live IoT Integration**: Connects directly to an MQTT broker to stream and process live sensor data from microcontrollers like an ESP32 in real-time.

---

## System Architecture

The system follows a logical flow from data acquisition to user-facing insights.

1.  **Data Acquisition**: Strain gauges and load cells are attached to a concrete beam. An ESP32/ESP8266 microcontroller reads the analog sensor data.
2.  **Data Transmission**: The microcontroller reads sensor values and publishes them as a JSON payload to a central MQTT broker on a specific topic (MQTT_TOPIC).
3.  **Dashboard Connection**: The user clicks "Connect Live Sensor" in the GUI. The application subscribes to the MQTT topic to listen for incoming data.
4.  **Remote Start Command**: Upon successful connection, the application publishes a START message to a command topic (MQTT_COMMAND_TOPIC) to signal the microcontroller to begin sending data.
5.  **Real-Time Processing**: For each incoming data point, the RealTimeProcessor smooths the values, calculates engineered features, and feeds them into the pre-trained machine learning model.
6.  **ML Prediction**: The preprocessed data is fed into the trained Logistic Regression model, which classifies the current state into one of the five crack categories.
7.  **Visualization & Alerts**: The Tkinter GUI plots the data on the stress-strain graph, updates the status label with a color-coded prediction, and logs the activity. It can provide alerts if a critical crack stage is detected.

---

## The Machine Learning Model

The core of this system is a **Logistic Regression** classifier. After evaluating six different algorithms (including Random Forest, XGBoost, and SVM), Logistic Regression was chosen for its optimal balance of high accuracy and low inference time.

- **Model**: Logistic Regression
- **Accuracy**: **93.75%** (on the test set)
- **Inference Time**: ~0.000009 seconds per prediction
- **Classification Labels**:
    - `0` - No Crack (Safe)
    - `1` - Minute Crack Forming
    - `2` - Minute Crack Formed
    - `3` - Large Crack Forming
    - `4` - Large Crack Formed

The model was trained on a dataset generated from eight reinforced concrete beam specimens under controlled loading conditions.

---

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites
```sh
pandas
scikit-learn
numpy
matplotlib
openpyxl
joblib
paho-mqtt
```
### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/AnshuMohanan/Automatic-Crack-Detection-System-.git
    cd Automatic-Crack-Detection-System-
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Add Pre-trained Models:**
    This application requires the pre-trained model and scaler files. Please place `model.pkl` and `scaler.pkl` into the `models` directory (you may need to create this folder).

---

## Usage

Once the installation is complete, you can launch the dashboard.

```sh
python main.py
```

The application has two primary modes of operation, accessible from the GUI.

### Mode 1: Batch Processing

This mode is for analyzing existing data files.

1.  In one of the system frames (e.g., "System 1"), click **Upload Data (Batch)**.
2.  Select a `.csv` or `.xlsx` file containing the sensor data.
3.  After the file is processed, click **Monitor Batch Data**.
4.  The system will visualize the entire dataset row-by-row on the stress-strain graph.

### Mode 2: Real-Time Simulation

This mode simulates a live feed of sensor data from a file.

1.  **Configure MQTT Settings**: Before launching, open the config.py file and update the following MQTT credentials:
```sh
# --- MQTT Configuration ---
MQTT_BROKER = "your_broker_address"
MQTT_PORT = *** # Your broker's port
MQTT_USER = "your_username"
MQTT_PASS = "your_password"
MQTT_TOPIC = "sensor/data/topic"
MQTT_COMMAND_TOPIC = "sensor/command/topic"
```
2. Start Monitoring: In the GUI, click the Connect Live Sensor button.
3. **View Live Data**: The application will attempt to connect to the broker. Once connected, it will listen for data and update the plot and status in real-time as sensor readings are received.
4. **Disconnect**: Click Disconnect Sensor to stop monitoring and close the connection.

Note: This "live" mode simulates a real-time feed using data from a pre-recorded file. This approach was necessary as access to a lab with the required professional equipment was not available.

[▶️ Watch the Live Simulation Video](https://drive.google.com/file/d/1LiZXKcTF943unkCOa2lLIoZv6bomhIiH/view?usp=sharing)

---

## Technologies Used

- **Backend**: Python
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **IoT Communication**: Paho-MQTT
- **GUI**: Tkinter
- **Data Visualization**: Matplotlib
- **Model Persistence**: Joblib

---

## License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

---

## Authors

This project is based on the research paper by:

- **Anshu Mohanan**
- **Gishnu Ravindran**
- **Jibin Bino**
- **Prannoy Roy**
- **Dr. Starlet Ben Alex**

*Department of Electronics and Communication Engineering, Saintgits College of Engineering (Autonomous), Kottayam, India.*

---

## Acknowledgments

- Thanks to the technicians and staff at the engineering lab for their support during the experimental phase of this research.
- The comprehensive journal article provided a clear and detailed foundation for this project's documentation.
