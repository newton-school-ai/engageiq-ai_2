# Pull Request Log

## Issue 1
**By:** Gargi

The main problem was that the Docker setup wasn't working because the frontend hadn't been scaffolded yet and some Docker packages were outdated. I updated the Dockerfile with compatible package names,temporarily disabled the frontend service in Docker Compose and verified that the backend and PostgreSQL containers started successfully. After that, I confirmed the backend was running through the health endpoint.

---

## Issue 2
**By:** Gargi

This issue was about setting up a GitHub Actions CI workflow to automatically check every PR. I created the workflow from scratch, configured it to run formatting, linting and test checks on Prs to  dev and main and tested the same commands locally. While testing, I found some existing formatting and lint issues in the repository but since they were unrelated to the task ,I kept the PR focused only on the CI setup.
