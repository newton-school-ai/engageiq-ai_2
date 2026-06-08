# Issues Tracker

All 26 issues with: Why, What, Files to create, How to test, Acceptance Criteria, Dependencies.

---

## M1: Project Scaffold and Webcam Pipeline

### Issue #1: Initialize repo scaffold, CI config, Docker setup

**Why:** Every contributor needs a clean, importable project structure from day one. Without it, people create conflicting directory layouts and waste time on setup.

**What:** Create the full directory tree, add __init__.py to all Python packages, configure Dockerfile and docker-compose.yml for development, add GitHub Actions CI for lint and test on every PR.

**Files to create:**
- All __init__.py files in src/ subdirectories
- Dockerfile
- docker-compose.yml
- .github/workflows/ci.yml

**How to test:**
```bash
python -c "from src.agents import supervisor; print('imports work')"
docker-compose build  # should complete without errors
```

**Acceptance Criteria:**
- All src/ packages are importable.
- Docker builds successfully.
- CI runs on PR and reports lint + test results.

**Dependencies:** None (first issue).

---

### Issue #2: Design database schema

**Why:** The schema defines every data relationship in the system. Getting it wrong early means painful migrations later.

**What:** Create SQLAlchemy models for User, Course, Session, EngagementLog, Nudge, Report. Create initial Alembic migration. Document the ERD.

**Files to create:**
- src/models/user.py
- src/models/course.py
- src/models/session.py
- src/models/engagement_log.py
- src/models/nudge.py
- src/models/report.py
- src/models/base.py
- alembic/ (init + first migration)

**How to test:**
```bash
alembic upgrade head
psql engageiq_dev -c "\dt"  # should show all tables
pytest tests/test_models.py
```

**Acceptance Criteria:**
- All 6 tables created with correct columns and foreign keys.
- Alembic migration runs cleanly on fresh database.
- At least 1 test per model.

**Dependencies:** #1

---

### Issue #3: Build webcam capture pipeline

**Why:** The entire system depends on getting frames from a webcam. This is the input to every CV model.

**What:** Build a webcam capture service that reads from browser MediaStream API (via WebSocket to backend) or directly from OpenCV VideoCapture for CLI mode. Support RTSP, file input, and webcam.

**Files to create:**
- src/ingestion/webcam_capture.py
- src/ingestion/stream_handler.py
- src/api/routes/stream.py

**How to test:**
```bash
python -m src.ingestion.webcam_capture --source webcam --fps 15 --duration 10
# Should display 10 seconds of webcam feed with FPS counter
```

**Acceptance Criteria:**
- Captures frames from webcam at configurable FPS (5-30).
- Supports webcam, video file, and RTSP stream inputs.
- WebSocket endpoint accepts frames from browser.
- Graceful shutdown on KeyboardInterrupt.

**Dependencies:** #1

---

### Issue #4: Create frame preprocessing service

**Why:** Raw webcam frames need normalization before any CV model can process them. Preprocessing quality directly affects detection accuracy.

**What:** Build a preprocessing pipeline that detects face region, crops it, resizes to model input dimensions, normalizes pixel values, and controls output FPS.

**Files to create:**
- src/ingestion/frame_extractor.py
- src/utils/image_utils.py

**How to test:**
```bash
python -m src.ingestion.frame_extractor --input data/sample_recordings/test_clip.mp4 --output-fps 10
# Should output preprocessed face crops
```

**Acceptance Criteria:**
- Detects and crops face region from full frame.
- Resizes to configurable dimensions (default 224x224).
- Normalizes pixel values to 0-1 range.
- Drops frames to maintain target FPS.

**Dependencies:** #3

---

### Issue #5: Build user onboarding API

**Why:** Students and teachers have different roles, permissions, and privacy preferences. The onboarding flow captures these at signup.

**What:** Create FastAPI endpoints for user registration, course creation, course enrollment, and privacy preference setting.

