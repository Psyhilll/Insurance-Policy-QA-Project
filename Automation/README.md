# SafeGuard Insurance – Playwright Automation Framework

## Structure
```
Automation/
├── tests/           # Test scripts (one file per module)
├── pages/           # Page Object Model classes
├── locators/        # All element locators
├── utilities/       # Helpers (random data, screenshots)
├── reports/         # HTML test reports (auto-generated)
├── screenshots/     # Failure/pass screenshots
├── conftest.py      # Pytest fixtures & browser setup
├── pytest.ini       # Pytest configuration
└── requirements.txt # Dependencies
```

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
playwright install chromium
```

## Run All Tests
```bash
# Make sure app is running first: python app.py
pytest
```

## Run Specific Module
```bash
pytest tests/test_login.py
pytest tests/test_registration.py
pytest tests/test_quote.py
pytest tests/test_claims.py
pytest tests/test_admin.py
```

## Run a Single Test
```bash
pytest tests/test_login.py::TestLogin::test_valid_customer_login
```

## View Report
Open `reports/test_report.html` in your browser after running tests.

## Test Accounts
| Role     | Email                    | Password   |
|----------|--------------------------|------------|
| Admin    | admin@insurance.com      | Admin@1234 |
| Customer | playwright@test.com      | Test@1234  |

## Pre-requisite
Register `playwright@test.com` manually once before running tests,
then purchase at least one policy so claims tests have data to work with.
