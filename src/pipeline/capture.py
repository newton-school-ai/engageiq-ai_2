import cv2
import threading
import time
from datetime import datetime

class WebcamCapture:
    def __init__(self, src=0, fps=15, resolution=(640, 480)):
        self.src = src
        self.target_fps = fps
        self.resolution = resolution
        self.stream = cv2.VideoCapture(src)
        
        # Configure hardware
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        
        self.frame = None
        self.timestamp = None
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        """Starts the capture thread."""
        self.running = True
        thread = threading.Thread(target=self._capture_loop, daemon=True)
        thread.start()

    def _capture_loop(self):
        """Internal loop to capture frames."""
        interval = 1.0 / self.target_fps
        while self.running:
            start_time = time.time()
            grabbed, frame = self.stream.read()
            if grabbed:
                with self.lock:
                    self.frame = frame
                    self.timestamp = datetime.now()
            
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)

    def read(self):
        """Safely returns the latest frame and timestamp."""
        with self.lock:
            return self.frame, self.timestamp

    def stop(self):
        """Stops the capture thread and releases hardware."""
        self.running = False
        self.stream.release()