import numpy as np

from src.pipeline.preprocessor import FramePreprocessor


def test_preprocessor_output_shape():
    frame = np.random.randint(
        0,
        255,
        (1080, 1920, 3),
        dtype=np.uint8,
    )

    prep = FramePreprocessor(target_size=(640, 480))

    result = prep.process(frame)

    assert result.shape == (480, 640, 3)
    assert result.dtype == np.float32