**Files to create:**
- src/api/routes/users.py
- src/api/routes/courses.py
- src/api/schemas/user.py
- src/api/schemas/course.py

**How to test:**
```bash
# Register a student
curl -X POST http://localhost:8000/api/users -d '{"name": "Test", "email": "test@nst.edu", "role": "student", "privacy_mode": "local_only"}'

# Create a course
curl -X POST http://localhost:8000/api/courses -d '{"name": "DSA", "code": "CS201", "teacher_id": 1}'
```

**Acceptance Criteria:**
- Student and teacher registration with role-based validation.
- Course CRUD with teacher assignment.
- Privacy preference stored and enforced (local_only or share_with_teacher).
- Input validation with clear error messages.

**Dependencies:** #2

---

## M2: Face Detection and Gaze Estimation

### Issue #6: Integrate MediaPipe Face Mesh

**Why:** Face Mesh provides 468 landmarks that power every downstream detection (pose, gaze, drowsiness, expression). It is the foundation of the entire CV pipeline.

**What:** Integrate MediaPipe Face Mesh, benchmark FPS on laptop CPU, build a visualization overlay, handle face-not-found gracefully.

**Files to create:**
- src/detection/face_mesh.py

**How to test:**
```bash
python -m src.detection.face_mesh --demo
# Should open webcam with 468 landmarks drawn on face, FPS counter in corner
```

**Acceptance Criteria:**
- Detects face and returns 468 landmarks as numpy array.
- Runs at 25+ FPS on laptop CPU.
- Returns None gracefully when no face detected.
- Demo mode visualizes all landmarks with FPS counter.

**Dependencies:** #4

---

### Issue #7: Implement head pose estimation

**Why:** Head pose tells us if the student is facing the screen. A student looking down at their phone or sideways at a roommate is not engaged.

**What:** Select 6 key landmarks (nose tip, chin, left/right eye corner, left/right mouth corner), use OpenCV solvePnP to compute pitch, yaw, roll.

**Files to create:**
- src/detection/head_pose.py

**How to test:**
```bash
python -m src.detection.head_pose --demo
# Should show webcam with 3 axes drawn on face (red=yaw, green=pitch, blue=roll)
# Turn head left/right - yaw changes. Nod - pitch changes.
```

**Acceptance Criteria:**
- Returns pitch, yaw, roll in degrees.
- Accuracy within 5 degrees for frontal and 15-degree offset poses.
- Visualization draws 3-axis gizmo on nose tip.
- Handles partial face occlusion without crashing.

**Dependencies:** #6

---

### Issue #8: Build gaze direction classifier

**Why:** Raw head pose angles need to be classified into actionable categories that the engagement scorer can use.

**What:** Map head pose angles + eye landmark positions to discrete gaze states: at_screen, away_left, away_right, looking_down, eyes_closed.

**Files to create:**
- src/detection/gaze_classifier.py

**How to test:**
```bash
python -m src.detection.gaze_classifier --demo
# Should show webcam with current gaze state label
# Look straight -> "at_screen", look left -> "away_left", close eyes -> "eyes_closed"
```

**Acceptance Criteria:**
- Classifies into 5 states with > 85% accuracy on manual testing.
- Configurable angle thresholds in settings.
- Handles transitions smoothly (no rapid flipping between states).
- Returns confidence score for each classification.

**Dependencies:** #7

---

## M3: Drowsiness and Expression Detection

### Issue #9: Implement EAR-based drowsiness detection

**Why:** Drowsy students are not learning. Detecting prolonged eye closure (vs normal blinks) is the most reliable drowsiness signal.

**What:** Compute Eye Aspect Ratio from MediaPipe eye landmarks. Distinguish blinks (< 0.3s) from drowsiness (> 1.5s) using temporal tracking.

**Files to create:**
- src/detection/drowsiness.py
- src/utils/landmark_utils.py

**How to test:**
```bash
python -m src.detection.drowsiness --demo
# Blink normally -> "blink" label appears briefly
# Close eyes for 2 seconds -> "DROWSY" warning appears
```

