/*
  Main project file. Initializes and coordinates all modules.
  - Author: [ANSHU MOHANAN]
  - Author: [GISHNU RAVINDRAN]
  - Author: [PRANNOY ROY]
  - Author: [JIBIN BINO]
  - Project:[Automatic Crack Detection System (ACDS)]
*/

// --- Core Libraries (include these here as they are fundamental) ---
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// --- Custom Modules ---
#include "config.h"       // All configuration and global variables
#include "wifi_manager.h" // Handles all Wi-Fi connectivity logic
#include "data_handler.h" // Handles sensors, SD card, and MQTT data

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- Combined Data Logger & Wi-Fi Manager ---");

  // Initialize all modules by calling their setup functions
  setupWifiManager();
  setupDataHandler();

  Serial.println("--- System Initialization Complete ---");
}

void loop() {
  // The main loop is now very simple and readable.
  // Each function handles its own state and logic.

  // 1. Ensure Wi-Fi is connected. This function will block and handle
  // reconnection (auto or manual) if the connection is lost.
  handleWifiConnection();

  // 2. If Wi-Fi is connected, this function will manage MQTT connection,
  // read sensors, log to SD, and send data.
  handleDataAndMqtt();
}
