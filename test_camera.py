import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access webcam")
else:
    print("Webcam is working!")
cap.release()
