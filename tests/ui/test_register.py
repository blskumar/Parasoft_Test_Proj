import json
from pathlib import Path

from pages.register import RegisterPage
from playwright.sync_api import expect


def test_register_user(page, base_url):
    register_page = RegisterPage(page, base_url)
    password = "Password123!"
    username = register_page.register_user(password=password)

    expect(page.get_by_text("Your account was created successfully")).to_be_visible()
    assert username.startswith("testuser_")

    credentials_path = Path(__file__).parents[2] / "data" / "users.json"
    credentials = []
    if credentials_path.exists():
        stored_credentials = json.loads(credentials_path.read_text(encoding="utf-8"))
        if isinstance(stored_credentials, dict):
            credentials = [
                {"username": stored_username, "password": stored_password}
                for stored_username, stored_password in stored_credentials.items()
            ]
        else:
            credentials = stored_credentials

    credentials.append({"username": username, "password": password})
    credentials_path.write_text(json.dumps(credentials, indent=2) + "\n", encoding="utf-8")