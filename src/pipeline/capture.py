import logging
import threading
import time
from datetime import datetime

import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebcamCapture:
    def __init__(self, src=0, fps=15, resolution=(640, 480)):
        self.src = src
        self.target_fps = fps
        self.resolution = resolution

        self.stream = cv2.VideoCapture(src)

        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        if not self.stream.isOpened():
            raise ConnectionError(
                f"CRITICAL: Could not open video source: {src}. "
                "Check if camera is connected or file path is valid."
            )

        self.frame = None
        self.timestamp = None
        self.frame_id = 0

        self.running = False
        self.thread = None

        self.lock = threading.Lock()

        self.frame_count = 0
        self.start_time = None
        self.failed_reads = 0

    def start(self):
        """Starts the capture thread."""
        if self.running:
            return

        self.running = True
        self.start_time = time.perf_counter()

        self.thread = threading.Thread(
            target=self._capture_loop,
            daemon=True,
        )

        self.thread.start()

    def _capture_loop(self):
        """Captures frames continuously."""
        interval = 1.0 / self.target_fps

        while self.running:
            try:
                start_time = time.perf_counter()

                grabbed, frame = self.stream.read()

                if not grabbed:
                    self.failed_reads += 1

                    logger.warning(
                        "Failed frame grab (%s failures)",
                        self.failed_reads,
                    )

                    if self.failed_reads >= 10:
                        logger.warning("Attempting camera reconnection...")

                        self.stream.release()

                        self.stream = cv2.VideoCapture(self.src)

                        self.failed_reads = 0

                    time.sleep(1)
                    continue

                with self.lock:
                    self.frame = frame
                    self.timestamp = datetime.now()
                    self.frame_id += 1
                    self.frame_count += 1
                    self.failed_reads = 0

                elapsed = time.perf_counter() - start_time
                sleep_time = max(0, interval - elapsed)

                time.sleep(sleep_time)

            except Exception as e:
                logger.exception(
                    "Unexpected error in capture loop: %s",
                    e,
                )
                self.running = False

    def read(self):
        """Returns latest frame safely."""
        with self.lock:
            if self.frame is None:
                return None, None, None

            return (
                self.frame.copy(),
                self.timestamp,
                self.frame_id,
            )

    def stop(self):
        """Stops the capture thread and releases hardware."""
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=2)

        if self.stream is not None:
            self.stream.release()
            self.stream = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_health(self):
        if not self.running:
            return "STOPPED"

        if self.frame is None:
            return "WAITING_FOR_DATA"

        return "HEALTHY"

    def get_fps(self):
        if self.start_time is None:
            return 0.0

        elapsed = time.perf_counter() - self.start_time

        if elapsed <= 0:
            return 0.0

        return self.frame_count / elapsed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--duration", type=int, default=5)

    args = parser.parse_args()

    cap = WebcamCapture(fps=args.fps)

    cap.start()

    time.sleep(args.duration)

    logger.info(
        "Actual FPS: %.2f",
        cap.get_fps(),
    )

    cap.stop()
