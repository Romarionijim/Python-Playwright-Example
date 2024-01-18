from playwright.sync_api import Page, Locator
from typing import Union
from pages.application_main_page import BasePage


class CheckBoxes():
    def __init__(self, page: Page):
        self.page = page

    def change_checkbox_state(self, checkbox_locator: Locator):
        if not checkbox_locator.is_checked():
            checkbox_locator.check()
        else:
            checkbox_locator.uncheck()

    def get_checkbox_state(self, checkbox_locator: Locator):
        return checkbox_locator.is_checked()
