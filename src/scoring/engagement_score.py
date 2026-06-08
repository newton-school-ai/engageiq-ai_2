"""Multi-signal engagement scorer."""

from src.config.settings import settings


def compute_engagement_score(
    gaze_score: float,
    pose_score: float,
    expression_score: float,
    alertness_score: float,
) -> float:
    """Compute weighted engagement score from multiple CV signals.

    Args:
        gaze_score: 0-100 score from gaze classifier.
        pose_score: 0-100 score from head pose.
        expression_score: 0-100 score from expression classifier.
        alertness_score: 0-100 score from drowsiness/yawn detectors.

    Returns:
        Engagement score 0-100.
    """
    return (
        gaze_score * settings.gaze_weight
        + pose_score * settings.pose_weight
        + expression_score * settings.expression_weight
        + alertness_score * settings.alertness_weight
    )
