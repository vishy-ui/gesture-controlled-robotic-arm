import cv2
import mediapipe as mp
import serial
import time

# serial setup
ser = serial.Serial('COM3', 9600)   # comm
time.sleep(2)

# mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# camera setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
cv2.namedWindow("finger preset servo", cv2.WINDOW_NORMAL)

# finger count 
def count_fingers(hand):
    fingers = 0

    # index, middle, ring, pinky
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers += 1

    # thumb
    if hand.landmark[4].x > hand.landmark[3].x:
        fingers += 1

    return fingers

last_sent = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        finger_count = count_fingers(hand)
        finger_count = min(max(finger_count, 1), 4)

        if finger_count != last_sent:
            ser.write(str(finger_count).encode())
            last_sent = finger_count

        cv2.putText(frame, f"Fingers: {finger_count}",
                    (30, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3)

    cv2.imshow("Finger Preset Servo", frame)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()

'''#include <ESP32Servo.h>

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


pins 
brown - GND
red - 3.3V
orange - D18
'''