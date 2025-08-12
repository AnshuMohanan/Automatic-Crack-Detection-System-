#ifndef CONFIG_H
#define CONFIG_H

#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include "HX711.h"

// --- Use header guards to prevent multiple inclusions ---

// --- LED Pin Definitions ---
const int WIFI_LED_PIN = D5; // GPIO14
const int MQTT_LED_PIN = D6; // GPIO12

// --- EEPROM Configuration for Wi-Fi Credentials ---
const int MAX_WIFI_CREDENTIALS = 5;
const int SSID_MAX_LEN = 32;
const int PASS_MAX_LEN = 64;
struct WifiCredential {
  char ssid[SSID_MAX_LEN + 1];
  char password[PASS_MAX_LEN + 1];
};
const int EEPROM_SIZE = sizeof(WifiCredential) * MAX_WIFI_CREDENTIALS;

// --- MQTT Credentials ---
const char* mqtt_server = "*******";
const int mqtt_port = ****;
const char* mqtt_user = "*********";
const char* mqtt_pass = "*********";
const char* mqtt_topic = "********";

// --- SD Card & Sensor Pins ---
const int chipSelect = D4; // GPIO2
#define LOADCELL_DOUT_PIN    D1 // GPIO5
#define LOADCELL_SCK_PIN     D2 // GPIO4
#define STRAINGAUGE_DOUT_PIN D3 // GPIO0
#define STRAINGAUGE_SCK_PIN  D0 // GPIO16

// --- Global Library Instances ---
// These are declared here so other .cpp files can access them
extern WiFiClientSecure espClient;
extern PubSubClient client;
extern HX711 loadCell;
extern HX711 strainGauge;

#endif // CONFIG_H
