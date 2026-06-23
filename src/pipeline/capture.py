import threading
import time
from datetime import datetime

import cv2


class WebcamCapture:
    def __init__(self, src=0, fps=15, resolution=(640, 480)):
        self.src = src
        self.target_fps = fps
        self.resolution = resolution
        self.stream = cv2.VideoCapture(src)
        self.frame_id = 0

        # Configure hardware
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        # Graceful error handling: Raise if camera not found
        if not self.stream.isOpened():
            raise ConnectionError(
                f"CRITICAL: Could not open video source: {src}. "
                "Check if camera is connected or file path is valid."
            )

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
        """Internal loop to capture frames with error recovery."""
        interval = 1.0 / self.target_fps
        while self.running:
            try:
                start_time = time.time()
                grabbed, frame = self.stream.read()

                if not grabbed:
                    print("Warning: Failed to grab frame. Retrying...")
                    time.sleep(1)
                    continue

                with self.lock:
                    self.frame = frame
                    self.timestamp = datetime.now()
                    self.frame_id += 1

                # Maintain FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                time.sleep(sleep_time)

            except Exception as e:
                print(f"Error in capture loop: {e}")
                self.running = False
                if self.stream:
                    self.stream.release()

    def read(self):
        """Safely returns the latest frame and timestamp."""
        with self.lock:
            return self.frame, self.timestamp, self.frame_id

    def stop(self):
        """Stops the capture thread and releases hardware."""
        self.running = False
        if self.stream is not None:
            self.stream.release()
            self.stream = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    # In your capture.py
    def get_health(self):
        if not self.running:
            return "STOPPED"
        if self.frame is None:
            return "WAITING_FOR_DATA"
        return "HEALTHY"
