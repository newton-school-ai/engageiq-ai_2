from unittest.mock import MagicMock, patch

from src.pipeline.capture import WebcamCapture

# import pytest


@patch("cv2.VideoCapture")
def test_pipeline_smoke(mock_capture):
    """Checks if the capture pipeline initializes."""

    mock_camera = MagicMock()
    mock_camera.isOpened.return_value = True
    mock_camera.read.return_value = (True, "fake_frame")

    mock_capture.return_value = mock_camera

    with WebcamCapture(src=0) as cap:
        assert cap is not None
