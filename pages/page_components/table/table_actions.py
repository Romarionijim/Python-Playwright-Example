from pages.orange_hr_base_page import OrangeHrBasePage
from pages.base_page import BasePage
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
    __deletion_dialog_locator = '[role="document"]'
    __table_container_locator = '.orangehrm-container'
    __dynamic_table_row_locator = f'{__table_container_locator} .oxd-table-card'

    def __init__(self, page: Page):
        super().__init__(page)

    def count_table_items(self) -> int:
        table_items = self.page.locator(f'{self.__table_container_locator} .oxd-table-card')
        return self.count_items(table_items)

    def click_on_specific_button_from_table(self, row_text: str,
                                            button_locator: Union[str, Locator]):
        table_row = self.page.locator(f'{self.__table_container_locator} .oxd-table-card', has_text=row_text)
        button_element = table_row.locator(button_locator)
        self.click_element(button_element)

    def select_all_table_items(self, delete_selected: Optional[bool] = None):
        """click on the first checkbox to select all checkbox and validate all checkboxes are checked - it has the
        option to delete all rows"""
        checkbox_list = self.page.locator(self.__checkbox_wrapper_locator).all()
        select_all_first_checkbox = checkbox_list[0]
        self.click_element(select_all_first_checkbox)
        checkbox_list_state: list = []
        for checkbox in checkbox_list:
            check_box_state = self.get_checkbox_state(checkbox)
            checkbox_list_state.append(check_box_state)
        all_checked = all(checkbox_list_state)
        return all_checked

    def handle_dialog_prompt(self, dialog_option: str):
        """handle dialog that is prompted when performing an action such as deleting an item from a table by
        confirming or canceling the prompt dialog"""
        dialog_prompt = self.page.locator(self.__deletion_dialog_locator)
        dialog_inner_text = dialog_prompt.inner_text().strip()
        dialog_button_option = dialog_prompt.locator('button', has_text=dialog_option)
        self.click_element(dialog_button_option)
        return dialog_inner_text

    def delete_all_items_from_table(self):
        """deletes all the items that exist on the table - the ADMIN and PIM modules must have at least one item/row
        in the table and therefore not all rows could be deleted in these specific modules"""
        row_count = self.count_table_items()
        records_found = self.get_records_found()
        while True:
            all_checkboxes_are_checked = self.select_all_table_items()
            if all_checkboxes_are_checked:
                delete_selected_button = self.page.locator(self.__delete_selected_locator)
                self.click_element(delete_selected_button)
                self.handle_dialog_prompt('Yes, Delete')
                current_active_module = self.get_current_active_module_name()
                if (
                        current_active_module != 'Admin\nUser Management' and current_active_module != 'PIM') and row_count == 0:
                    break
                elif (
                        current_active_module == 'Admin\nUser Management' or current_active_module == 'PIM') and row_count == 1:
                    break
        return row_count, records_found

    def delete_last_item_and_validate_error_message(self, row_text: str):
        """this method tries to delete the last item in the Admin or PIM module and get the toastr
        error since the last item cannot be deleted in these modules"""
        current_active_module = self.get_current_active_module_name()
        row_count = self.count_table_items()
        if (current_active_module == 'Admin\nUser Management' or current_active_module == 'PIM') and row_count == 1:
            self.click_on_specific_button_from_table(row_text, self.__delete_button_table_locator)
            error_popup = self.get_toastr_notification_caption()
            return error_popup

    def delete_selected_row_item(self, row_text: str):
        """delete a specific row that contains a specific text then return if the row got removed from the row list"""
        self.select_specific_table_row(row_text)
        delete_selected_button = self.page.locator(self.__delete_selected_locator)
        delete_selected_button_visibility = delete_selected_button.is_visible()
        if delete_selected_button_visibility:
            self.click_element(delete_selected_button)
            return self.check_if_item_is_in_list(self.__dynamic_table_row_locator, row_text)

    def get_records_found(self) -> str:
        records_found_locator = self.page.locator(self.__records_found_locator)
        records_found_inner_text = records_found_locator.inner_text()
        return records_found_inner_text

    def download_file_from_table_row(self, row_text: str):
        table_row = self.page.locator(self.__dynamic_table_row_locator, has_text=row_text)
        download_button = table_row.locator(self.__download_button_table_locator)
        return self.download_file(download_button)

    def check_if_item_row_exist(self, row_text: str):
        return self.check_if_item_is_in_list(self.__dynamic_table_row_locator, row_text)

    def get_cell_value_inner_text(self, row_text: str, column_name: str) -> str:
        table_row = self.page.locator(f'{self.__table_container_locator} .oxd-table-card', has_text=row_text)
        table_column = self.get_column_index_by_name(column_name)
        table_cell = table_row.locator('[role=cell]').nth(table_column)
        cell_inner_text = table_cell.inner_text()
        return cell_inner_text

    def get_table_cell_value(self, row_text: str, column_name: str):
        return self.get_cell_value_inner_text(row_text, column_name)

    def modify_table_row_details(self):
        """this function only clicks on the modify button from the table"""
        self.click_element(self.__edit_button_table_locator)

    def get_all_table_cell_values(self, row_text: str, expected_values: list[str]):
        return self.get_all_row_cell_values(row_text, expected_values)

    def select_specific_table_row(self, row_text: str):
        """selects the checkbox on the specific row that contains a specific text"""
        table_row = self.page.locator(self.__dynamic_table_row_locator, has_text=row_text)
        row_checkbox = table_row.locator(self.__checkbox_wrapper_locator)
        self.click_element(row_checkbox)

    def get_column_index_by_name(self, column_name: str) -> int:
        """this function retrieves the column index dynamically by name - hardcoded since the table locators are the
        same in every page of the application instead of repeatedly re-writing them in every page this method is called"""
        table_header_container = self.page.locator(
            f'{self.__table_container_locator} .oxd-table-header')
        column_list = table_header_container.locator('[role="columnheader"]').all()
        for i in range(len(column_list)):
            if column_list[i].inner_text().strip() == column_name:
                return i
        raise Exception(f"the column {column_name} does not exist in the column list")

    def get_order_of_cell_values(self, column_name: str) -> list:
        """get the order of all cell values under a specific column in a table"""
        cell_value_order: list = []
        table = self.page.locator(f'{self.__table_container_locator} .oxd-table-card').all()
        table_column = self.get_column_index_by_name(column_name)
        for row in table:
            row_cell = row.locator('[role=cell]').nth(table_column)
            cell_inner_text = row_cell.inner_text().strip()
            cell_value_order.append(cell_inner_text)
        return cell_value_order

    def get_all_row_cell_values(self, row_text: str, expected_values: list[str]):
        """returns if the expected values exist on a specific row else it raises an error"""
        table_row = self.page.locator(self.__dynamic_table_row_locator, has_text=row_text)
        row_inner_text = table_row.inner_text().strip()
        for value in expected_values:
            if value not in row_inner_text:
                raise ValueError(f"one or more cell values {expected_values} were not found on table row")
        return True
