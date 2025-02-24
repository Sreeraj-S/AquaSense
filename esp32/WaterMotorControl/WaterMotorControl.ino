
#include <Arduino.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <PubSubClient.h>
#include "LittleFS.h"
#include <ArduinoJson.h>

AsyncWebServer server(80);

const char* PARAM_INPUT_1 = "ssid";
const char* PARAM_INPUT_2 = "pass";
const char* PARAM_INPUT_3 = "ip";
const char* PARAM_INPUT_4 = "gateway";
const char* PARAM_INPUT_5 = "staticIp";
const char* PARAM_INPUT_6 = "mqttServer";
const char* PARAM_INPUT_7 = "mqttPort";
const char* PARAM_INPUT_8 = "mqttUsername";
const char* PARAM_INPUT_9 = "mqttPassword";
const char* PARAM_INPUT_10 = "mqttTopic";

const char* mqtt_server = "mqtt.example.com";
const int mqtt_port = 1883;
const char* mqtt_username = "YourMQTTUsername";
const char* mqtt_password = "YourMQTTPassword";

DynamicJsonDocument doc(1024);
String ssid;
String pass;
String ip;
String gateway;
String staticIp;
String mqttServer;
uint16_t mqttPort;
String mqttUsername;
String mqttPassword;
String mqttTopic;

const char* ssidPath = "/ssid.txt";
const char* passPath = "/pass.txt";
const char* ipPath = "/ip.txt";
const char* gatewayPath = "/gateway.txt";
const char* staticIpPath = "/staticip.txt";
const char* mqttServerPath = "/mqttserver.txt";
const char* mqttPortPath = "/mqttport.txt";
const char* mqttUsernamePath = "/mqttusername.txt";
const char* mqttPasswordPath = "/mqttpassword.txt";
const char* mqttTopicPath = "/mqtttopic.txt";

bool ap = true;


IPAddress localIP;

IPAddress localGateway;

IPAddress subnet(255, 255, 0, 0);

#define RELAY 4


String state;
  
unsigned long previousMillis = 0;
const long interval = 10000;

WiFiClient espClient;
PubSubClient client(espClient);


void initLittleFS() {
  if (!LittleFS.begin(true)) {
    Serial.println("An error has occurred while mounting LittleFS");
  }
  Serial.println("LittleFS mounted successfully");
}

String readFile(fs::FS& fs, const char* path) {
  Serial.printf("Reading file: %s\r\n", path);

  File file = fs.open(path);
  if (!file || file.isDirectory()) {
    Serial.println("- failed to open file for reading");
    return String();
  }

  String fileContent;
  while (file.available()) {
    fileContent = file.readStringUntil('\n');
    break;
  }
  return fileContent;
}


void writeFile(fs::FS& fs, const char* path, const char* message) {
  Serial.printf("Writing file: %s\r\n", path);

  File file = fs.open(path, FILE_WRITE);
  if (!file) {
    Serial.println("- failed to open file for writing");
    return;
  }
  if (file.print(message)) {
    Serial.println("- file written");
  } else {
    Serial.println("- write failed");
  }
}


bool initWiFi() {
  if (ssid == "") {
    Serial.println("Undefined SSID or IP address.");
    return false;
  }

  WiFi.mode(WIFI_STA);


  if (staticIp == "on") {
    localIP.fromString(ip.c_str());
    localGateway.fromString(gateway.c_str());

    if (!WiFi.config(localIP, localGateway, subnet)) {
      Serial.println("STA Failed to configure");
      return false;
    }
  }
  WiFi.begin(ssid.c_str(), pass.c_str());
  Serial.println("Connecting to WiFi...");

  unsigned long currentMillis = millis();
  previousMillis = currentMillis;

  while (WiFi.status() != WL_CONNECTED) {
    currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      Serial.println("Failed to connect.");
      return false;
    }
  }
  ap = false;
  Serial.println(WiFi.localIP());
  return true;
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client", mqttUsername.c_str(), mqttPassword.c_str())) {
      Serial.println("connected");
      client.subscribe(String(mqttTopic + "state").c_str());
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void stateChange(String state) {
  if (state == "on") {
    digitalWrite(RELAY, HIGH); // Turn relay ON
    println("on")
  } else if (state == "off") {
    digitalWrite(RELAY, LOW);  // Turn relay OFF
    println("on")

  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);
if (strcmp(topic, (mqttTopic + "state").c_str()) != 0) {
    // If the topic doesn't match, exit the function
    return;
  }
  Serial.print("Payload: ");
  state="";
  for (int i = 0; i < length; i++) {
    
    state = state + (char)payload[i];
  }
stateChange(state)
}

