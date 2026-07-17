import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2

# Add the src directory to sys.path so we can import modules properly
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from detection.drowsiness import DrowsinessDetector, compute_ear
from detection.face_mesh import FaceMeshDetector
from scoring.state_machine import EngagementStateMachine


def main():
    print("Initializing components...")
    face_detector = FaceMeshDetector()
    drowsiness_detector = DrowsinessDetector()
    # Use low hysteresis durations (e.g. 1 or 2 seconds) so you don't have to wait 30 seconds!
    from scoring.state_machine import EngagementState

    state_machine = EngagementStateMachine(
        hysteresis_seconds={
            EngagementState.PASSIVE: 2.0,
            EngagementState.CONFUSED: 2.0,
            EngagementState.DISTRACTED: 2.0,
            EngagementState.DROWSY: 1.0,
        }
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    print("Camera running. Press 'q' to quit.")
    print("Press 'c' to simulate CONFUSED state.")
    print("Press 'b' to simulate BORED (PASSIVE) state.")
    print("Press 'n' to simulate NEUTRAL (ENGAGED) state.")

    # State flags controlled by keyboard
    force_confused = False
    force_bored = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        # Default signals
        score = 85.0  # default engaged
        is_drowsy = False
        is_confused = force_confused

        face_result = face_detector.detect(frame)
        if face_result and face_result.faces:
            face = face_result.faces[0]

            # 1. Drowsiness (EAR)
            left_eye = [
                (face.landmarks[i][0] * w, face.landmarks[i][1] * h) for i in LEFT_EYE
            ]
            right_eye = [
                (face.landmarks[i][0] * w, face.landmarks[i][1] * h) for i in RIGHT_EYE
            ]
            avg_ear = (compute_ear(left_eye) + compute_ear(right_eye)) / 2.0
            is_drowsy = drowsiness_detector.update(avg_ear, time.time())

            # Mock the score to test the state machine behavior:
            if is_drowsy:
                score = 20.0
            elif force_bored:
                score = 45.0  # PASSIVE range (40 - 70)
            else:
                score = 85.0  # ENGAGED
        else:
            score = 10.0  # No face = DISTRACTED

        # 3. Update State Machine
        current_state = state_machine.update(
            score=score,
            is_drowsy=is_drowsy,
            is_confused=is_confused,
            timestamp=datetime.now(timezone.utc),
        )

        state_str = current_state.value.upper() if current_state else "INITIALIZING"

        # 4. Draw on screen
        color = (0, 255, 0)
        if state_str == "CONFUSED":
            color = (0, 165, 255)  # Orange
        elif state_str == "DROWSY":
            color = (0, 0, 255)  # Red
        elif state_str == "PASSIVE":
            color = (0, 255, 255)  # Yellow
        elif state_str == "DISTRACTED":
            color = (0, 0, 255)  # Red

        cv2.putText(
            frame,
            f"STATE: {state_str}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            color,
            3,
        )
        cv2.putText(
            frame,
            f"Score (mock): {score:.1f}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Confused: {is_confused}",
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            f"Drowsy: {is_drowsy}",
            (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.imshow("State Machine Camera Test", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            force_confused = True
            force_bored = False
        elif key == ord("b"):
            force_bored = True
            force_confused = False
        elif key == ord("n"):
            force_confused = False
            force_bored = False

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
