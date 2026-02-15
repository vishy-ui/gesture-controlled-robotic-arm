int ledPin = 18;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') digitalWrite(ledPin, HIGH);
    if (c == '0') digitalWrite(ledPin, LOW);
  }
}