**Acceptance Criteria:**
- EAR computed correctly from 6 eye landmarks per eye.
- Blinks (< 0.3s closure) are not flagged as drowsiness.
- Sustained closure (> 1.5s) triggers drowsiness state.
- Thresholds are configurable.
- False positive rate < 5% during normal attentive behavior.

**Dependencies:** #6

---

### Issue #10: Build yawn detection

**Why:** Yawning is a strong fatigue indicator. Frequent yawning (3+ in 5 minutes) signals the student needs a break.

**What:** Compute Mouth Aspect Ratio from lip landmarks. Detect sustained mouth opening as yawns. Track yawn frequency.

**Files to create:**
- src/detection/yawn.py

**How to test:**
```bash
python -m src.detection.yawn --demo
# Open mouth wide for 2 seconds -> "YAWN" detected
# Normal talking should NOT trigger yawn detection
```

**Acceptance Criteria:**
- MAR > 0.6 sustained for > 1.5 seconds classified as yawn.
- Normal speech does not trigger false yawns.
- Yawn frequency tracked (count per 5-minute window).
- 3+ yawns in 5 minutes emits fatigue signal.

**Dependencies:** #6

---

### Issue #11: Train or integrate expression classifier

**Why:** A confused student needs different help than a bored one. Expression classification adds emotional context to raw engagement scores.

**What:** Either integrate the FER library (pre-trained on FER2013) or train a lightweight custom CNN. Classify into 4 classes: engaged, confused, bored, neutral.

**Files to create:**
- src/detection/expression.py
- notebooks/expression_training.ipynb (if custom model)

**How to test:**
```bash
python -m src.detection.expression --demo
# Should show webcam with predicted expression label and confidence
# Make confused face -> "confused", look attentive -> "engaged"
```

**Acceptance Criteria:**
- Classifies 4 expressions with > 70% accuracy on FER2013 test set.
- Inference time < 30ms per frame.
- Returns class label and confidence score.
- Handles varying lighting conditions.

**Dependencies:** #6

---

## M4: Violation Classification and Severity Scoring

### Issue #12: Design multi-signal engagement scoring

**Why:** No single CV signal accurately captures engagement. Combining gaze, pose, expression, and alertness gives a robust score.

**What:** Build a weighted scorer that fuses all detection outputs into a 0-100 engagement score. Weights are configurable per course type.

**Files to create:**
- src/scoring/engagement_score.py
- src/config/scoring_weights.py

**How to test:**
```bash
pytest tests/test_engagement_score.py -v
# Test cases: all signals positive -> score > 90
# Gaze away + drowsy -> score < 20
# Neutral expression + at screen -> score 50-70
```

**Acceptance Criteria:**
- Score range 0-100 with clear interpretation.
- Weights configurable per course (theory vs lab vs seminar).
- Handles missing signals gracefully (e.g., expression model fails -> use remaining signals).
- At least 8 test cases covering edge conditions.

**Dependencies:** #8, #9, #11

---

### Issue #13: Build engagement state machine

**Why:** A continuous score is hard to act on. The state machine provides clear, actionable states with smooth transitions.

**What:** Implement a finite state machine with 5 states (Engaged, Passive, Distracted, Drowsy, Confused). Add hysteresis to prevent rapid flipping.

**Files to create:**
- src/scoring/state_machine.py

**How to test:**
```bash
pytest tests/test_state_machine.py -v
# Test: score 80 for 5 seconds -> state is Engaged
# Test: score drops to 30 for 10 seconds -> state transitions to Distracted (not instant)
# Test: brief score dip (2 seconds) -> state stays Engaged (hysteresis)
```

**Acceptance Criteria:**
- 5 states with configurable score ranges and duration thresholds.
- Hysteresis prevents state changes from transient events.
- State history is logged with timestamps.
- Transitions emit events that downstream agents can subscribe to.

**Dependencies:** #12

---

### Issue #14: Implement temporal smoothing and anomaly filtering

