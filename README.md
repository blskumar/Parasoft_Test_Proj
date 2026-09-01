# Parasoft Test Project

This project contains a Playwright + Pytest UI automation suite for the ParaBank demo application. It covers user login validation, invalid login scenarios, and registration flow.

## Overview

The project automates end-to-end browser interactions against:

- https://parabank.parasoft.com/parabank/index.htm

It validates:

- successful login for registered users
- failed login for invalid and edge-case credentials
- successful new user registration
- persistence of generated users for later login tests

## Project Structure

```text
Parasoft_Test_Proj/
├── conftest.py              # Pytest fixtures and browser setup
├── generate_users.py        # Generates sample users and writes them to data/users.json
├── requirements.txt         # Python dependencies
├── data/
│   ├── login_cases.json     # Invalid login test cases
│   └── users.json           # Registered user data
├── pages/
│   ├── login.py             # Login page actions and assertions
│   └── register.py          # Registration page actions
├── tests/
│   └── ui/
│       ├── test_login.py    # Login tests
│       └── test_register.py # Registration test
├── utils/
│   ├── data_loader.py       # JSON loader helper
│   └── login_data.py        # User data access helpers
├── reports/
│   └── screenshots/         # Screenshots captured during test execution
├── .venv/                   # Local virtual environment (if present)
└── README.md                # Project documentation
```

## Prerequisites

- Python 3.10+
- pip
- A browser supported by Playwright

## Setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browser binaries:

```bash
python -m playwright install
```

## Running the Tests

Run the full UI test suite:

```bash
pytest
```

Run only login tests:

```bash
pytest tests/ui/test_login.py
```

Run only registration tests:

```bash
pytest tests/ui/test_register.py
```

## Custom Configuration

The test suite supports a custom base URL via environment variables:

```bash
$env:BASE_URL = "https://parabank.parasoft.com/parabank/index.htm"
pytest
```

You can also configure browser behavior:

```bash
$env:PLAYWRIGHT_HEADLESS = "true"
$env:PLAYWRIGHT_SLOW_MO = "200"
pytest
```

## Test Data

- `data/login_cases.json` contains invalid login scenarios and expected error messages.
- `data/users.json` stores generated or known user credentials used by login tests.
- `generate_users.py` can create additional test users automatically.

## Notes

- Screenshots are saved under `reports/screenshots/` when a test passes and a page exists.
- The project uses pytest fixtures for browser lifecycle management and screenshot capture.

## License

This project is intended for test automation and learning purposes within the repository context.
