# 🛡️ SafeGuard Insurance – End-to-End QA Portfolio Project

![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Tests](https://img.shields.io/badge/Test%20Cases-60%2B-blue)
![Automation](https://img.shields.io/badge/Automation-Playwright%20%2B%20Python-green)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)

A complete, end-to-end QA testing portfolio project built on a custom insurance web application. This project demonstrates real-world QA skills including manual testing, API testing, test automation, SQL validation, and CI/CD integration.

---

## 📋 Project Overview

| Item | Details |
|---|---|
| **Application** | SafeGuard Insurance – Policy & Claims Management System |
| **Tech Stack** | Python, Flask, SQLite, Bootstrap 5 |
| **Testing Types** | Manual, API, UI Automation, Database, Regression |
| **Automation Tools** | Playwright + Python + Pytest |
| **API Testing** | Postman |
| **CI/CD** | GitHub Actions |
| **Agile Tool** | Jira |
| **Domain** | Insurance |

---

## 🗂️ Repository Structure

```
Insurance-Policy-QA-Project/
│
├── 📁 Application/          # Flask web app (the system under test)
├── 📁 TestPlan/             # Test Strategy & Test Plan document
├── 📁 TestCases/            # 60+ manual test cases (Excel)
├── 📁 RTM/                  # Requirements Traceability Matrix
├── 📁 BugReports/           # 15+ detailed bug reports
├── 📁 SQLQueries/           # Database validation SQL queries
├── 📁 Postman/              # Postman collection (API tests)
├── 📁 Automation/           # Playwright + Pytest automation framework
│   ├── tests/               # Test scripts
│   ├── pages/               # Page Object Model classes
│   ├── locators/            # Element locators
│   ├── utilities/           # Helpers & config
│   ├── reports/             # HTML test reports
│   └── screenshots/         # Failure screenshots
├── 📁 CI-CD/                # GitHub Actions workflow
├── 📁 AgileDocs/            # Jira sprint artifacts
└── 📄 README.md
```

---

## ✅ Application Modules Tested

| Module | Manual | API | Automated |
|---|---|---|---|
| User Registration | ✅ | ✅ | ✅ |
| Login / Logout | ✅ | ✅ | ✅ |
| Quote Generator | ✅ | ✅ | ✅ |
| Policy Purchase | ✅ | — | ✅ |
| Claims Submission | ✅ | ✅ | ✅ |
| Claim Tracking | ✅ | ✅ | — |
| Admin Dashboard | ✅ | — | — |
| Claims Approval | ✅ | — | — |

---

## 🧪 Test Summary

| Category | Count |
|---|---|
| Total Test Cases | 60+ |
| Passed | TBD |
| Failed | TBD |
| Blocked | TBD |
| Bug Reports | 15+ |
| API Test Cases | 20+ |
| Automated Scripts | 10+ |

---

## 🚀 Running the Application

```bash
cd Application
pip install -r requirements.txt
python app.py
# Open: http://localhost:5000
```

**Demo credentials:**
- Admin: `admin@insurance.com` / `Admin@1234`
- Customer: Register a new account

---

## 🤖 Running Automation Tests

```bash
cd Automation
pip install pytest playwright
playwright install chromium
pytest tests/ --html=reports/report.html
```

---

## 🔗 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register customer |
| POST | `/api/login` | Customer login |
| GET | `/api/policies` | Get all policies |
| POST | `/api/quote` | Generate quote |
| POST | `/api/claim` | Submit claim |
| GET | `/api/claim/{id}` | Get claim by ID |

---

## 📌 Skills Demonstrated

`Manual Testing` `Test Case Design` `Bug Reporting` `API Testing (Postman)`
`SQL / Database Testing` `UI Test Automation` `Playwright` `Pytest`
`Page Object Model` `CI/CD (GitHub Actions)` `Agile / Scrum` `Jira`
`RTM` `Insurance Domain Knowledge` `Python` `Git / GitHub`

---

## 👤 About

**Sahil** – QA Analyst | Winnipeg, MB  
Open to QA Analyst / Associate QA / Software Tester roles  
📧 [your email] | 🔗 [your LinkedIn]
