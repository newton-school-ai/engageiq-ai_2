"""Yawn detection using Mouth Aspect Ratio (MAR)."""


def compute_mar(mouth_landmarks: list[tuple[float, float]]) -> float:
    """Compute Mouth Aspect Ratio from lip landmarks.

    Args:
        mouth_landmarks: List of lip landmark (x, y) tuples.

    Returns:
        MAR value. Above 0.6 indicates open mouth (potential yawn).
    """
    # TODO: Implement MAR computation
    raise NotImplementedError


class YawnDetector:
    """Detects yawns from sustained mouth opening and tracks frequency."""

    def __init__(self, mar_threshold: float = 0.6, yawn_duration: float = 1.5):
        self.mar_threshold = mar_threshold
        self.yawn_duration = yawn_duration
        self.yawn_count = 0
        self._yawn_timestamps = []

    def update(self, mar: float, timestamp: float) -> bool:
        """Update detector with new MAR reading.

        Returns:
            True if a yawn is detected.
        """
        # TODO: Implement
        raise NotImplementedError

    def is_fatigued(self, window_seconds: float = 300.0) -> bool:
        """Check if 3+ yawns occurred in the given time window."""
        # TODO: Implement
        raise NotImplementedError
