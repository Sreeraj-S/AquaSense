



/*
********************************************
  ULTRASONIC DISTANCE SENSOR CODE 
      Version : 1.73
********************************************
*/
#define TRIGGER 4
#define ECHO    5

// NodeMCU Pin D1 > TRIGGER | Pin D2 > ECHO

#define BLYNK_PRINT Serial    // Comment this out to disable prints and save space
//#include <Esp32WiFiManager.h>

#include <WiFi.h>
#include <WiFiClient.h>

#include <BlynkSimpleEsp32.h>

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "***********************";

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "***********************";
char pass[] = "***********************";
void setup() {

  Serial.begin (9600);
  Blynk.begin(auth, ssid, pass);
  pinMode(TRIGGER, OUTPUT);
  pinMode(ECHO, INPUT);
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
    delay(200);
    Blynk.run();
  }
  catch (...)
  {
    while (true)
    {
      if (Blynk.connected())
      {
        break;
      }
      else
      {
        try {
          Blynk.begin(auth, ssid, pass);
        }
        catch (...) {

        }

      }
    }
  }


}