**Why:** Blinks, sneezes, head scratches, and brief glances away are normal. Without filtering, they cause false disengagement alerts.

**What:** Build a temporal filter that smooths engagement scores over a sliding window and filters out anomalous single-frame events.

**Files to create:**
- src/scoring/temporal_filter.py

**How to test:**
```bash
pytest tests/test_temporal_filter.py -v
# Test: inject a single low-score frame among high scores -> output stays high
# Test: sustained low scores (15+ seconds) -> output correctly drops
```

**Acceptance Criteria:**
- Sliding window of configurable size (default 30 frames = 2 seconds at 15 FPS).
- Single-frame anomalies are suppressed.
- Sustained changes are detected within the configured duration threshold.
- Does not introduce more than 1 second of latency.

**Dependencies:** #12

---

## M5: Escalation and Notification Agent

### Issue #15: Build nudge decision agent

**Why:** Nudging at the right time matters. Too early is annoying, too late is useless. The agent must balance helpfulness with non-intrusiveness.

**What:** Build a LangGraph agent that decides when to nudge based on: current state, state duration, recent nudge history, session nudge count, and nudge effectiveness history.

**Files to create:**
- src/nudge/nudge_decision.py
- src/agents/nudge_agent.py

**How to test:**
```bash
pytest tests/test_nudge_decision.py -v
# Test: distracted for 30 seconds, no recent nudge -> should nudge
# Test: distracted for 30 seconds, nudged 2 minutes ago -> should nudge
# Test: distracted for 30 seconds, nudged 1 minute ago -> should NOT nudge (cooldown)
# Test: 5 nudges already sent this session -> should NOT nudge (max reached)
```

**Acceptance Criteria:**
- Nudge triggers after configurable sustained disengagement (default 30 seconds).
- Cooldown of 5 minutes minimum between nudges.
- Maximum nudges per session configurable (default 5).
- Agent considers past nudge effectiveness when deciding.

**Dependencies:** #13

---

### Issue #16: Implement nudge delivery system

**Why:** Different students respond to different nudge types. The system needs multiple channels.

**What:** Build three delivery channels: browser push notification, visual overlay (subtle screen-edge glow), and optional gentle audio chime.

**Files to create:**
- src/nudge/nudge_delivery.py
- frontend/src/components/NudgeOverlay.jsx

**How to test:**
```bash
# Trigger each nudge type manually
python -m src.nudge.nudge_delivery --type notification --message "Time to refocus!"
python -m src.nudge.nudge_delivery --type overlay --message "You seem distracted"
python -m src.nudge.nudge_delivery --type audio
```

**Acceptance Criteria:**
- Browser notification shows with custom message.
- Visual overlay is subtle and non-blocking (screen edge glow, not popup).
- Audio chime is gentle (< 2 seconds, low volume).
- Student can disable any channel in preferences.
- Nudge type is logged for effectiveness tracking.

**Dependencies:** #15

---

### Issue #17: Add nudge effectiveness tracker

**Why:** If nudges don't improve engagement, we should stop sending them. The tracker closes the feedback loop.

**What:** After each nudge, measure engagement score change in the next 60 seconds. Track success rate per nudge type. Feed results back to the decision agent.

**Files to create:**
- src/nudge/effectiveness_tracker.py

**How to test:**
```bash
pytest tests/test_effectiveness_tracker.py -v
# Test: engagement improves after nudge -> effectiveness = positive
# Test: engagement stays low after nudge -> effectiveness = negative
# Test: 3 consecutive ineffective nudges -> agent adjusts strategy
```

**Acceptance Criteria:**
- Measures engagement delta in 60-second post-nudge window.
- Tracks success rate per nudge type (notification vs overlay vs audio).
- Feeds effectiveness data back to nudge decision agent.
- Persists effectiveness history per student across sessions.

**Dependencies:** #16

---

## M6: Compliance Tracking and Analytics

### Issue #18: Build class-level engagement aggregator

