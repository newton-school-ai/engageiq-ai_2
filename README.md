# EngageIQ AI

Agentic classroom engagement monitoring system that uses webcam-based computer vision to track student attention during online and hybrid lectures.

Built by a 5-student pod at Newton School of Technology (NST) as part of the Summer Profile Building Drive 2026.

---

## What It Does

EngageIQ AI watches your webcam during a lecture and tells you (and optionally your teacher) how engaged you are. It detects drowsiness, distraction, confusion, and phone usage in real-time using computer vision -- then an AI agent scores your engagement, nudges you when you drift off, and generates actionable analytics.

**For Students:** Personal engagement timeline, focus streaks, self-improvement tips, smart nudges.
**For Teachers:** Class-level analytics, engagement heatmaps, at-risk student flags, pedagogical suggestions.

**Privacy first:** All CV processing happens on your device. No video is stored or transmitted. Teachers only see anonymized aggregate scores. You can opt out at any time.

---

## Key Features

- Real-time face detection with 468 facial landmarks (MediaPipe Face Mesh)
- Head pose estimation (pitch, yaw, roll) for gaze tracking
- Drowsiness detection via Eye Aspect Ratio (EAR) with blink filtering
- Yawn detection via Mouth Aspect Ratio (MAR)
- Facial expression classification (engaged, confused, bored, neutral)
- Phone/object detection (YOLOv8 nano)
- Multi-signal engagement scoring with configurable weights
- Engagement state machine (Engaged / Passive / Distracted / Drowsy / Confused)
- Smart nudge agent with cooldown and effectiveness tracking
- LLM-powered intervention suggestions for teachers
- Session and weekly engagement reports
- Student dashboard and teacher dashboard (React + Tailwind)

---

## Tech Stack

| What | Tool |
|------|------|
| Agent orchestration | LangGraph |
| Face detection | MediaPipe Face Mesh (468 landmarks) |
| Head pose | OpenCV solvePnP |
| Expression classifier | FER library or custom CNN |
| Object detection | YOLOv8n (Ultralytics) |
| LLM | Groq (default, free), Gemini, Ollama |
| Backend | FastAPI |
| Frontend | React + Tailwind CSS |
| Database | PostgreSQL + Alembic |
| Real-time | WebSocket |
| Deployment | Docker + Railway or Render |

---

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (for frontend)
- Webcam (laptop built-in or USB)

### Setup

```bash
# Clone
git clone https://github.com/newton-school-ai/engageiq-ai.git
cd engageiq-ai

# Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env with your Groq API key (free at console.groq.com)

# Database
createdb engageiq_dev
alembic upgrade head

# Run backend
uvicorn src.api.main:app --reload --port 8000

# Run frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Test with your webcam

```bash
# Quick test - point webcam at yourself
python -m src.detection.face_mesh --demo

# Full session test - watch any lecture video with webcam on
python -m src.agents.supervisor --mode student --duration 30
```

---

## Project Structure

```
src/
  agents/         Supervisor, engagement scorer, nudge agent, intervention agent
  detection/      Face mesh, head pose, gaze, drowsiness, yawn, expression, object detection
  ingestion/      Webcam capture, frame extraction, stream handling
  scoring/        Engagement score, state machine, temporal filtering
  nudge/          Nudge decisions, delivery, effectiveness tracking
  analytics/      Class aggregation, risk identification, trend analysis
  reports/        Session reports, weekly reports, intervention suggestions
  api/            FastAPI routes
  models/         SQLAlchemy database models
  templates/      Jinja2 email/report templates
  utils/          Image, landmark, math, time utilities
  config/         Settings, enums, thresholds
```

---

## Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - Branch strategy, PR workflow, coding standards
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - Full setup guide, daily workflow, testing
- [MILESTONES.md](MILESTONES.md) - M1-M8 with acceptance criteria and defense questions
- [ISSUES_TRACKER.md](ISSUES_TRACKER.md) - All 26 issues with full descriptions
- [POD_GUIDE.md](POD_GUIDE.md) - Pod roles, sprint timeline, Q&A schedule

---

## Pod

| Role | Owns |
|------|------|
| Maintainer | Repo arch, supervisor agent, config, M1+M8 |
| Contributor 1 | M2 - Face Detection + Head Pose + Gaze |
| Contributor 2 | M3+M4 - Drowsiness/Expression + Engagement Scoring |
| Contributor 3 | M5 - Nudge Agent + Delivery System |
| Contributor 4 | M6+M7 - Teacher Analytics + Report Generator |

---

## Milestones

| # | Name | Status |
|---|------|--------|
| M1 | Project Scaffold and Webcam Pipeline | Todo |
| M2 | Face Detection and Gaze Estimation | Todo |
| M3 | Drowsiness and Expression Detection | Todo |
| M4 | Engagement Scoring Agent | Todo |
| M5 | Nudge Agent and Delivery System | Todo |
| M6 | Teacher Analytics and Insights | Todo |
| M7 | Report Generator and Intervention Agent | Todo |
| M8 | Dashboard, Integration and Demo | Todo |

---

## License

MIT

---

NST Engineering - EngageIQ AI | Summer Profile Building Drive 2026
