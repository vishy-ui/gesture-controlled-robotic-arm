import cv2
import mediapipe as mp
import serial
import time

# ---- Serial Setup ----
esp = serial.Serial('COM3', 9600)
time.sleep(3)
esp.flush()

# ---- MediaPipe Setup ----
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

prev_angle = -1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    angle = 90  # default reset if no hand

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        # Draw all 21 landmarks
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # ---- Index fingertip ----
        index_tip = hand.landmark[8]

        cx = int(index_tip.x * w)
        cy = int(index_tip.y * h)

        # Draw index tip
        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)

        # Map X to servo angle
        angle = int(index_tip.x * 180)
        angle = max(0, min(180, angle))

    # Send only if angle changed
    if angle != prev_angle:
        esp.write(f"{angle}\n".encode())
        prev_angle = angle

    # Display angle
    cv2.putText(frame,
                f"Servo Angle: {angle}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("Index Finger Servo Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
esp.close()
cv2.destroyAllWindows()
