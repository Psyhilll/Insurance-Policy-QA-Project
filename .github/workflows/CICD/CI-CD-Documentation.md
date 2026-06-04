# CI/CD Pipeline – SafeGuard Insurance QA

## Overview
This project uses **GitHub Actions** as the CI/CD platform.
Every time code is pushed to `master`, the pipeline automatically:

1. Starts the Flask application
2. Creates a test user via the API
3. Runs all 28 Playwright tests
4. Generates an HTML test report
5. Uploads the report and screenshots as downloadable artifacts

---

## Pipeline Diagram

```
Code Push to master
        │
        ▼
┌─────────────────────┐
│  Checkout Code      │  actions/checkout@v4
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Setup Python 3.11  │  actions/setup-python@v5
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Install App Deps   │  Flask, SQLAlchemy, Werkzeug
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Start Flask App    │  python app.py (background)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Verify App Running │  curl http://localhost:5000
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Install Playwright │  pytest-playwright + chromium
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Create Test User   │  POST /api/register
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Run Pytest Suite   │  28 tests across 5 modules
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Upload Artifacts   │  HTML Report + Screenshots
└────────┬────────────┘
         │
         ▼
    Pipeline Done ✅
```

---

## Workflow File Location
```
.github/workflows/qa-pipeline.yml
```

## How to Trigger Manually
1. Go to your GitHub repo
2. Click **Actions** tab
3. Click **SafeGuard Insurance – QA Automation Pipeline**
4. Click **Run workflow** → **Run workflow**

## Viewing Results
1. Go to **Actions** tab on GitHub
2. Click the latest workflow run
3. Scroll to **Artifacts** section
4. Download `playwright-test-report` to view the HTML report

---

## What This Demonstrates
- Automated test execution on every code push
- No manual intervention needed to run tests
- Test results preserved as downloadable artifacts
- Industry-standard DevOps practice (GitHub Actions)
