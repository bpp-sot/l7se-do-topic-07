# Green Lights, Red Flags

**Topic 7 Breakout Exercise · Designing and Building Secure Software**  
Level 7 Software Engineering · BPP University

---

## Scenario

Hartley University's IT department recently deployed **StudyTrack**, a lightweight Flask-based internal portal that allows academic registry staff to search student records by surname. The application was promoted to production three weeks ago after successfully passing all automated tests in the CI/CD pipeline.

A registry administrator has since raised a support ticket reporting that searches for students with apostrophes in their surname (e.g., O'Brien, O'Sullivan) either return a **500 Internal Server Error** or produce no results — despite those students being present in the database.

The development team has logged a bug report, proposed a diagnosis, and confirmed that the full automated test suite continues to pass with no failures. Your group has been asked to investigate.

---

## Artefacts

### Artefact 1 — Source Code (`app.py`)

The relevant search route is in `app.py`. This is the code currently running in production.

### Artefact 2 — Bug Report (BUG-2047)

```
Bug ID:       BUG-2047
Title:        Search fails for surnames containing apostrophes
Reported by:  Registry Admin (J. Whitfield)
Date raised:  14 March 2026
Severity:     Medium
Status:       Under Investigation

Description:
  Searching for students with apostrophe characters in their surname
  (e.g., O'Brien, O'Connor) returns either a 500 Internal Server Error
  or no results, despite those students existing in the database.

Steps to reproduce:
  1. Navigate to /students/search?surname=O'Brien
  2. Observe: 500 Internal Server Error returned

  Expected:  Matching student records returned as JSON
  Actual:    500 Internal Server Error

Developer note (L. Patel, 15 March 2026):
  Most likely a character encoding issue between Flask's URL handling
  and the SQLite database layer. Will investigate UTF-8 collation
  settings. All automated tests pass — no regression detected.
```

### Artefact 3 — Automated Test Suite (`tests/test_search.py`)

The test suite currently reports **all 4 tests passing** with no failures. You can verify this yourself by running the tests locally (see [Getting Started](#getting-started) below).

---

## Tasks

Work through the following tasks as a group. Be prepared to share your findings in the report-back discussion.

**Task 1**

The developer attributes the apostrophe error to a character encoding issue between Flask's URL handling and the SQLite database layer. Do you agree with this diagnosis? What is the actual root cause of the error, and where precisely does it originate in the code?

**Task 2**

The automated test suite passes with no failures, yet a significant vulnerability is present. Why do the tests fail to detect it? What does this tell us about the limitations of test coverage as a security assurance mechanism?

**Task 3**

An attacker discovers this endpoint. What could they realistically do with it? Sketch out a plausible attack scenario — consider what data could be exposed, exfiltrated, or manipulated, and how. Frame your thinking as responsible disclosure: focus on understanding the threat, not enabling it.

**Task 4**

Rewrite the vulnerable `search_students` function in `app.py` to eliminate the vulnerability. Be prepared to explain precisely why your fix works at a technical level — what does the corrected approach prevent the database engine from doing?

**Task 5**

Write one additional test case that *would have* detected this vulnerability before the application reached production. What input would it use, and what would it assert? Could the same test be adapted to cover other injection vectors?

---

## Report-Back Prompt

After working through the tasks, be ready to address this question in your group's two-minute report-back:

> *"Fixing this single line of code addresses the immediate vulnerability — but what **single change to the development process** would most have prevented it from reaching production in the first place?"*

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- `pip`

### Installation

```bash
# Clone the repository, then:
cd l7se-do-topic-07

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the tests

```bash
pytest -v
```

All four tests should pass. This is expected and is part of the exercise.

### Running the app locally (optional)

If you want to interact with the application in a browser or via `curl`:

```bash
# Seed the local database first
python setup_db.py

# Start the Flask development server
python app.py
```

The app will be available at `http://127.0.0.1:5000`. Try:

```
http://127.0.0.1:5000/students/search?surname=Smith
http://127.0.0.1:5000/students/search?surname=O'Brien
```

---

## Repository Structure

```
studytrack-exercise/
├── app.py              # Flask application (production code under review)
├── setup_db.py         # Seeds a local SQLite database for manual testing
├── requirements.txt
├── .gitignore
├── README.md           # This file
└── tests/
    ├── conftest.py     # Pytest fixtures (test database setup)
    └── test_search.py  # Automated test suite
```

---

*Designing and Building Secure Software · Level 7 · BPP University · Internal Teaching Material*
