from pages.orange_hr_base_page import OrangeHrBasePage
from playwright.sync_api import Page
from typing import Union, Optional
from playwright.sync_api import Locator


class TableActions(OrangeHrBasePage):
    __checkbox_wrapper_locator = '.oxd-checkbox-wrapper input'
    __delete_selected_locator = '[class="oxd-button oxd-button--medium oxd-button--label-danger orangehrm-horizontal-margin"]'
    __records_found_locator = '[class="orangehrm-horizontal-padding orangehrm-vertical-padding"] .oxd-text'
    __download_button_table_locator = '[class="oxd-icon bi-download"]'
    __delete_button_table_locator = '[class="oxd-icon bi-trash"]'
    __edit_button_table_locator = '[class="oxd-icon bi-pencil-fill"]'
    __eye_button_table_locator = '[class="oxd-icon bi-eye-fill"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def count_table_items(self) -> int:
        table_items = self.page.locator(f'{self._table_container_locator} .oxd-table-card')
        return self.count_items(table_items)

    def select_all_table_items(self, delete_selected: Optional[bool] = None):
        """click on the first checkbox to select all checkbox and validate all checkboxes are checked - it has the
        option to delete all rows"""
        checkbox_list = self.page.locator(self.__checkbox_wrapper_locator).all()
        select_all_first_checkbox = checkbox_list[0]
        self.click_element(select_all_first_checkbox)
        checkbox_list_state: list = []
        for checkbox in checkbox_list:
            checkbox_list_state.append(self.get_checkbox_state(checkbox))
        all_checked = all(checkbox_list_state)
        if all_checked and delete_selected is not None:
            delete_selected_button = self.page.locator(self.__delete_selected_locator)
            self.click_element(delete_selected_button)
        return checkbox_list_state

    def delete_selected_row_item(self, row_text: str):
        """delete a specific row that contains a specific text then return if the row got removed from the row list"""
        table_row = self.page.locator(self._dynamic_table_row_locator, has_text=row_text)
        row_checkbox = table_row.locator(self.__checkbox_wrapper_locator)
        self.click_element(row_checkbox)
        delete_selected_button = self.page.locator(self.__delete_selected_locator)
        delete_selected_button_visibility = delete_selected_button.is_visible()
        if delete_selected_button_visibility:
            self.click_element(delete_selected_button)
            return self.check_if_item_is_in_list(self._dynamic_table_row_locator, row_text)

    def get_records_found(self) -> str:
        records_found_locator = self.page.locator(self.__records_found_locator)
        records_found_inner_text = records_found_locator.inner_text()
        return records_found_inner_text

    def download_file_from_table_row(self, row_text: str):
        table_row = self.page.locator(self._dynamic_table_row_locator, has_text=row_text)
        download_button = table_row.locator(self.__download_button_table_locator)
        return self.download_file(download_button)

    def check_if_item_row_exist(self, row_text: str):
        return self.check_if_item_is_in_list(self._dynamic_table_row_locator, row_text)

    def get_table_cell_value(self, row_text: str, column_name: str):
        return self.get_cell_value_inner_text(row_text, column_name)

    def modify_table_row_details(self):
        pass

    def get_all_table_cell_values(self, row_text: str, expected_values: list[str]):
        return self.get_all_row_cell_values(row_text, expected_values)
