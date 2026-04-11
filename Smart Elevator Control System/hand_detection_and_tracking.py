import cv2
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def run_hand_detection():
    pTime = 0
    confirmation = []
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)

            # FPS
            cTime = time.time()
            if pTime == 0:
                pTime = cTime
            fps = int(1 / (cTime - pTime + 0.0001))
            pTime = cTime

            cv2.putText(image, f"{fps} FPS", (10, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            image.flags.writeable = True

            fingerCount = 0

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                    handLabel = results.multi_handedness[idx].classification[0].label

                    handLandmarks = []
                    for lm in hand_landmarks.landmark:
                        handLandmarks.append([lm.x, lm.y])

                    # Thumb
                    if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                        fingerCount += 1
                    elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                        fingerCount += 1

                    # Fingers
                    if handLandmarks[8][1] < handLandmarks[6][1]:
                        fingerCount += 1
                    if handLandmarks[12][1] < handLandmarks[10][1]:
                        fingerCount += 1
                    if handLandmarks[16][1] < handLandmarks[14][1]:
                        fingerCount += 1
                    if handLandmarks[20][1] < handLandmarks[18][1]:
                        fingerCount += 1

                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

            confirmation.append(fingerCount)

            if len(confirmation) == 5:
                if confirmation.count(confirmation[0]) == 5:
                    print(f"I GOT IT → {confirmation[0]}")
                    fingerCount = confirmation[0]

                confirmation = []

            cv2.putText(image, str(fingerCount),
                        (image.shape[1] // 2 - 40, 60),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 3)

            cv2.imshow("Hand Detection", image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()