**Why:** Teachers need to see the forest, not every tree. Class-level metrics show overall lecture effectiveness.

**What:** Aggregate individual student engagement scores into class-wide metrics: average, distribution, timeline synced to lecture minutes.

**Files to create:**
- src/analytics/class_aggregator.py

**How to test:**
```bash
pytest tests/test_class_aggregator.py -v
# Test: 10 students with scores [80,70,90,60,85,75,65,80,70,90] -> avg 76.5
# Test: timeline shows minute-by-minute engagement curve for the class
```

**Acceptance Criteria:**
- Computes real-time class average, median, and standard deviation.
- Generates minute-by-minute engagement timeline.
- Identifies engagement dip moments (> 15% drop from session average).
- All data uses anonymized student IDs.

**Dependencies:** #13

---

### Issue #19: Implement at-risk student identifier

**Why:** Students who are consistently disengaged across multiple sessions need proactive support, not just session-level nudges.

**What:** Flag students with engagement below a threshold for 3+ consecutive sessions. Detect declining trends using rolling average comparison.

**Files to create:**
- src/analytics/risk_identifier.py
- src/analytics/trend_analyzer.py

**How to test:**
```bash
pytest tests/test_risk_identifier.py -v
# Test: student with avg engagement [40, 35, 30] over 3 sessions -> flagged as at-risk
# Test: student with avg engagement [80, 75, 70] -> declining trend detected
# Test: student with avg engagement [50, 80, 70] -> NOT flagged (not consecutive)
```

**Acceptance Criteria:**
- Flags students below configurable threshold for 3+ sessions.
- Detects declining trend (current week avg < previous week avg by > 10%).
- At-risk list is anonymized for teacher view.
- Supports rolling 7-day and 30-day windows.

**Dependencies:** #18

---

## M7: Report Generator and Intervention Agent

### Issue #20: Build session engagement report

**Why:** After each lecture, both students and teachers want a quick summary of how it went.

**What:** Generate a per-session report with: engagement timeline, key distraction moments, overall score, comparison to class average, top engaged/distracted periods.

**Files to create:**
- src/reports/session_report.py
- src/templates/session_report.html

**How to test:**
```bash
python -m src.reports.session_report --session-id 1 --output report.html
# Open report.html - should show engagement timeline chart, score summary, key moments
```

**Acceptance Criteria:**
- Report includes engagement timeline chart.
- Highlights top 3 distraction moments with timestamps.
- Shows overall session score and class average comparison.
- Renders as HTML (viewable in browser) and sendable as email.

**Dependencies:** #18

---

### Issue #21: Build weekly trend report

**Why:** Weekly patterns reveal systemic issues (Monday 8am lectures always have low engagement) that session reports miss.

**What:** Generate weekly report with: engagement curves per lecture, day-of-week patterns, week-over-week improvement tracking, class ranking (anonymized).

**Files to create:**
- src/reports/weekly_report.py
- src/templates/weekly_report.html

**How to test:**
```bash
python -m src.reports.weekly_report --course-id 1 --week 2026-W24 --output weekly.html
```

**Acceptance Criteria:**
- Shows engagement trend across all lectures in the week.
- Identifies day/time patterns (e.g., "Friday 4pm consistently lowest").
- Compares to previous week with delta indicators.
- Exportable as HTML and PDF.

**Dependencies:** #20

---

### Issue #22: Implement LLM-powered intervention agent

**Why:** Raw analytics tell teachers what happened but not what to do about it. The LLM agent bridges data to action.

**What:** Build a LangGraph agent that analyzes engagement data and generates specific, actionable teaching suggestions. Avoid generic advice.

**Files to create:**
- src/agents/intervention_agent.py

**How to test:**
```bash
python -m src.agents.intervention_agent --session-id 1
# Should output 3+ specific suggestions like:
# "Engagement dropped 25% at minute 14 (recursion topic). Consider adding a live coding example."
# "Class engagement peaks during Q&A segments. Add 2-minute Q&A breaks every 15 minutes."
```

