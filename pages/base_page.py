from playwright.sync_api import Page, Locator
from typing import Union
from utils.custom_exceptions.custom_exceptions import ElementNotClickableError
from abc import ABC

"""abstract base class for common reusable base functions mainly keyboard and mouse actions"""


class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page

    def __get_element_type(self, locator: Union[str, Locator]) -> Union[str, Locator]:
        if isinstance(locator, str):
            return self.page.locator(locator)
        elif isinstance(locator, Locator):
            return locator
        else:
            raise TypeError(f"the locator {locator} must be of type string or Locator")

    def goto_website(self, url: str):
        self.page.goto(url)

    def click_element(self, locator: Union[str, Locator]):
        try:
            element = self.__get_element_type(locator)
            element.click(force=True)
        except Exception as error:
            raise ElementNotClickableError(f'the element: {locator} is not clickable: {error}')

    def fill_text(self, locator: Union[str, Locator], text: str):
        element = self.__get_element_type(locator)
        self.click_element(element)
        element.fill(text)

    def hover_element(self, locator: Union[str, Locator]):
        element = self.__get_element_type(locator)
        element.hover()

    def drag_and_drop(self, drag_locator: str, target_locator: Locator):
        drag_element = self.__get_element_type(drag_locator)
        target_element = self.__get_element_type(target_locator)
        drag_element.drag_to(target_element)

    def change_checkbox_state(self, locator: Union[str, Locator]):
        element = self.__get_element_type(locator)
        is_checked = self.get_checkbox_state(element)
        if not is_checked:
            element.check()
        else:
            element.uncheck()

    def change_radio_button_state(self, label: str):
        element = self.page.get_by_label(label)
        is_radio_checked = self.get_checkbox_state(element)
        if not is_radio_checked:
            element.check()
        else:
            element.uncheck()

    def get_current_url(self) -> str:
        url = self.page.url
        return url

    def select_option(self, select_locator: Union[str, Locator], expected_value: str, label: str = None,
                      value: str = None):
        """selects an option based on value, label or by passing the value directly without specifying a value or a
        label attribute"""
        try:
            element = self.__get_element_type(select_locator)
            if label is not None:
                element.select_option(label=expected_value)
            elif value is not None:
                element.select_option(value=expected_value)
            else:
                element.select_option(expected_value)
        except Exception as error:
            raise ValueError(f'none of the conditions were satisfied in the select option method: {error}')

    def count_elements(self, elements_locator: Union[str, Locator]) -> int:
        element_list = self.__get_element_type(elements_locator)
        element_list_count = element_list.count()
        return element_list_count

    def get_checkbox_state(self, checkbox_locator: Union[str, Locator]) -> bool:
        """applies to checkboxes and radio buttons - returns a boolean to check if checkbox/radio is checked or not"""
        checkbox = self.__get_element_type(checkbox_locator)
        return checkbox.is_checked()

    def wait_for_visibility_of_element(self, locator: Union[str, Locator]) -> None:
        element = self.__get_element_type(locator)
        element.wait_for(state='visible')

    def wait_for_invisibility_of_element(self, locator: Union[str, Locator]) -> None:
        element = self.__get_element_type(locator)
        element.wait_for(state='hidden')