void setup() {
  Serial.begin(115200);

  initLittleFS();


  pinMode(RELAY, OUTPUT);
  digitalWrite(RELAY, LOW);


  ssid = readFile(LittleFS, ssidPath);
  pass = readFile(LittleFS, passPath);
  ip = readFile(LittleFS, ipPath);
  gateway = readFile(LittleFS, gatewayPath);
  staticIp = readFile(LittleFS, staticIpPath);
  mqttServer = readFile(LittleFS, mqttServerPath);
  mqttPort = readFile(LittleFS, mqttPortPath).toInt();
  mqttUsername = readFile(LittleFS, mqttUsernamePath);
  mqttPassword = readFile(LittleFS, mqttPasswordPath);
  mqttTopic = readFile(LittleFS, mqttTopicPath);
  Serial.println(ssid);
  Serial.println(pass);
  Serial.println(ip);
  Serial.println(gateway);
  Serial.println(staticIp);
  Serial.println(mqttServer);
  Serial.println(mqttPort);
  Serial.println(mqttUsername);
  Serial.println(mqttPassword);
  Serial.println(mqttTopic);
  if (initWiFi()) {

    client.setServer(mqttServer.c_str(), mqttPort);
    client.setCallback(callback);
    client.subscribe(String(mqttTopic + "state").c_str());
    webServerViewer();
  } else {
    Serial.println("Setting AP (Access Point)");
    WiFi.softAP("Water-Level-WIFI-MANAGER", NULL);

    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);
    webServerConfig();
  }
}

void webServerConfig() {
  server.on("/", HTTP_GET, [](AsyncWebServerRequest * request) {
    request->send(LittleFS, "/wifimanager.html", "text/html");
  });

  server.serveStatic("/", LittleFS, "/");

  server.on("/", HTTP_POST, [](AsyncWebServerRequest * request) {
    int params = request->params();
    Serial.println(params);
    for (int i = 0; i < params; i++) {
      const AsyncWebParameter* p = request->getParam(i);
      if (p->isPost()) {
        Serial.println(p->name());
        Serial.println(p->value());
        if (p->name() == PARAM_INPUT_1) {
          ssid = p->value().c_str();
          Serial.print("SSID set to: ");
          Serial.println(ssid);
          writeFile(LittleFS, ssidPath, ssid.c_str());
        }
        if (p->name() == PARAM_INPUT_2) {
          pass = p->value().c_str();
          Serial.print("Password set to: ");
          Serial.println(pass);
          writeFile(LittleFS, passPath, pass.c_str());
        }
        // HTTP POST ip value
        if (p->name() == PARAM_INPUT_3) {
          ip = p->value().c_str();
          Serial.print("IP Address set to: ");
          Serial.println(ip);
          writeFile(LittleFS, ipPath, ip.c_str());
        }
        if (p->name() == PARAM_INPUT_4) {
          gateway = p->value().c_str();
          Serial.print("Gateway set to: ");
          Serial.println(gateway);
          writeFile(LittleFS, gatewayPath, gateway.c_str());
        }
        if (p->name() == PARAM_INPUT_5) {
          staticIp = p->value().c_str();
          Serial.print("Static Ip: ");
          Serial.println(staticIp);
          writeFile(LittleFS, staticIpPath, staticIp.c_str());
        }
        if (p->name() == PARAM_INPUT_6) {
          mqttServer = p->value().c_str();
          Serial.print("MQTT Server: ");
          Serial.println(mqttServer);
          writeFile(LittleFS, mqttServerPath, mqttServer.c_str());
        }
        if (p->name() == PARAM_INPUT_7) {
          mqttPort = p->value().toInt();
          Serial.print("MQTT Port: ");
          Serial.println(mqttPort);
          String mqttPortString = String(mqttPort);
          writeFile(LittleFS, mqttPortPath, mqttPortString.c_str());

        }
        if (p->name() == PARAM_INPUT_8) {
          mqttUsername = p->value().c_str();
          Serial.print("MQTT Username: ");
          Serial.println(mqttUsername);
          writeFile(LittleFS, mqttUsernamePath, mqttUsername.c_str());
        }
        if (p->name() == PARAM_INPUT_9) {
          mqttPassword = p->value().c_str();
          Serial.print("MQTT Password: ");
          Serial.println(mqttPassword);
          writeFile(LittleFS, mqttPasswordPath, mqttPassword.c_str());
        }
        if (p->name() == PARAM_INPUT_10) {
          mqttTopic = p->value().c_str();
          Serial.print("MQTT Topic: ");
          Serial.println(mqttTopic);
          writeFile(LittleFS, mqttTopicPath, mqttTopic.c_str());
        }
      }
    }
    request->send(200, "text/plain", "Done. ESP will restart, connect to your router and go to IP address: " + ip);
    delay(3000);
    ESP.restart();
  });
  server.begin();
}

void webServerViewer() {
  server.on("/level", HTTP_GET, [](AsyncWebServerRequest * request) {
    request->send(LittleFS, "/index.html", "text/html");
  });
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest * request) {
    String jsonData;
    serializeJson(doc, jsonData);
    request->send(200, "application/json", jsonData);
  });
  server.serveStatic("/", LittleFS, "/");
  server.begin();
}

void loop() {
  if (!ap) {
    if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
}}
