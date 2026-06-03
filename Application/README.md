# SafeGuard Insurance – QA Portfolio App

A full-stack insurance web application built specifically as a QA testing portfolio project.

## Tech Stack
- **Backend:** Python + Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Frontend:** HTML + Bootstrap 5

## Features
| Module | Description |
|---|---|
| Registration | Create a customer account |
| Login | Authenticate as customer or admin |
| Quote Generator | Calculate insurance premiums |
| Policy Purchase | Buy a policy from a quote |
| Claims Submission | File a claim against an active policy |
| Claim Tracking | Monitor claim status |
| Admin Dashboard | View stats, manage customers & claims |
| REST API | 6 endpoints for Postman/API testing |

## Setup Instructions

### 1. Install Python
Make sure Python 3.8+ is installed: https://python.org

### 2. Create a virtual environment
```bash
cd insurance-app
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

## Login Credentials
| Role | Email | Password |
|---|---|---|
| Admin | admin@insurance.com | Admin@1234 |
| Customer | Register a new account |  |

## REST API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/register | Register a customer |
| POST | /api/login | Login |
| GET | /api/policies | Get all policies |
| POST | /api/quote | Get a premium quote |
| POST | /api/claim | Submit a claim |
| GET | /api/claim/{id} | Get claim by ID |

## Project Structure (QA Portfolio)
```
Insurance-Policy-QA-Project/
├── Application/          ← This app
├── TestPlan/
├── TestCases/
├── RTM/
├── BugReports/
├── SQLQueries/
├── Postman/
├── Automation/
├── CI-CD/
├── AgileDocs/
└── README.md
```
