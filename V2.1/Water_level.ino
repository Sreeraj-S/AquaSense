
#include <ESPAsyncWebServer.h>
#include <WiFi.h>

/*
   --------------------------------------
              Version : 2.1
   --------------------------------------
*/



#define TRIGGER 4
#define ECHO    5
const char* ssid = "Mystic";  //replace
const char* password =  "p@dmalayam"; //replace
AsyncWebServer server(80);
//int relayPin = 23;
void setup()
{
  pinMode(TRIGGER, OUTPUT);
  pinMode(ECHO, INPUT);
  Serial.begin(19200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println(WiFi.localIP());
  server.on("/test", HTTP_GET, [](AsyncWebServerRequest * request) {
    request->send(200, "text/plain", "Worked!");
  });
  /*server.on("/relay/off", HTTP_GET   , [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", "ok");
    });
    server.on("/relay/on", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain","ok");
    });
    server.on("/relay/toggle", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain","ok");
    digitalWrite(relayPin, !digitalRead(relayPin));
    });
    server.on("/relay", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", String(digitalRead(relayPin)));
    });*/
  server.begin();
}
void loop() {
  int duration, distance;
  String dis = "";
  
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIGGER, LOW);
  duration = pulseIn(ECHO, HIGH);
  distance = (duration / 2) / 29.1;
  server.on("/level", HTTP_GET, [distance](AsyncWebServerRequest * request) {
    request->send(200, "text/plain", String(distance));
  });
  delay(200);

}
