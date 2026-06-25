import cv2
import numpy as np


class FramePreprocessor:
    def __init__(self, target_size=(640, 480)):
        self.target_size = target_size

    def process(self, frame):
        """Preprocess frame for AI inference."""

        if frame is None:
            return None

        if frame.size == 0:
            return None

        h, w = frame.shape[:2]

        if (w, h) != self.target_size:
            frame = cv2.resize(
                frame,
                self.target_size,
                interpolation=cv2.INTER_AREA,
            )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        frame = frame.astype(
            np.float32,
            copy=False,
        )

        frame *= 1.0 / 255.0

        return frame
