import cv2
import numpy as np

class FramePreprocessor:
    def __init__(self, target_size=(640, 480)):
        self.target_size = target_size

    def process(self, frame):
        if frame is None:
            return None
        
        # RGB Convert (OpenCV default is BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize to standardized resolution
        frame = cv2.resize(frame, self.target_size)
        
        # Normalize (0 to 1)
        return frame.astype(np.float32) / 255.0