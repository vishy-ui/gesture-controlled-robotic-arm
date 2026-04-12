#include <ESP32Servo.h>

Servo myServo;
int servoPin = 18;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(0);   // Default to 0 degrees (Closed Fist)
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    // Mapping 5 states to 180 degrees (45 degrees per finger)
    if (c == '0') myServo.write(0);
    if (c == '1') myServo.write(45);
    if (c == '2') myServo.write(90);
    if (c == '3') myServo.write(135);
    if (c == '4') myServo.write(180);
  }
}
