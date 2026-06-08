# Milestones

All 8 milestones with acceptance criteria and defense questions.
Framework: Build, Understand, Defend.

---

## M1: Project Scaffold and Webcam Pipeline

**Owner:** Maintainer
**Issues:** #1-5
**Duration:** Week 1

### Acceptance Criteria
- Repo has clean directory structure with all packages importable.
- PostgreSQL schema created via Alembic migration (users, courses, sessions, engagement_logs, nudges, reports tables).
- Webcam capture pipeline reads frames at configurable FPS.
- Frame preprocessing outputs normalized, cropped face regions.
- User onboarding API supports student/teacher roles with privacy preferences.
- All endpoints documented in FastAPI /docs.
- At least 3 tests pass.

### Defense Questions
- Why PostgreSQL over SQLite for a project of this scale?
- What is Alembic and why do we need migrations instead of raw SQL?
- How does WebSocket differ from HTTP polling for real-time frame streaming?
- What FPS is sufficient for engagement detection and why?
- How does the privacy_mode config affect data flow?

---

## M2: Face Detection and Gaze Estimation

**Owner:** Contributor 1
**Issues:** #6-8
**Duration:** Week 2

### Acceptance Criteria
- MediaPipe Face Mesh detects 468 landmarks at 25+ FPS on laptop CPU.
- Head pose estimation returns pitch, yaw, roll angles within 5-degree accuracy.
- Gaze classifier outputs one of: at_screen, away_left, away_right, looking_down, eyes_closed.
- Works in varied lighting (desk lamp, window light, dim room).
- Demo script visualizes landmarks and pose axes on webcam feed.
- At least 5 tests pass.

### Defense Questions
- Why MediaPipe over dlib or OpenCV's Haar cascades?
- Explain the solvePnP algorithm for head pose estimation. What are the 6 model points?
- How do you handle the case where the face is partially occluded?
- What is the coordinate system for pitch/yaw/roll and what thresholds indicate "looking away"?
- Why 468 landmarks instead of the simpler 68-point model?

---

## M3: Drowsiness and Expression Detection

**Owner:** Contributor 2
**Issues:** #9-11
**Duration:** Week 3

### Acceptance Criteria
- EAR computation correctly distinguishes blinks (< 0.3s) from drowsiness (> 1.5s).
- MAR-based yawn detection triggers on sustained mouth opening (> 1.5s).
- Expression classifier achieves > 70% accuracy on FER2013 test set for 4 classes.
- Drowsiness and yawn detectors have configurable thresholds.
- False positive rate for drowsiness is below 5% during normal attentive behavior.
- At least 5 tests pass.

### Defense Questions
- Derive the EAR formula. Why does it work for drowsiness?
- How do you differentiate a blink from drowsiness using only temporal information?
- What is FER2013? What are its known limitations?
- Why 4 expression classes instead of the standard 7?
- How does the MAR formula differ from EAR and why?

---

## M4: Engagement Scoring Agent

**Owner:** Contributor 2
**Issues:** #12-14
**Duration:** Week 4

### Acceptance Criteria
- Multi-signal scorer combines gaze, pose, expression, alertness into 0-100 score.
- State machine transitions between 5 states with hysteresis (no rapid flipping).
- Temporal smoothing prevents false state changes from blinks, sneezes, brief glances.
- Scoring weights are configurable per course type in settings.
- Deduplication engine groups same-type violations within 5-minute windows.
- At least 5 tests pass.

### Defense Questions
- Why weighted average instead of a trained ML model for score fusion?
- What is hysteresis in the context of state machines and why is it needed here?
- How do you tune the duration thresholds for each state transition?
- What happens when two conflicting signals arrive (e.g., engaged expression but looking away)?
- How would you validate that the engagement score correlates with actual learning outcomes?

---

## M5: Nudge Agent and Delivery System

**Owner:** Contributor 3
**Issues:** #15-17
**Duration:** Week 5

### Acceptance Criteria
- Nudge agent triggers only after sustained disengagement (configurable threshold).
- Cooldown period prevents repeated nudges (minimum 5 minutes between nudges).
- Maximum nudges per session is configurable (default: 5).
- Three delivery channels work: browser notification, visual overlay, audio chime.
- Effectiveness tracker measures engagement change in 60-second post-nudge window.
- Nudge log records timestamp, type, trigger state, and post-nudge engagement delta.
- At least 5 tests pass.

### Defense Questions
- How do you prevent nudge fatigue? What is the optimal nudge frequency?
- Why track nudge effectiveness? How does the agent use this feedback?
- What is the tradeoff between nudging too early (annoying) and too late (student already lost)?
- How would you A/B test different nudge types to find what works best?
- Why is max nudges per session important from a UX perspective?

---

## M6: Teacher Analytics and Insights

**Owner:** Contributor 4
**Issues:** #18-19
**Duration:** Week 6

### Acceptance Criteria
- Class-level aggregator computes real-time average engagement across all students.
- Engagement timeline is synced to lecture timestamps (minute-by-minute).
- At-risk identifier flags students with engagement below threshold for 3+ consecutive sessions.
- Declining trend detection uses rolling average comparison (current week vs previous).
- All analytics use anonymized student IDs (teacher never sees names unless student opts in).
- At least 3 tests pass.

### Defense Questions
- How do you aggregate engagement scores across students with different baselines?
- What statistical method do you use for trend detection?
- How do you define "at-risk" and what are the false positive implications?
- Why is anonymization implemented at the data layer rather than just the UI layer?
- How would you handle a class where most students have low engagement (is the content the problem)?

---

## M7: Report Generator and Intervention Agent

**Owner:** Contributor 4
**Issues:** #20-23
**Duration:** Week 7

### Acceptance Criteria
- Session report includes per-student timeline, distraction moments, overall score, class comparison.
- Weekly report includes engagement curves, day-of-week patterns, improvement tracking.
- LLM intervention agent produces at least 3 actionable suggestions per session.
- Content difficulty correlator maps engagement dips to specific lecture segments.
- Reports render as HTML email and downloadable PDF.
- At least 3 tests pass.

### Defense Questions
- What prompt engineering techniques make the LLM produce actionable teaching suggestions?
- How do you correlate engagement dips with lecture content without access to slide content?
- What is the difference between a session report and a weekly report in terms of audience and purpose?
- How do you prevent the LLM from generating generic advice like "make it more interesting"?
- What feedback loop would improve intervention suggestions over time?

---

## M8: Dashboard, Integration and Demo

**Owner:** Maintainer
**Issues:** #24-26
**Duration:** Week 8

### Acceptance Criteria
- Student dashboard shows personal engagement history, focus streaks, tips.
- Teacher dashboard shows class overview, real-time monitoring, historical analytics.
- Real-time WebSocket updates engagement scores on teacher dashboard within 2 seconds.
- E2E test processes a 10-minute pre-recorded session through full pipeline without errors.
- Demo video (3-5 minutes) shows complete flow: student joins, engagement tracked, nudge delivered, teacher sees analytics.
- Deployment guide covers Docker setup on Railway or Render.
- All existing tests still pass.

### Defense Questions
- How does WebSocket handle 60+ simultaneous student connections?
- What is your strategy for E2E testing a system that depends on a webcam?
- How would you scale this to handle 500 students in a single lecture?
- What are the key metrics you would track in production to know the system is working?
- If you had 2 more weeks, what would you build next?

---

NST Engineering - EngageIQ AI | Summer Profile Building Drive 2026
