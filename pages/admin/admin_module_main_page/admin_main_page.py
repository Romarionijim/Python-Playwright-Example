from pages.orange_hr_base_page import OrangeHrBasePage
from playwright.sync_api import Page
from pages.page_components.table.table_actions import TableActions
from pages.page_components.button.button import Button
from pages.page_components.dropdowns.dropdown import Dropdown
from pages.page_components.input_fields.input_fields import InputFields


class AdminMainPage(OrangeHrBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.table_actions = TableActions(page)
        self.dropdown = Dropdown(page)
        self.input_fields = InputFields(page)
        self.button = Button(page)
