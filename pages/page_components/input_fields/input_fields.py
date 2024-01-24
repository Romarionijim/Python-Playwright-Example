from playwright.sync_api import Page
from pages.base_page import BasePage


class InputFields(BasePage):
    __input_fields_wrapper = '.oxd-grid-item'

    def __init__(self, page: Page):
        super().__init__(page)

    def fill_input_field(self, input_field_wrapper_text: str, value: str):
        input_field_wrapper = self.page.locator(self.__input_fields_wrapper, has_text=input_field_wrapper_text)
        input_field = input_field_wrapper.locator('input')
        self.fill_text(input_field, value)