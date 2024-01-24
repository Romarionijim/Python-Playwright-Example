from playwright.sync_api import Page, Locator

from pages.base_page import BasePage
from pages.orange_hr_base_page import OrangeHrBasePage
from typing import Union


class Dropdown(BasePage):
    __dropdown_select_locator = '[class="oxd-select-wrapper"]'
    __dropdown_list_items = '[class="oxd-select-text-input"]'
    __input_fields_wrapper = '[class="oxd-input-group oxd-input-field-bottom-space"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def __click_and_choose_from_dropdown_by_text(self, dropdown_locator: Union[str, Locator],
                                                 dropdown_list_locator: Union[str, Locator],
                                                 text: Union[str, list[str]]):
        """clicks on a dropdown - loops through a list of items and selects an item based on the provided text in the
        test - it clicks on the dropdown again and chooses another item if multi-selection is supported"""
        dropdown_element = self.page.locator(dropdown_locator)
        self.click_element(dropdown_element)
        provided_item_args = text if isinstance(text, list) else list(text)
        for i in range(len(provided_item_args)):
            item_text = provided_item_args[i]
            dropdown_items = self.page.locator(f'{dropdown_list_locator}:hast-text("{item_text}")').all()
            for item in dropdown_items:
                item_inner_text = item.inner_text()
                if text in dropdown_items and item_inner_text == text:
                    item.click()
                    break
            if i < len(provided_item_args) - 1:
                self.click_element(dropdown_element)

        raise ValueError(f'the item {text} was not found in the list')

    def choose_item_from_dropdown(self, dropdown_wrapper_text: str, item_text: str):
        dropdown_locator = self.page.locator(self.__input_fields_wrapper, has_text=dropdown_wrapper_text)
        select_locator = dropdown_locator.locator(self.__dropdown_select_locator)
        dropdown_item_list = select_locator.locator(self.__dropdown_list_items)
        self.__click_and_choose_from_dropdown_by_text(select_locator, dropdown_item_list, item_text)
