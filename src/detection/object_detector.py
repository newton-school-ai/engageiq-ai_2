"""YOLOv8 nano object detector for phone, book, and second person detection."""


class ObjectDetector:
    """Detects distracting objects in the webcam frame."""

    def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.5):
        self.model_path = model_path
        self.confidence = confidence
        self._model = None

    def detect(self, frame) -> list[dict]:
        """Detect objects in frame.

        Returns:
            List of dicts with keys: class_name, confidence, bbox.
        """
        # TODO: Implement
        raise NotImplementedError
