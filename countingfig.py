import cv2
import math
from cvzone.HandTrackingModule import HandDetector

# Initialize HandDetector
detector = HandDetector(maxHands=1, detectionCon=0.7)

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera (webcam)

while True:
    # Capture video from your webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Detect hands in the frame
    hands, _ = detector.findHands(frame)

    if hands:
        # Get landmarks of the detected hand
        hand = hands[0]  # Assuming only one hand is detected
        landmarks = hand["lmList"]

        # Count fingers
        finger_count = 0

        # Thumb (Landmark 4) check
        if landmarks[4][1] < landmarks[3][1]:
            finger_count += 1

        # Four fingers (Landmarks 8, 12, 16, 20) check
        for landmark_id in [8, 12, 16, 20]:
            if landmarks[landmark_id][2] < landmarks[landmark_id - 2][2]:
                finger_count += 1

        # Display the finger count
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the video frame (you can skip this part if not needed)
    cv2.imshow("Finger Counting", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
