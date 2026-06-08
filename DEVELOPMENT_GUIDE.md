# Development Guide

Complete setup from scratch, daily workflow, and testing guide for EngageIQ AI.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | python.org or `pyenv install 3.10` |
| PostgreSQL | 14+ | `brew install postgresql` (Mac) or `sudo apt install postgresql` (Ubuntu) |
| Node.js | 18+ | nodejs.org or `nvm install 18` |
| Git | 2.30+ | git-scm.com |
| Webcam | Any | Laptop built-in or USB webcam |

Optional: Docker (for deployment only, not needed for development).

---

## Step 1: Clone and Branch

```bash
git clone https://github.com/newton-school-ai/engageiq-ai.git
cd engageiq-ai
git checkout dev
git checkout -b feature/issue-N-your-task
```

---

## Step 2: Python Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Verify MediaPipe and OpenCV:
```bash
python -c "import mediapipe; print(mediapipe.__version__)"
python -c "import cv2; print(cv2.__version__)"
```

---

## Step 3: Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:
- `GROQ_API_KEY` - Get free at https://console.groq.com (required for agent features)
- `DATABASE_URL` - Your local PostgreSQL connection string
- Other keys are optional for initial development

---

## Step 4: Database

```bash
# Create database
createdb engageiq_dev

# Run migrations
alembic upgrade head

# Verify
psql engageiq_dev -c "\dt"
```

---

## Step 5: Run Backend

```bash
uvicorn src.api.main:app --reload --port 8000
```

API docs at http://localhost:8000/docs

---

## Step 6: Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard at http://localhost:5173

---

## Step 7: Test Webcam Pipeline

```bash
# Quick detection test - opens webcam window with landmark overlay
python -m src.detection.face_mesh --demo

# Engagement scoring test - runs full pipeline for 60 seconds
python -m src.agents.supervisor --mode student --duration 60
```

---

## Daily Workflow

```bash
# 1. Start your day - sync with dev
git checkout dev
git pull origin dev
git checkout feature/issue-N-your-task
git rebase dev

# 2. Work on your task
# ... write code ...

# 3. Run tests before committing
pytest tests/ -v
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# 4. Commit with conventional format
git add .
git commit -m "feat(detection): add head pose estimation using solvePnP"

# 5. Push and open PR when ready
git push origin feature/issue-N-your-task
# Open PR on GitHub targeting dev
```

---

## Testing Guide

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Module Tests

```bash
pytest tests/test_drowsiness.py -v
pytest tests/test_engagement_score.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Testing CV Components Without Webcam

Many tests use static images or pre-recorded frames in `data/sample_recordings/`:

```bash
# Test face detection on a static image
python -m src.detection.face_mesh --image data/sample_recordings/test_face.jpg

# Test drowsiness on a pre-recorded clip
python -m src.detection.drowsiness --video data/sample_recordings/drowsy_demo.mp4
```

### Testing Engagement Pipeline

```bash
# Process a recorded session (no live webcam needed)
python -m src.agents.supervisor --mode student --input data/sample_recordings/session_01.mp4

# Check output
cat data/sample_recordings/session_01_report.json
```

---

## Formatting and Linting

```bash
# Format
black src/ tests/
isort src/ tests/ --profile black

# Lint
flake8 src/ tests/ --max-line-length 88

# Type check (optional)
mypy src/ --ignore-missing-imports
```

---

## Troubleshooting

### MediaPipe not detecting face
- Ensure good lighting on your face.
- Webcam must be at face level, not pointing at ceiling.
- Check webcam permissions in browser/OS settings.

### OpenCV webcam not opening
- Try different camera index: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`.
- On Mac: grant terminal camera permission in System Settings > Privacy > Camera.

### PostgreSQL connection refused
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env matches your local setup.

### Groq API rate limit
- Free tier allows 30 requests/minute. Add retry logic with backoff.
- For development, use Ollama (local) to avoid rate limits entirely.

---

NST Engineering - EngageIQ AI | Summer Profile Building Drive 2026
