import cv2
import math
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera (webcam)

# Initialize drawing variables
drawing = False
draw_color = (0, 255, 0)
prev_x, prev_y = 0, 0

while True:
    # Capture video from your webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get hand landmarks as a list
            landmarks = []
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                landmarks.append((x, y))

            # Count fingers
            finger_count = 0

            # Thumb (Landmark 4) check
            if landmarks[4][1] < landmarks[3][1]:
                finger_count += 1

            # Four fingers (Landmarks 8, 12, 16, 20) check
            for landmark_id in [8, 12, 16, 20]:
                if landmarks[landmark_id][1] < landmarks[landmark_id - 2][1]:
                    finger_count += 1

            # Display the finger count
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Check for specific hand gestures
            if finger_count == 5:
                cv2.putText(frame, "Open Hand", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif finger_count == 0:
                cv2.putText(frame, "Closed Fist", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Enable drawing mode when thumb and index finger are close
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            distance = math.sqrt((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2)
            if distance < 30:
                drawing = True
            else:
                drawing = False

            # Drawing on the screen
            if drawing:
                cv2.line(frame, (prev_x, prev_y), (landmarks[8][0], landmarks[8][1]), draw_color, 10)
            prev_x, prev_y = landmarks[8]

    # Display the video frame (you can skip this part if not needed)
    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
