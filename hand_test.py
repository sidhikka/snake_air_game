import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = None, None
direction = "NONE"

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            # Index finger tip = landmark 8
            finger = hand.landmark[8]
            x = int(finger.x * w)
            y = int(finger.y * h)

            # Draw finger point
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            if prev_x is not None:
                dx = x - prev_x
                dy = y - prev_y

                if abs(dx) > abs(dy):
                    if dx > 15:
                        direction = "RIGHT"
                    elif dx < -15:
                        direction = "LEFT"
                else:
                    if dy > 15:
                        direction = "DOWN"
                    elif dy < -15:
                        direction = "UP"

            prev_x, prev_y = x, y

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # Show direction text
    cv2.putText(
        frame,
        f"Direction: {direction}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("Air Gesture Direction", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
