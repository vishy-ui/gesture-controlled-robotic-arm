#include <ESP32Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Servo myServo;

int currentAngle = 90;

void setup() {
  Serial.begin(9600);

  myServo.attach(18);

  // Initialize OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED failed");
    while(true);
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(10, 10);
  display.println("Servo");
  display.display();
}

void loop() {

  if (Serial.available()) {

    int angle = Serial.parseInt();

    if (angle >= 0 && angle <= 180) {

      currentAngle = angle;
      myServo.write(currentAngle);

      // Update OLED
      display.clearDisplay();

      display.setTextSize(2);
      display.setCursor(10, 10);
      display.print("Angle:");

      display.setTextSize(3);
      display.setCursor(10, 35);
      display.print(currentAngle);

      display.display();
    }
  }
}
