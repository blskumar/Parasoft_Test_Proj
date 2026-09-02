import pytest
import allure
from pages.login import LoginPage
from utils.login_data import invalid_login_cases, registered_users

@allure.feature("User Login")
@allure.story("Login with invalid credentials")
@pytest.mark.parametrize(
    "credentials",
    invalid_login_cases(),
    ids=lambda credentials: credentials["username"],
)
def test_login_with_invalid_credentials(page, base_url, credentials):
    login_page = LoginPage(page, base_url)

    login_page.open()
    login_page.login(credentials["username"], credentials["password"])

    login_page.assert_login_failed()

    login_page.assert_logged_in()