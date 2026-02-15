import cv2
import mediapipe as mp
import math
import serial
import time


ser = serial.Serial('COM3', 9600)  
time.sleep(2)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("Pinch LED Control", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Pinch LED Control", 1280, 720)

PINCH_ON_THRESHOLD = 55
PINCH_OFF_THRESHOLD = 85

led_on = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        x1, y1 = int(thumb.x * w), int(thumb.y * h)
        x2, y2 = int(index.x * w), int(index.y * h)

        cv2.circle(frame, (x1, y1), 10, (255, 0, 0), -1)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 0), -1)

        distance = math.hypot(x2 - x1, y2 - y1)

        #  PINCH  ESP32 
        if not led_on and distance < PINCH_ON_THRESHOLD:
            led_on = True
            ser.write(b'1')   # LED ON
            print("LED ON")

        elif led_on and distance > PINCH_OFF_THRESHOLD:
            led_on = False
            ser.write(b'0')   # LED OFF
            print("LED OFF")

        

    if led_on:
        led_color = (0, 255, 0)
        led_text = "LED ON (Pinch)"
    else:
        led_color = (0, 0, 255)
        led_text = "LED OFF"

    cv2.circle(frame, (100, 100), 30, led_color, -1)
    cv2.putText(frame, led_text, (150, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, led_color, 2)

    cv2.imshow("Pinch LED Control", frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()

'''
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

pins 

led long leg - d18
short leg - resistor - gnd
'''