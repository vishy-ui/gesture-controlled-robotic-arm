import cv2
import mediapipe as mp
import serial
import time
import statistics
from collections import deque

try:
    ser = serial.Serial('COM3', 9600)  
    time.sleep(2)
    print("Successfully connected to ESP32 on COM3")
except serial.SerialException:
    print("ERROR: Could not connect to COM3. Check connection and close Arduino IDE Serial Monitor.")
    exit()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.namedWindow("Finger Preset Servo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Finger Preset Servo", 1280, 720)

finger_history = deque(maxlen=7)

def count_fingers(hand, hand_label):
    fingers = 0
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers += 1

    if hand_label == "Right":
        if hand.landmark[4].x < hand.landmark[3].x:
            fingers += 1
    elif hand_label == "Left":
        if hand.landmark[4].x > hand.landmark[3].x:
            fingers += 1

    return fingers

last_sent = -1 
current_angle = 0


sweep_step = 0 # sweep 0 to 4
sweep_direction = 1
last_sweep_time = 0
SWEEP_INTERVAL = 0.5  

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks and result.multi_handedness:
        hand = result.multi_hand_landmarks[0]
        hand_label = result.multi_handedness[0].classification[0].label
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        raw_count = count_fingers(hand, hand_label)
        
        # 0 as min
        raw_count = min(max(raw_count, 0), 5) 
        finger_history.append(raw_count)

        if len(finger_history) == finger_history.maxlen:
            smoothed_count = statistics.mode(finger_history)

            if smoothed_count == 5:
                current_time = time.time()
                if current_time - last_sweep_time > SWEEP_INTERVAL:
                    ser.write(str(sweep_step).encode())
                    current_angle = sweep_step * 45 
                    print(f"Sweeping... sent: {sweep_step} (Angle: {current_angle})")
                    
                    last_sweep_time = current_time
                    last_sent = 5  

                    sweep_step += sweep_direction
                    if sweep_step == 4:
                        sweep_direction = -1 
                    elif sweep_step == 0:
                        sweep_direction = 1   
                        
            else:
                # 0 to 4 finger
                if smoothed_count != last_sent:
                    ser.write(str(smoothed_count).encode())
                    current_angle = smoothed_count * 45
                    print(f"Sent command: {smoothed_count} (Angle: {current_angle})")
                    last_sent = smoothed_count
                    
                    # reset sweep variables
                    sweep_step = 0
                    sweep_direction = 1

            status_text = "(Sweeping)" if smoothed_count == 5 else ""
            text_color = (0, 165, 255) if smoothed_count == 5 else (0, 255, 0)
            
            cv2.putText(frame, f"Fingers: {smoothed_count} | Angle = {current_angle} deg {status_text}",
                        (30, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, text_color, 3)

    else:
        finger_history.clear()

    cv2.imshow("Finger Preset Servo", frame)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
