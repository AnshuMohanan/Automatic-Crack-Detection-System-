#include <SD.h>
#include "config.h"
#include "data_handler.h"

// --- Module-specific Globals ---
unsigned long lastSendAttempt = 0;
const long sendInterval = 5000; // Try to send data every 5 seconds
bool processStarted = false;     // NEW: Controls whether we send data or just store it

// --- Global Library Instances (defined in config.h) ---
WiFiClientSecure espClient;
PubSubClient client(espClient);
HX711 loadCell;
HX711 strainGauge;

// --- Forward Declarations for internal functions ---
void mqttCallback(char* topic, byte* payload, unsigned int length); // NEW
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
  client.setCallback(mqttCallback); // NEW: Set the function to handle incoming messages
}

void handleDataAndMqtt() {
  // This function only runs if Wi-Fi is already connected.
  digitalWrite(WIFI_LED_PIN, HIGH);

  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop(); // IMPORTANT: This processes incoming messages

  // STEP 1: Always read sensors and save to SD card, no matter what.
  String payload = "{";
  payload += "\"load_cell\":" + String(loadCell.get_value(5)) + ",";
  payload += "\"strain_gauge\":" + String(strainGauge.get_value(5));
  payload += "}";

  saveDataToSD(payload);

  // STEP 2: Only send data if the process has been started by the receiver.
  if (processStarted && client.connected()) {
    if (millis() - lastSendAttempt > sendInterval) {
      sendDataFromSD();
      lastSendAttempt = millis();
    }
  }
}

// --- NEW: This function is called whenever a message is received on a subscribed topic ---
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // Convert payload to a String for easy comparison
  payload[length] = '\0'; // Add a null terminator
  String message = String((char*)payload);

  Serial.print("MQTT Message Received [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);

  // Check if the message is on our command topic and if it's the "START" signal
  if (String(topic) == String(mqtt_command_topic) && message == "START") {
    Serial.println(">>> START Command Received! Beginning data transmission. <<<");
    processStarted = true;
    
    // Immediately try to send the backlog of data from the SD card
    sendDataFromSD();
    lastSendAttempt = millis();
  }
}

// --- MODIFIED: This function now also subscribes to the command topic ---
void reconnectMQTT() {
  digitalWrite(MQTT_LED_PIN, LOW);
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ACDS-ESP8266-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
      Serial.println("connected.");
      digitalWrite(MQTT_LED_PIN, HIGH);
      
      // Subscribe to the command topic to listen for the "START" signal
      client.subscribe(mqtt_command_topic);
      Serial.print("--> Subscribed to command topic: ");
      Serial.println(mqtt_command_topic);

    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// NOTE: You still need to paste your full implementations of
// saveDataToSD() and sendDataFromSD() here.
void saveDataToSD(String dataLine) {
    // ... your entire saveDataToSD function ...
}

void sendDataFromSD() {
    // ... your entire sendDataFromSD function ...
}
