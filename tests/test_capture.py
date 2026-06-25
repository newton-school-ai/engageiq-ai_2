import time
from unittest.mock import MagicMock, patch

import numpy as np

from src.pipeline.capture import WebcamCapture


@patch("cv2.VideoCapture")
def test_capture_initialization(mock_capture):
    mock_camera = MagicMock()
    mock_camera.isOpened.return_value = True

    mock_capture.return_value = mock_camera

    cap = WebcamCapture()

    assert cap.target_fps == 15
    assert cap.resolution == (640, 480)


@patch("cv2.VideoCapture")
def test_fps_tracking(mock_capture):
    mock_camera = MagicMock()

    mock_camera.isOpened.return_value = True

    mock_camera.read.return_value = (
        True,
        np.zeros((480, 640, 3), dtype=np.uint8),
    )

    mock_capture.return_value = mock_camera

    cap = WebcamCapture(fps=15)

    cap.start()

    time.sleep(2)

    fps = cap.get_fps()

    cap.stop()

    assert fps > 10
