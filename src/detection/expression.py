"""Facial expression classifier (engaged, confused, bored, neutral)."""

from enum import Enum


class Expression(str, Enum):
    ENGAGED = "engaged"
    CONFUSED = "confused"
    BORED = "bored"
    NEUTRAL = "neutral"


class ExpressionClassifier:
    """Classifies facial expressions from cropped face images."""

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path
        self._model = None

    def predict(self, face_crop) -> tuple[Expression, float]:
        """Predict expression from cropped face image.

        Args:
            face_crop: Cropped face as numpy array (224x224x3).

        Returns:
            Tuple of (Expression, confidence).
        """
        # TODO: Implement using FER library or custom model
        raise NotImplementedError
