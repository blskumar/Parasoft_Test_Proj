import json
from pathlib import Path

from playwright.sync_api import sync_playwright, expect

from pages.register import RegisterPage

BASE_URL = "https://parabank.parasoft.com/parabank/index.htm"
OUTPUT_PATH = Path(__file__).resolve().parent / "data" / "users.json"


def register_new_user(password: str = "Password123!") -> dict[str, str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")

        register_link = page.get_by_role("link", name="Register")
        expect(register_link).to_be_visible(timeout=15000)
        register_link.click()
        expect(page.get_by_text("Signing up is easy")).to_be_visible(timeout=15000)

        reg = RegisterPage(page, BASE_URL)
        username = reg.register_user(password=password)
        context.close()
        browser.close()
        return {"username": username, "password": password}


if __name__ == "__main__":
    users = [register_new_user() for _ in range(5)]
    OUTPUT_PATH.write_text(json.dumps(users, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(users)} valid users and saved to {OUTPUT_PATH}")
    for user in users:
        print(f"- {user['username']} / {user['password']}")