**Acceptance Criteria:**
- Generates 3+ actionable suggestions per session.
- Suggestions reference specific timestamps and engagement data.
- No generic advice ("make it more engaging" is a failure).
- Uses Groq (free tier) by default.

**Dependencies:** #18, #20

---

### Issue #23: Add content difficulty correlator

**Why:** Engagement dips are often caused by content difficulty, not student laziness. Identifying hard topics helps teachers prepare better.

**What:** Map engagement dips to lecture segments. Flag topics that consistently cause disengagement across multiple sessions.

**Files to create:**
- src/analytics/difficulty_correlator.py

**How to test:**
```bash
pytest tests/test_difficulty_correlator.py -v
# Test: engagement dips at minute 14, 28, 42 -> flags those segments
# Test: same topic causes dips across 3 sessions -> flagged as consistently difficult
```

**Acceptance Criteria:**
- Identifies segments where engagement drops > 15% from session average.
- Tracks which segments are problematic across multiple sessions.
- Outputs ranked list of difficult segments with timestamps.
- Works even without access to slide content (uses timing only).

**Dependencies:** #18

---

## M8: Dashboard, Integration and Demo

### Issue #24: Build student dashboard

**Why:** Students need a personal view of their engagement data to self-improve.

**What:** React dashboard showing: engagement history across sessions, focus streaks, self-improvement tips, session-by-session comparison.

**Files to create:**
- frontend/src/pages/StudentDashboard.jsx
- frontend/src/components/EngagementChart.jsx
- frontend/src/components/FocusStreak.jsx
- frontend/src/components/SessionHistory.jsx

**How to test:**
- Navigate to /student/dashboard after login.
- Should show engagement chart for last 7 sessions.
- Focus streak counter should increment for sessions with avg engagement > 70.

**Acceptance Criteria:**
- Shows engagement history with interactive charts.
- Focus streak counter (consecutive sessions > 70 avg).
- Self-improvement tips based on personal patterns.
- Responsive design (works on laptop and phone).

**Dependencies:** #20

---

### Issue #25: Build teacher dashboard

**Why:** Teachers need a single view to monitor class engagement and take action.

**What:** React dashboard showing: class overview, real-time engagement during live sessions (WebSocket), historical analytics, intervention suggestions.

**Files to create:**
- frontend/src/pages/TeacherDashboard.jsx
- frontend/src/components/ClassOverview.jsx
- frontend/src/components/LiveEngagement.jsx
- frontend/src/components/InterventionPanel.jsx

**How to test:**
- Navigate to /teacher/dashboard after login.
- During a live session, engagement scores should update in real-time.
- At-risk students should be highlighted (anonymized).

**Acceptance Criteria:**
- Real-time class engagement updates via WebSocket (< 2 second latency).
- Historical view with session selector.
- At-risk students highlighted with trend indicators.
- Intervention suggestions panel shows LLM recommendations.

**Dependencies:** #19, #22, #24

---

### Issue #26: E2E testing, demo video, deployment guide

**Why:** The project must work end-to-end and be demonstrable. A demo video is required for portfolio and faculty review.

**What:** Write E2E tests using pre-recorded webcam sessions. Record a 3-5 minute demo video. Write deployment guide for Docker on Railway/Render.

**Files to create:**
- tests/test_e2e.py
- docs/deployment_guide.md
- docs/demo_script.md

**How to test:**
```bash
pytest tests/test_e2e.py -v
# Should process a 10-minute recorded session through full pipeline:
# frame extraction -> detection -> scoring -> nudge -> analytics -> report
```

**Acceptance Criteria:**
- E2E test processes recorded session without errors.
- Demo video shows complete flow (student joins, engagement tracked, nudge sent, teacher sees analytics).
- Deployment guide covers Docker build, env setup, database migration, and hosting.
- All existing tests still pass.

**Dependencies:** #24, #25

---

NST Engineering - EngageIQ AI | Summer Profile Building Drive 2026
