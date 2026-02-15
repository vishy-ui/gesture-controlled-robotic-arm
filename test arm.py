import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Camera setup (stable POV)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.namedWindow("Hand X-Y Motion", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand X-Y Motion", 1280, 720)

prev_x, prev_y = None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    dx, dy = 0, 0

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        # Draw 21 landmarks (visual only)
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # Wrist landmark (index 0) as reference
        wrist = hand.landmark[0]
        cx = int(wrist.x * w)
        cy = int(wrist.y * h)

        # Draw reference point
        cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)

        # Calculate X-Y movement
        if prev_x is not None:
            dx = cx - prev_x
            dy = cy - prev_y

        prev_x, prev_y = cx, cy

    # Display movement values
    cv2.putText(frame, f"X movement: {dx}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Y movement: {dy}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand X-Y Motion", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
