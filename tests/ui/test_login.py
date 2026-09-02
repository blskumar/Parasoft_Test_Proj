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

?