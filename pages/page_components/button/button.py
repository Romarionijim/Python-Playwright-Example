from pages.base_page import BasePage
from playwright.sync_api import Page


class Button(BasePage):

    def __click_button(self, button_text: str):
        """generic function that clicks on a specific button with the 'button' tag element that contains a specific text """
        button_locator = self.page.locator('button', has_text=button_text)
        self.click_element(button_locator)

    def click_add(self):
        self.__click_button('Add')

    def click_reset(self):
        self.__click_button('Reset')

    def click_search(self):
        self.__click_button('Search')
