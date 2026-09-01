import os
from pathlib import Path

import pytest
from playwright.sync_api import Playwright


PROJECT_ROOT = Path(__file__).resolve().parent


def _load_dotenv_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        values[key] = value.strip('"').strip("'")
    return values


@pytest.fixture(scope="session")
def base_url() -> str:
    env_values = _load_dotenv_values(PROJECT_ROOT / ".env")
    return (
        os.getenv("BASE_URL")
        or os.getenv("base_url")
        or env_values.get("BASE_URL")
        or env_values.get("base_url")
        or ""
    )


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture
def page(browser, base_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url, wait_until="domcontentloaded")
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="session", autouse=True)
def api_request(playwright: Playwright):
    request = playwright.request.new_context(
        base_url="https://api.restful-api.dev/",
        extra_http_headers={"Content-Type": "application/json", "x-api-key": "2444ef21-be1f-4a38-8a97-0c7ffb2c6c8b"},
    )
    yield request
    request.dispose()


@pytest.fixture(scope="session", autouse=True)
def api_request_without_content_type(playwright: Playwright):
    request = playwright.request.new_context(
        base_url="https://api.restful-api.dev/",
        extra_http_headers={"x-api-key": "2444ef21-be1f-4a38-8a97-0c7ffb2c6c8b"},
    )
    yield request
    request.dispose()