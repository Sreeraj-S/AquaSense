



/*
********************************************
  ULTRASONIC DISTANCE SENSOR CODE

  Version : 1.01
  
********************************************
*/
#define TRIGGER 4
#define ECHO    5

// NodeMCU Pin D1 > TRIGGER | Pin D2 > ECHO

#define BLYNK_PRINT Serial    // Comment this out to disable prints and save space
//#include <Esp32WiFiManager.h>

#include <WiFi.h>
#include <BlynkSimpleEsp32.h>

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "***********************";

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = ***********************";
char pass[] = "***********************";
void setup() {

  Serial.begin (9600);
  WiFi.begin(ssid, pass);
  Serial.print("Connecting to ");
  Serial.print(ssid);

  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(500);
    Serial.print('.');
    Serial.println('\n');
  }
  Serial.println("Connection established!");
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer

  Blynk.config(auth);
  pinMode(TRIGGER, OUTPUT);
  pinMode(ECHO, INPUT);
  delay (1000);
  //pinMode(BUILTIN_LED, OUTPUT);
}


void loop() {
  try
  {
    long duration, distance, wdis;
    digitalWrite(TRIGGER, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIGGER, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIGGER, LOW);
    duration = pulseIn(ECHO, HIGH);
    distance = (duration / 2) / 29.1;


    if (distance <= 81) {
      Blynk.virtualWrite(V0, 255);
    }
    else {
      Blynk.virtualWrite(V0, 0);
    }

    if (distance <= 67) {
      Blynk.virtualWrite(V1, 255);
    }
    else {
      Blynk.virtualWrite(V1, 0);
    }

    if (distance <= 45) {
      Blynk.virtualWrite(V2, 255);
    }
    else {
      Blynk.virtualWrite(V2, 0);
    }

    if (distance <= 22) {
      Blynk.virtualWrite(V3, 255);
    }
    else {
      Blynk.virtualWrite(V3, 0);
    }

    if (distance <= 9) {
      Blynk.virtualWrite(V4, 255);
    }
    else {
      Blynk.virtualWrite(V4, 0);
    }
    if (distance <= 5) {
      Blynk.virtualWrite(V7, 255);
    }
    else {
      Blynk.virtualWrite(V7, 0);
    }
    if (distance <= 86) {
      Blynk.virtualWrite(V8, 255);
    }
    else {
      Blynk.virtualWrite(V8, 0);
    }

    Serial.print(distance);
    Serial.println("Centimeter:");
    Blynk.virtualWrite(V5, distance);
    wdis = 90 - distance;
    Blynk.virtualWrite(V6, wdis);
    delay(2000);
    Blynk.run();
  }
  catch (...){
    Serial.println("Restarting in 10 seconds");
  delay(10000);
  ESP.restart();

  }
}
