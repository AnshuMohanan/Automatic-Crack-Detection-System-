# Automatic-Crack-Detection-System-
ACDS: An IoT-based system for real-time, automatic crack detection in concrete using machine learning . It leverages sensor data (stress/strain) to classify crack severity and provide early warnings for structural health monitoring, moving beyond traditional visual inspection.

# 🛠️ Sensor-Based Automatic Crack Detection System (ACDS)

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)

A real-time structural health monitoring system that uses sensor data and machine learning to predict and classify concrete crack severity. This project provides a desktop GUI for live monitoring, batch data analysis, and visualization.

![ACDS GUI](https://i.imgur.com/qL6W20Q.png)

---

## 📋 Table of Contents

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

## 📖 About The Project

Traditional methods for inspecting civil structures like bridges and buildings are often manual, subjective, and unsafe. They typically only identify surface-level cracks after they have already formed. This project, the **Automatic Crack Detection System (ACDS)**, addresses these limitations by providing an automated, real-time solution for structural health monitoring.

Instead of relying on cameras, ACDS uses data from physical sensors (like **strain gauges** and **load cells**) to capture the stress and strain on a concrete structure. This data is fed into a machine learning model that can predict the structural integrity *before* cracks become visible to the naked eye. The system is designed to be low-cost, scalable, and deployable for both laboratory testing and on-site field monitoring.

---

## ✨ Key Features

- **🧠 Real-Time Prediction**: Classifies the health of a concrete structure into five severity levels, from "No Crack" to "Large Crack Formed."
- **📊 Multi-System Dashboard**: A user-friendly GUI built with Tkinter allows for the simultaneous monitoring of up to three independent systems.
- **📂 Batch Data Processing**: Analyze pre-recorded datasets from CSV or Excel files to visualize crack formation over time.
- **📈 Dynamic Visualization**: Plots a color-coded stress-strain curve in real-time, providing an intuitive visual representation of the structure's current state.
- **⚡ High Performance**: Powered by a lightweight Logistic Regression model that achieves **93.75% accuracy** with an extremely fast inference time, making it ideal for real-time applications.
- **🔌 IoT-Ready Architecture**: Designed to integrate with microcontrollers like ESP32/ESP8266 for live data streaming from embedded sensors.

---

## 🏗️ System Architecture

The system follows a logical flow from data acquisition to user-facing insights.

1.  **Data Acquisition**: Strain gauges and load cells are attached to a concrete beam. An ESP32/ESP8266 microcontroller reads the analog sensor data.
2.  **Data Transmission**: The microcontroller wirelessly transmits the stress and strain data to the central processing unit (the PC running the dashboard).
3.  **Data Preprocessing**: Raw sensor values are received and preprocessed. This includes scaling the data and performing feature engineering to create new metrics like slope, stress/strain difference, and a stress-strain curve score.
4.  **ML Prediction**: The preprocessed data is fed into the trained Logistic Regression model, which classifies the current state into one of the five crack categories.
5.  **Visualization & Alerts**: The Tkinter GUI plots the data on the stress-strain graph, updates the status label with a color-coded prediction, and logs the activity. It can provide alerts if a critical crack stage is detected.

---

## 🧠 The Machine Learning Model

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

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- [Python](https://www.python.org/downloads/) (3.9 or newer)
- [Git](https://git-scm.com/downloads)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-project-name.git](https://github.com/your-username/your-project-name.git)
    cd your-project-name
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

## ▶️ Usage

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

1.  Click **Start Real-Time Simulation**.
2.  Select a `.csv` or `.xlsx` file to act as the source for the data stream.
3.  The application will process the data one entry at a time, updating the plot and status label in real-time.

---

## 💻 Technologies Used

- **Backend**: Python
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **GUI**: Tkinter
- **Data Visualization**: Matplotlib
- **Model Persistence**: Joblib

---

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

---

## 🧑‍💻 Authors

This project is based on the research paper by:

- **Anshu Mohanan**
- **Gishnu Ravindran**
- **Jibin Bino**
- **Prannoy Roy**
- **Dr. Starlet Ben Alex**

*Department of Electronics and Communication Engineering, Saintgits College of Engineering (Autonomous), Kottayam, India.*

---

## 🙏 Acknowledgments

- Thanks to the technicians and staff at the structural engineering lab for their support during the experimental phase of this research.
- The comprehensive journal article provided a clear and detailed foundation for this project's documentation.
