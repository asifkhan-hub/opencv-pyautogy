import cv2
import dlib
from scipy.spatial import distance
import time
import pygame  # Import the pygame library

# Initialize the face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera (webcam)

# Initialize variables for eye blink counting
blink_count = 0
blink_flag = False

# Initialize variables for time-based blink counting
start_time = time.time()
blink_interval = 10  # Set the time interval (in seconds)
blink_threshold = 10  # Set the blink threshold

# Initialize pygame
pygame.mixer.init()
alert_sound = pygame.mixer.Sound("alert_sound.wav")  # Replace with the path to your alert sound file

while True:
    # Capture video from your webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = detector(gray)

    for face in faces:
        # Detect landmarks in the detected face region
        landmarks = predictor(gray, face)

        # Extract the coordinates of the left and right eye
        left_eye = []
        right_eye = []

        for i in range(36, 42):  # Landmarks for left eye (0-5)
            x, y = landmarks.part(i).x, landmarks.part(i).y
            left_eye.append((x, y))

        for i in range(42, 48):  # Landmarks for right eye (6-11)
            x, y = landmarks.part(i).x, landmarks.part(i).y
            right_eye.append((x, y))

        # Calculate eye aspect ratio (EAR) for left and right eyes
        def eye_aspect_ratio(eye):
            A = distance.euclidean(eye[1], eye[5])
            B = distance.euclidean(eye[2], eye[4])
            C = distance.euclidean(eye[0], eye[3])
            ear = (A + B) / (2.0 * C)
            return ear

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Calculate the average EAR for both eyes
        ear = (left_ear + right_ear) / 2.0

        # Check for an eye blink
        if ear < 0.2:  # You can adjust this threshold as needed
            if not blink_flag:
                blink_count += 1
                blink_flag = True

                # Check if the blink count exceeds the threshold
                if blink_count >= blink_threshold:
                    elapsed_time = time.time() - start_time
                    if elapsed_time <= blink_interval:
                        print("Alert: Blink count exceeded the threshold!")
                        # Play the alert sound
                        alert_sound.play()
                        blink_count = 0  # Reset the blink count

        else:
            blink_flag = False

        # Display the eye blink count on the frame
        cv2.putText(frame, f"Blinks: {blink_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the video frame
    cv2.imshow("Eye Blink Counter", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
