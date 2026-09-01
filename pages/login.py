from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("input[value='Log In']")
        self.login_error = page.locator("#rightPanel .error")

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def assert_logged_in(self) -> None:
        expect(self.page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

    def assert_login_error(self, expected_message: str) -> None:
        expect(self.login_error).to_contain_text(expected_message)
