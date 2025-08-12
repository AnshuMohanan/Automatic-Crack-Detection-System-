#include <SD.h>
#include "config.h"
#include "data_handler.h"

// --- Module-specific Globals ---
unsigned long lastSendAttempt = 0;
const long sendInterval = 5000; // Try to send data every 5 seconds

// --- Global Library Instances (defined in config.h) ---
WiFiClientSecure espClient;
PubSubClient client(espClient);
HX711 loadCell;
HX711 strainGauge;

// --- Forward Declarations for internal functions ---
void reconnectMQTT();
void saveDataToSD(String dataLine);
void sendDataFromSD();


void setupDataHandler() {
  Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization failed! System halted.");
    while (1);
  }
  Serial.println("Initialization done.");

  loadCell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  strainGauge.begin(STRAINGAUGE_DOUT_PIN, STRAINGAUGE_SCK_PIN);
  Serial.println("Taring sensors... Please wait.");
  delay(2000);
  loadCell.tare();
  strainGauge.tare();
  Serial.println("Tare complete.");

  espClient.setInsecure();
  client.setServer(mqtt_server, mqtt_port);
}

void handleDataAndMqtt() {
  // This function only runs if Wi-Fi is already connected.
  digitalWrite(WIFI_LED_PIN, HIGH);

  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  if (client.connected()) {
    String payload = "{";
    payload += "\"load_cell\":" + String(loadCell.get_value(5)) + ",";
    payload += "\"strain_gauge\":" + String(strainGauge.get_value(5));
    payload += "}";

    saveDataToSD(payload);

    if (millis() - lastSendAttempt > sendInterval) {
      sendDataFromSD();
      lastSendAttempt = millis();
    }
  }
}

// --- Paste the full functions from your original code here ---
// reconnectMQTT()
// saveDataToSD()
// sendDataFromSD()

// NOTE: Just like before, copy and paste the full implementations of these
// functions from your .ino file into this .cpp file.
// For example:
void reconnectMQTT() {
  digitalWrite(MQTT_LED_PIN, LOW);
  while (!client.connected()) {
    // ... rest of the function
  }
}

void saveDataToSD(String dataLine) {
    // ... entire function
}

void sendDataFromSD() {
    // ... entire function
}
