"""Gaze direction classifier based on head pose and eye landmarks."""

from enum import Enum


class GazeState(str, Enum):
    AT_SCREEN = "at_screen"
    AWAY_LEFT = "away_left"
    AWAY_RIGHT = "away_right"
    LOOKING_DOWN = "looking_down"
    EYES_CLOSED = "eyes_closed"


def classify_gaze(pitch: float, yaw: float, ear: float) -> tuple[GazeState, float]:
    """Classify gaze direction from head pose and eye state.

    Args:
        pitch: Head pitch in degrees (negative = looking down).
        yaw: Head yaw in degrees (positive = looking right).
        ear: Eye Aspect Ratio (below threshold = eyes closed).

    Returns:
        Tuple of (GazeState, confidence).
    """
    # TODO: Implement classification logic
    raise NotImplementedError
