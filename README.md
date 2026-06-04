# 🛡️ SafeGuard Insurance – End-to-End QA Portfolio Project

<div align="center">

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Tests](https://img.shields.io/badge/Test%20Cases-60%2B-blue)
![Automation](https://img.shields.io/badge/Automation-Playwright%20%2B%20Python-blueviolet)
![API](https://img.shields.io/badge/API%20Testing-Postman-orange)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-yellow)
![Database](https://img.shields.io/badge/DB%20Testing-SQLite%20%2B%20SQL-lightgrey)

**A complete, end-to-end QA testing portfolio project built on a custom-developed insurance web application.**

[📋 Test Plan](#-test-plan) • [🧪 Test Cases](#-test-cases) • [🐛 Bug Reports](#-bug-reports) • [🤖 Automation](#-automation) • [🔗 API Testing](#-api-testing) • [🗄️ SQL Testing](#-sql-testing) • [⚙️ CI/CD](#-cicd-pipeline)

</div>

---

## 📌 Project Overview

| Item | Details |
|---|---|
| **Application** | SafeGuard Insurance – Policy & Claims Management System |
| **Purpose** | QA Portfolio Project demonstrating end-to-end testing skills |
| **Tech Stack** | Python, Flask, SQLite, Bootstrap 5 |
| **Testing Types** | Manual, API, UI Automation, Database, Regression, Security |
| **Automation** | Playwright + Python + Pytest |
| **API Testing** | Postman (12 test cases, 6 endpoints) |
| **CI/CD** | GitHub Actions (auto-runs on every push) |
| **Agile** | Jira (Sprint planning, backlog, defect tracking) |
| **Domain** | Insurance |

---

## 🏗️ Application – What Was Built

A full-stack insurance web application built from scratch as the system under test.

### Modules
| Module | Description |
|---|---|
| 🔐 Registration | New customer account creation with validation |
| 🔑 Login / Logout | Session-based authentication for customers and admin |
| 📊 Customer Dashboard | Policy summary, claims overview, quick actions |
| 💰 Quote Generator | Premium calculator (Auto, Health, Life, Home) |
| 📄 Policy Purchase | Buy insurance from a generated quote |
| 📋 Claims Submission | File a claim against an active policy |
| 🔍 Claim Tracking | Monitor claim status in real time |
| 🛡️ Admin Panel | Manage customers, approve/reject claims |
| 🌐 REST API | 6 endpoints for automated and API testing |

### How to Run the App
```bash
cd Application
pip install -r requirements.txt
python app.py
# Open: http://localhost:5000
```

**Demo Credentials:**
| Role | Email | Password |
|---|---|---|
| Admin | admin@insurance.com | Admin@1234 |
| Customer | Register a new account | — |

---

## 📋 Test Plan

📁 `TestPlan/TestPlan_SafeGuard_Insurance.docx`

A professional 11-section test plan covering:

- ✅ Project scope (in-scope and out-of-scope modules)
- ✅ Test strategy (8 testing types with tools)
- ✅ Test environment setup
- ✅ Entry and exit criteria
- ✅ Risk analysis with mitigations
- ✅ Test schedule (10-phase timeline)
- ✅ Roles and deliverables

---

## 🧪 Test Cases

📁 `TestCases/TestCases_SafeGuard.xlsx`
📁 `RTM/RTM_SafeGuard.xlsx`

**60 manual test cases** across 6 modules with live pass/fail tracking.

| Module | Test Cases | Coverage |
|---|---|---|
| Registration | TC001 – TC010 | Valid, duplicate, empty, boundary |
| Login | TC011 – TC020 | Valid, invalid, session, security |
| Quote Generator | TC021 – TC030 | All types, age/coverage boundaries |
| Policy Purchase | TC031 – TC038 | Valid flow, date validation, access control |
| Claims | TC039 – TC050 | Submit, boundary, tracking, status |
| Admin | TC051 – TC060 | Dashboard, approve/reject, access control |

**RTM (Requirements Traceability Matrix):** 24 requirements mapped to test cases — every requirement is covered.

---

## 🐛 Bug Reports

📁 `BugReports/BugReports_SafeGuard.docx`

**13 documented bugs** — 1 found during real testing, 12 intentionally planted for demonstration.

| Bug ID | Title | Severity | Status |
|---|---|---|---|
| BUG-001 | Expired policy stays Active — claims accepted | 🔴 High | Open |
| BUG-002 | Admin panel accessible by any customer (URL) | 🔴 Critical | Open |
| BUG-003 | Quote accepts age 0 and negative values | 🔴 High | Open |
| BUG-004 | Claim reason accepts 1 character | 🟠 Medium | Open |
| BUG-005 | No confirmation before claim submission | 🟢 Low | Open |
| BUG-006 | Premium shows $0 for coverage under $1,000 | 🔴 High | Open |
| BUG-007 | Whitespace-only password accepted | 🔴 High | Open |
| BUG-008 | Invalid email format accepted (no domain) | 🟠 Medium | Open |
| BUG-009 | End date can be before start date | 🔴 High | Open |
| BUG-010 | Claim amount field accepts letters | 🟠 Medium | Open |
| BUG-011 | Empty table shown when no admin claims | 🟢 Low | Open |
| BUG-012 | Dashboard shows $0 vs N/A for new users | 🟢 Low | Open |
| BUG-013 | No password strength indicator | 🟢 Low | Open |

Each bug report includes: **Steps to Reproduce, Expected vs Actual Result, Severity, Priority, Root Cause, and Recommendation.**

---

## 🤖 Automation

📁 `Automation/`

**28 automated tests** built with **Playwright + Python + Pytest** using the **Page Object Model** design pattern.

### Framework Structure
```
Automation/
├── tests/              # Test scripts (one per module)
│   ├── test_login.py          # 8 tests
│   ├── test_registration.py   # 6 tests
│   ├── test_quote.py          # 8 tests
│   ├── test_claims.py         # 6 tests
│   └── test_admin.py          # 5 tests
├── pages/              # Page Object Model classes
│   ├── login_page.py
│   ├── register_page.py
│   ├── quote_page.py
│   ├── claims_page.py
│   └── admin_page.py
├── locators/           # All element selectors (one place)
├── utilities/          # Helpers, random data, screenshots
├── reports/            # Auto-generated HTML reports
├── screenshots/        # Pass/fail screenshots
├── conftest.py         # Pytest fixtures & browser config
└── pytest.ini          # Test configuration
```

### Run the Tests
```bash
cd Automation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
pytest
```
View the report: open `Automation/reports/test_report.html`

---

## 🔗 API Testing

📁 `Postman/SafeGuard_Insurance_API.postman_collection.json`

**12 API test cases** across 6 REST endpoints using Postman.

| Method | Endpoint | Positive | Negative |
|---|---|---|---|
| POST | `/api/register` | ✅ | ✅ |
| POST | `/api/login` | ✅ | ✅ |
| POST | `/api/quote` | ✅ | ✅ |
| GET | `/api/policies` | ✅ | — |
| POST | `/api/claim` | ✅ | ✅ |
| GET | `/api/claim/{id}` | ✅ | ✅ |

Each request includes **Postman test scripts** validating:
- Status codes (200, 201, 400, 401, 404, 409)
- Response time under 500ms
- JSON response body structure
- Error message presence on failures

---

## 🗄️ SQL Testing

📁 `SQLQueries/SQLQueries_SafeGuard.sql`
📁 `SQLQueries/SQLTesting_SafeGuard.docx`

**22 SQL validation queries** across all 4 database tables.

| Section | Queries | Purpose |
|---|---|---|
| Customers | SQL-001 to 006 | Registrations, duplicates, admin accounts |
| Policies | SQL-007 to 011 | Links, expired policies, $0 premiums |
| Claims | SQL-012 to 016 | Audit, status counts, integrity checks |
| Quotes | SQL-017 to 019 | Invalid ages, zero premiums |
| Cross-Table | SQL-020 to 022 | Customer summary, orphaned records |

**7 queries directly validate bug reports** — connecting database evidence to documented defects.

**Tool:** DB Browser for SQLite (free) — sqlitebrowser.org

---

## ⚙️ CI/CD Pipeline

📁 `.github/workflows/qa-pipeline.yml`

**GitHub Actions** pipeline that automatically runs on every push to master.

```
Push to master
      │
      ▼
Checkout Code
      │
      ▼
Setup Python + Install Dependencies
      │
      ▼
Start Flask App (background)
      │
      ▼
Verify App is Running (curl check)
      │
      ▼
Install Playwright + Chromium
      │
      ▼
Create Test User via API
      │
      ▼
Run 28 Playwright Tests
      │
      ▼
Upload HTML Report + Screenshots
      │
      ▼
Pipeline Complete ✅
```

View pipeline runs → **Actions tab** on this repo.

---

## 📁 Repository Structure

```
Insurance-Policy-QA-Project/
│
├── 📁 .github/workflows/    # GitHub Actions CI/CD pipeline
├── 📁 Application/          # Flask web app (system under test)
├── 📁 TestPlan/             # Test strategy & test plan (Word doc)
├── 📁 TestCases/            # 60+ manual test cases (Excel)
├── 📁 RTM/                  # Requirements Traceability Matrix
├── 📁 BugReports/           # 13 detailed bug reports (Word doc)
├── 📁 SQLQueries/           # 22 SQL validation queries
├── 📁 Postman/              # API test collection (JSON)
├── 📁 Automation/           # Playwright + Pytest framework
├── 📁 CI-CD/                # Pipeline documentation
├── 📁 AgileDocs/            # Jira sprint artifacts
└── 📄 README.md             # This file
```

---

## 🎯 Skills Demonstrated

| Category | Skills |
|---|---|
| **Manual Testing** | Test case design, RTM, boundary testing, negative testing |
| **Bug Reporting** | Severity/priority classification, root cause analysis, reproduction steps |
| **API Testing** | REST API validation, Postman collections, status code testing |
| **Automation** | Playwright, Pytest, Page Object Model, fixtures, screenshots |
| **Database** | SQL queries, data integrity checks, cross-table validation |
| **CI/CD** | GitHub Actions, automated pipeline, artifact publishing |
| **Agile** | Jira, sprint planning, backlog management, defect tracking |
| **Domain** | Insurance domain knowledge (policies, claims, premiums) |
| **Tools** | Git, GitHub, Postman, DB Browser, VS Code, Jira |

---

## 👤 About

**Sahil** — QA Analyst | Winnipeg, MB, Canada

Actively seeking QA Analyst / Associate QA / Software Tester roles.

📧 mayur.dalvi123@gmail.com | 🔗 https://www.linkedin.com/in/sahildalvi/

---

<div align="center">

⭐ If this project helped you, consider giving it a star!

</div>
