# Automatic Crack Detection System (ACDS) - Data Logger

This repository contains the source code for the data acquisition and transmission unit of the Automatic Crack Detection System (ACDS). This firmware is designed for an ESP8266 microcontroller and is responsible for reading sensor data, logging it to an SD card, and transmitting it to an MQTT server for further analysis.

The system is built to be robust, featuring a smart Wi-Fi manager that can store multiple network credentials and an offline-first data logging approach to prevent data loss.

## Authors
- **Anshu Mohanan**
- **Gishnu Ravindran**
- **Prannoy Roy**
- **Jibin Bino**

---

## Table of Contents

- [Features](#Features)
- [Hardware Requirements](#Hardware-Requirements)
- [Software & Libraries](#Software-&-Libraries)
- [How to Use](#How-to-Use)
- [File Structure](#File-Structure)

---

## Features

- **Smart Wi-Fi Manager**:
    - Automatically scans for and connects to known Wi-Fi networks.
    - Stores up to 5 Wi-Fi credentials in permanent memory (EEPROM).
    - Provides an interactive setup via the Serial Monitor to add or replace Wi-Fi networks if no known networks are found.
- **Robust Data Logging**:
    - Reads data from a load cell and a strain gauge using two HX711 amplifiers.
    - Saves every sensor reading to a microSD card, ensuring no data is lost during network outages.
- **Reliable MQTT Communication**:
    - Periodically sends all stored data from the SD card to a secure MQTT broker.
    - If a data transmission fails, the data is kept on the SD card to be sent later.
    - Uses status LEDs to provide a visual indication of Wi-Fi and MQTT connection status.
- **Modular Codebase**:
    - The code is split into logical modules (`wifi_manager`, `data_handler`) for better readability, maintenance, and scalability.

---

## Hardware Requirements

- **Microcontroller**: ESP8266 (NodeMCU, Wemos D1 Mini, or similar)
- **Sensors**:
    - 1 x Load Cell
    - 1 x Strain Gauge
- **Amplifiers**: 2 x HX711 Load Cell Amplifier Modules
- **Storage**: MicroSD Card Module & a MicroSD Card
- **Indicators**: 2 x LEDs (for Wi-Fi and MQTT status)
- **Power Supply**: 5V power supply suitable for the ESP8266 and sensors.

---

## Software & Libraries

This project is built using the Arduino IDE. You will need to install the following libraries:

- `ESP8266WiFi` (usually included with the ESP8266 board manager)
- `PubSubClient` by Nick O'Leary
- `HX711_ADC` by Olav Kallhovd (or a similar HX711 library)

---

## How to Use

1.  **Clone the Repository**:
    ```sh
    git clone https://github.com/AnshuMohanan/Automatic-Crack-Detection-System-
    ```

2.  **Configure the Project**:
    Open the `config.h` file. This is the central place for all your settings.
    - **MQTT Credentials**: Fill in your `mqtt_server`, `mqtt_port`, `mqtt_user`, `mqtt_pass`, and `mqtt_topic`.
    - **Pin Definitions**: Ensure the pin numbers for the LEDs, sensors, and SD card match your hardware wiring.

3.  **Upload the Code**:
    - Open the `Data_Transfer_Sender.ino` file in the Arduino IDE.
    - Select the correct ESP8266 board and COM port.
    - Click "Upload".

4.  **First-Time Wi-Fi Setup**:
    - After uploading, open the Serial Monitor (set baud rate to 115200).
    - The device will scan for networks. If it doesn't find a network it knows, it will start the manual setup process.
    - Follow the on-screen prompts to select a Wi-Fi network and enter the password.
    - The credentials will be saved, and the device will automatically connect on the next boot.

---

## File Structure

The project is organized into several files to keep the code clean and manageable:

- **`Data_Transfer_Sender.ino`**: The main sketch file. Contains the `setup()` and `loop()` functions and coordinates the different modules.
- **`config.h`**: A configuration file to store all pins, credentials, and global settings. **This is the main file you need to edit.**
- **`wifi_manager.h` / `.cpp`**: This module handles all Wi-Fi related tasks, including scanning, connecting, and saving credentials.
- **`data_handler.h` / `.cpp`**: This module is responsible for initializing sensors, reading data, saving to the SD card, and communicating with the MQTT server.


