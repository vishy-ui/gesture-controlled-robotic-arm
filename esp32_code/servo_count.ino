#include <ESP32Servo.h>

Servo myServo;
int servoPin = 18;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(0);   // default
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    if (c == '1') myServo.write(0);
    if (c == '2') myServo.write(60);
    if (c == '3') myServo.write(120);
    if (c == '4') myServo.write(180);
  }
}