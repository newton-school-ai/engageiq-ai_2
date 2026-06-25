import time # <--- This was missing!
import cv2
from src.pipeline.capture import WebcamCapture

# Now your script will work
cap = WebcamCapture()
cap.start()
time.sleep(1) 

raw_frame, _ = cap.read()
if raw_frame is not None:
    cv2.imwrite("test_frame.jpg", raw_frame)
    print("Frame successfully stored to test_frame.jpg")

cap.stop()