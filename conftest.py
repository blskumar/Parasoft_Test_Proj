import base64
import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import Playwright


SCREENSHOT_DIR = Path(__file__).parent / "reports" / "screenshots"


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://parabank.parasoft.com/parabank/index.htm")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.passed or "page" not in item.funcargs:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    filename = re.sub(r"[^A-Za-z0-9_.-]+", "_", report.nodeid) + ".png"
    screenshot_path = SCREENSHOT_DIR / filename
    item.funcargs["page"].screenshot(path=str(screenshot_path), full_page=True)
    try:
        from pytest_html import extras

        report.extras = getattr(report, "extras", [])
        image_data = base64.b64encode(screenshot_path.read_bytes()).decode("ascii")
        report.extras.append(extras.image(image_data, mime_type="image/png"))
    except ImportError:
        pass


@pytest.fixture(scope="session")
def browser(playwright, browser_type_launch_args):
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() != "false"
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "500"))
    launch_options = {**browser_type_launch_args, "headless": headless}
    launch_options.setdefault("slow_mo", slow_mo)
    browser = playwright.chromium.launch(**launch_options)
    yield browser
    browser.close()


@pytest.fixture
def browser_context(browser, base_url):
    context = browser.new_context(base_url=base_url)
    yield context
    context.close()


@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session", autouse=True)
def api_request(playwright:Playwright):
    request = playwright.request.new_context(
        base_url="https://parabank.parasoft.com/parabank/index.htm",
        extra_http_headers={"Content-Type": "application/json", "x-api-key": "2444ef21-be1f-4a38-8a97-0c7ffb2c6c8b"}
    )
    yield request
    request.dispose()
    
# @pytest.fixture(scope="usersession", autouse=True)
# def api_request_without_content_type(playwright:Playwright):
#     request = playwright.request.new_context(
#         base_url="https://api.restful-api.dev/",
#         extra_http_headers={"x-api-key": "2444ef21-be1f-4a38-8a97-0c7ffb2c6c8b"}
#     )
#     yield request
#     request.dispose()