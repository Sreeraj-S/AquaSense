/*
 * ***********************************
 *           Version:3.01
 *           MQTT Client
 * ***********************************
 */







#include <PubSubClient.h>
#include <WiFi.h>

/* ---- INFO ----*/

/* WIFI Settings */
// Name of wifi network
const char* ssid = "ssid";

// Password to wifi network
const char* password = "pwd";

/* Web Updater Settings */
// Host Name of Device
const char* host = "M-WaterReader1";

// Path to access firmware update page (Not Neccessary to change)
const char* update_path = "/firmware";

/* MQTT Settings */
// Topic which listens for commands
char* outTopic = "M-SmartHouse/utilities/M-WaterReader1/status";

//MQTT Server IP Address
const char* server = "192.168.1.2";

//MQTT Server Port
int port = 1883;

//Unique device ID
const char* mqttDeviceID = "M-SmartHouseWR1";

//Defineing
#define TRIGGER 4
#define ECHO    5
int duration, distance;
char dis[100];
/* ---- PROGRAM ----*/

//Connecting to the WiFi
void connectToWiFi() {
  Serial.print("Connectiog to ");

  WiFi.begin(ssid, password);
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.print("Connected.");

}

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void setupMQTT() {
  mqttClient.setServer(server, port);
  // set the callback function
  mqttClient.setCallback(callback);
}

void setup() {
  Serial.begin(9600);
  connectToWiFi();
  setupMQTT();
  pinMode(TRIGGER, OUTPUT);
  pinMode(ECHO, INPUT);
}

void reconnect() {
  Serial.println("Connecting to MQTT Broker...");
  while (!mqttClient.connected()) {
    Serial.println("Reconnecting to MQTT Broker..");
    String clientId = "M-SmartHouseWR1";

    if (mqttClient.connect(mqttDeviceID)){
      Serial.println("Connected.");
      mqttClient.subscribe(outTopic);
    }

  }
}

void loop(){
  if (!mqttClient.connected()) {
    reconnect();
  }
  mqttClient.loop();

  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIGGER, LOW);
  duration = pulseIn(ECHO, HIGH);
  distance = (duration / 2) / 29.1;
  sprintf(dis, "%u", distance);
  Serial.println(dis);
  mqttClient.publish("M-SmartHouse/utilities/M-WaterReader1/state", dis);
  delay(200);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Callback - ");
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
}
