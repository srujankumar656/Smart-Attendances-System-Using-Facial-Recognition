import cv2
cam = cv2.VideoCapture(0)  # Initialize the webcam
ret, img = cam.read()
if not ret:
    print("Error: Cannot capture frame from the camera.")
