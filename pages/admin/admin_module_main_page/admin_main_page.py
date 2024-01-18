from pages.application_main_page import ApplicationMainPage
from playwright.sync_api import Page
from pages.components.table.table_actions import TableActions
from pages.components.dropdowns.dropdown import Dropdown


class AdminMainPage(ApplicationMainPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.table_actions = TableActions(page)
        self.dropdown = Dropdown(page)

    def add_user(self):
        add_button = self.page.get_by_role("button", name="Add")
        self.click_element(add_button)

    def fill_user_name(self):
        pass

    def choose_user_role(self):
        pass

    def type_employee_name(self):
        pass
