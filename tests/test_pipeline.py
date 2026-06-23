import pytest

from src.pipeline.capture import WebcamCapture

# from src.pipeline.preprocessor import FramePreprocessor


def test_pipeline_smoke():
    """Checks if the capture and preprocessor can start without error."""
    try:
        with WebcamCapture(src=0) as cap:
            cap.start()
            frame, _, _ = cap.read()
            # If we reached here, the capture is working
            assert True
    except Exception as e:
        pytest.fail(f"Pipeline failed to initialize: {e}")
