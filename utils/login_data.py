from pathlib import Path
from typing import Any

from utils.data_loader import load_json


PROJECT_ROOT = Path(__file__).parents[1]
USERS_PATH = PROJECT_ROOT / "data" / "users.json"
LOGIN_CASES_PATH = PROJECT_ROOT / "data" / "login_cases.json"


def registered_users() -> list[dict[str, str]]:
    users: Any = load_json(USERS_PATH)
    if isinstance(users, dict):
        return [
            {"username": username, "password": password}
            for username, password in users.items()
        ]
    if not isinstance(users, list):
        raise ValueError("users.json must contain a list or an object")
    return users


def invalid_login_cases() -> list[dict[str, str]]:
    cases = load_json(LOGIN_CASES_PATH)
    if not isinstance(cases, list):
        raise ValueError("login_cases.json must contain a list")
    return cases
