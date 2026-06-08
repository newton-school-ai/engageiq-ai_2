"""Temporal smoothing and anomaly filtering for engagement scores."""

from collections import deque


class TemporalFilter:
    """Smooths engagement scores over a sliding window."""

    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self._buffer = deque(maxlen=window_size)

    def smooth(self, score: float) -> float:
        """Add score to buffer and return smoothed value.

        Returns:
            Moving average of scores in the window.
        """
        self._buffer.append(score)
        return sum(self._buffer) / len(self._buffer)
