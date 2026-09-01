from uuid import uuid4
from secrets import randbelow

from playwright.sync_api import Page, expect


class RegisterPage:
	def __init__(self, page: Page, base_url: str):
		self.page = page
		self.base_url = base_url

	def open_registration(self) -> None:
		self.page.goto(self.base_url, wait_until="domcontentloaded")
		self.page.get_by_role("link", name="Register").click()
		# Verify that the registration page is loaded
		expect(self.page.get_by_text("Signing up is easy")).to_be_visible()

	def register_user(
		self,
		first_name: str = "Test",
		last_name: str = "User",
		address: str = "1 Main Street",
		city: str = "Boston",
		state: str = "MA",
		zip_code: str = "02108",
		phone: str = "6175550100",
		ssn: str | None = None,
		password: str = "Password123!",
	) -> str:
		self.open_registration()
		username = f"testuser_{uuid4().hex[:10]}"
		ssn = ssn or str(randbelow(900_000_000) + 100_000_000)
		self.page.locator("//tr[td[contains(., 'First Name:')]]//input[@type='text']").fill(first_name)
		# self.page.get_by_label("First Name").fill(first_name)
		self.page.locator("//tr[td[contains(., 'Last Name:')]]//input[@type='text']").fill(last_name)
		# self.page.get_by_label("Last Name").fill(last_name)
		self.page.locator("//tr[td[contains(., 'Address:')]]//input[@type='text']").fill(address)
		# self.page.get_by_label("Address").fill(address)
		self.page.locator("//tr[td[contains(., 'City:')]]//input[@type='text']").fill(city)
		# self.page.get_by_label("City").fill(city)
		self.page.locator("//tr[td[contains(., 'State:')]]//input[@type='text']").fill(state)
		# self.page.get_by_label("State").fill(state)
		self.page.locator("//tr[td[contains(., 'Zip Code:')]]//input[@type='text']").fill(zip_code)
		# self.page.get_by_label("Zip Code").fill(zip_code)
		self.page.locator("//tr[td[contains(., 'Phone #:')]]//input[@type='text']").fill(phone)
		# self.page.get_by_label("Phone #").fill(phone)
		self.page.locator("//tr[td[contains(., 'SSN:')]]//input[@type='text']").fill(ssn)
		# self.page.get_by_label("SSN").fill(ssn)
		self.page.locator("//tr[td[contains(., 'Username:')]]//input[@type='text']").fill(username)
		# self.page.get_by_label("Username").fill(username)
		self.page.locator("//tr[td[contains(., 'Password:')]]//input[@type='password']").fill(password)
		# self.page.get_by_label("Password").fill(password)
		self.page.locator("//tr[td[contains(., 'Confirm:')]]//input[@type='password']").fill(password)
		# self.page.get_by_label("Confirm").fill(password)
		self.page.locator("//input[@value='Register']").click()
		return username


