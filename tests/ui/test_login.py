import pytest

from pages.login import LoginPage
from utils.login_data import invalid_login_cases, registered_users


@pytest.mark.parametrize(
    "credentials",
    registered_users(),
    ids=lambda credentials: credentials["username"],
)
def test_login_with_valid_registered_user(page, base_url, credentials):
    login_page = LoginPage(page, base_url)

    login_page.open()
    login_page.login(credentials["username"], credentials["password"])

    login_page.assert_logged_in()


@pytest.mark.parametrize(
    "login_case",
    invalid_login_cases(),
    ids=lambda login_case: login_case["name"],
)
def test_login_rejects_invalid_and_edge_case_credentials(page, base_url, login_case):
    login_page = LoginPage(page, base_url)

    login_page.open()
    login_page.login(login_case["username"], login_case["password"])

    login_page.assert_login_error(login_case["expected_error"])
    assert not page.get_by_text("Accounts Overview", exact=True).is_visible()
