"""
Diagnostic: draws the 6 reference landmarks used by head_pose.py directly on
the webcam feed, labeled, so we can visually confirm each one lands on the
correct physical point (nose tip, chin, correct eye corners, correct mouth
corners).

Run from repo root:
    python scripts/debug_landmarks.py

Press 'q' to quit.
"""

import cv2

from src.detection.face_mesh import FaceMeshDetector
from src.detection.head_pose import LANDMARK_INDICES

LABELS = ["NOSE_TIP", "CHIN", "LEFT_EYE", "RIGHT_EYE", "LEFT_MOUTH", "RIGHT_MOUTH"]
COLORS = [
    (0, 255, 255),  # nose tip - yellow
    (255, 0, 255),  # chin - magenta
    (0, 255, 0),  # left eye - green
    (0, 0, 255),  # right eye - red
    (255, 255, 0),  # left mouth - cyan
    (255, 0, 0),  # right mouth - blue
]


def main():
    detector = FaceMeshDetector()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    print("Press 'q' to quit.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            height, width = frame.shape[:2]
            result = detector.detect(frame)

            if result is not None and result.faces:
                landmarks = result.faces[0].landmarks
                for label, idx, color in zip(LABELS, LANDMARK_INDICES, COLORS):
                    x, y, _ = landmarks[idx]
                    px, py = int(x * width), int(y * height)
                    cv2.circle(frame, (px, py), 6, color, -1)
                    cv2.putText(
                        frame,
                        label,
                        (px + 8, py),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )
            else:
                cv2.putText(
                    frame,
                    "No face detected",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow("Landmark Debug", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
