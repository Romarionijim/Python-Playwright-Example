from pages.orange_hr_base_page import OrangeHrBasePage
from playwright.sync_api import Page

from pages.page_components.dropdowns.dropdown import Dropdown
from pages.page_components.input_fields.input_fields import InputFields


class AdminCreationPage(OrangeHrBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.input_fields = InputFields(page)
        self.dropdown = Dropdown(page)

    def choose_user_role(self, user_role: str):
        self.dropdown.choose_item_from_dropdown('User Role', user_role)

    # def fill_employee_name
