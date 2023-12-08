from pages.base_page import BasePage
from playwright.sync_api import Page, Locator
from app_enums.navigation_enums.urls.application_url import ApplicationUrl
from typing import Union
import logging
import os
from app_enums.navigation_enums.sidebar.sidebar_modules import SideBarModules
from app_enums.navigation_enums.menu.module_portlet_menu import ModulePortletMenu
from utils import properties
from utils.properties import UPLOAD_PATH

"""this class contains common reusable functions that are used throughout the tested application"""


class OrangeHrBasePage(BasePage):
    _table_container_locator = '.orangehrm-container'
    _sidebar_modules_locator = '.oxd-main-menu-item'
    _sidebar_expand_collapse_button_locator = '[class="oxd-icon-button oxd-main-menu-button"]'
    _dynamic_table_row_locator = f'{_table_container_locator} .oxd-table-card'
    _toastr_locator = '#oxd-toaster_1'
    _active_module_name_locator = '.oxd-topbar-header-breadcrumb'

    def __init__(self, page: Page):
        super().__init__(page)

    def load_application(self, app_url: ApplicationUrl):
        self.goto_website(app_url.value)

    def get_order_of_elements(self, locator: Union[str, Locator]) -> list:
        order_of_items: list = []
        element_list = self.page.locator(locator).all()
        for i in range(len(element_list)):
            element_inner_text = element_list[i].inner_text().strip()
            order_of_items.append(element_inner_text)
        return order_of_items

    def get_column_index_by_name(self, column_name: str) -> int:
        """this function retrieves the column index dynamically by name - hardcoded since the table locators are the
        same in every page of the application instead of repeatedly re-writing them in every page this method is called"""
        table_header_container = self.page.locator(
            f'{self._table_container_locator} .oxd-table-header.oxd-table-header')
        column_list = table_header_container.locator('[role="columnheader"]').all()
        for i in range(len(column_list)):
            if column_list[i].inner_text().strip() == column_name:
                return i

        raise Exception(f"the column {column_name} does not exist")

    def get_file_size(self, file_path: str) -> int:
        megabyte_size = (1024 ** 2)
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size
        file_size_megabytes = file_size / megabyte_size
        rounded_size = round(file_size_megabytes, 1)
        return rounded_size

    def get_file_extension(self, file_name: str) -> str:
        file_extension = file_name.split('.').pop()
        return file_extension

    def upload_file(self, file_name: str, upload_locator: str, path: str = properties.UPLOAD_PATH):
        file_path = f'{path}/{file_name}'
        file_size = self.get_file_size(file_path)
        logging.debug(f'the uploaded file size = {file_size}')
        file_extension = self.get_file_extension(file_name)
        logging.debug(f'the uploaded file extension = {file_extension}')
        upload_button = self.page.locator(upload_locator)
        upload_button.set_input_files(file_path)

    def click_and_choose_from_dropdown_by_text(self, dropdown_locator: Union[str, Locator], dropdown_list_locator: str,
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

    def click_on_specific_button_from_table(self, row_text: str,
                                            button_locator: Union[str, Locator]):
        table_row = self.page.locator(f'{self._table_container_locator} .oxd-table-card', has_text=row_text)
        button_element = table_row.locator(button_locator)
        self.click_element(button_element)

    def get_cell_value_inner_text(self, row_text: str, column_name: str) -> str:
        table_row = self.page.locator(f'{self._table_container_locator} .oxd-table-card', has_text=row_text)
        table_column = self.get_column_index_by_name(column_name)
        table_cell = table_row.locator('[role=cell]').nth(table_column)
        cell_inner_text = table_cell.inner_text()
        return cell_inner_text

    def get_order_of_cell_values(self, column_name: str) -> list:
        cell_value_order: list = []
        table = self.page.locator(f'{self._table_container_locator} .oxd-table-card').all()
        table_column = self.get_column_index_by_name(column_name)
        for row in table:
            row_cell = row.locator('[role=cell]').nth(table_column)
            cell_inner_text = row_cell.inner_text().strip()
            cell_value_order.append(cell_inner_text)
        return cell_value_order

    def count_items(self, list_locator: Union[str, Locator]) -> int:
        return self.count_elements(list_locator)

    def navigate_to_module(self, module: SideBarModules):
        side_bar_modules = self.page.locator(self._sidebar_modules_locator, has_text=module.value)
        self.click_element(side_bar_modules)

    def get_side_bar_state(self):
        """returns the state of the sidebar if it is expanded or collapsed"""
        side_bar_button = self.page.locator(self._sidebar_expand_collapse_button_locator)
        button_attribute = side_bar_button.locator('i').get_attribute('class')
        return 'expanded' if "left" in button_attribute else 'collapsed'

    def get_input_fields_values(self, input_fields_locator: Union[str, Locator]):
        """loops through each input field then returns the input fields input values or inner texts based on the
        element tag"""
        input_fields_list: list = []
        input_fields = self.page.locator(input_fields_locator).all()
        for i in range(len(input_fields)):
            input_field = input_fields[i]
            if input_field.evaluate("el => el.tagName.toLowerCase() == 'input'"):
                input_fields_list.append(input_field.input_value())
            else:
                input_fields_list.append(input_field.inner_text())

        return input_fields_list

    def choose_dropdown_menu(self, menu_list_locator: Union[str, Locator], portlet_menu: ModulePortletMenu,
                             dropdown_list_locator: str, item_name: str):
        """click and choose a dropdown meu and choose an item from the dropdown list"""
        portlet_menu = self.page.locator(menu_list_locator, has_text=portlet_menu.value)
        self.click_element(portlet_menu)
        dropdown_options = self.page.locator(f'{dropdown_list_locator} li').all()
        for item in dropdown_options:
            item_inner_text = item.inner_text()
            if item_inner_text.strip() == item_name:
                item.click()
                break
        raise ValueError(f'item {item_name} does not exist in the dropdown list')

    def check_if_item_is_in_list(self, list_locator: Union[str, Locator], item_name: str) -> bool:
        item_list: list = []
        item_list_locator = self.page.locator(list_locator).all()
        for item in item_list_locator:
            item_inner_text = item.inner_text()
            item_list.append(item_inner_text)
        return item_name in item_list

    def download_file(self, download_button_locator: Union[str, Locator], path: str = properties.DOWNLOAD_PATH):
        with self.page.expect_download() as download_info:
            self.click_element(download_button_locator)
            download = download_info.value
            file_name = download.suggested_filename
            logging.info(f'downloaded file: {file_name}')
            download.save_as(f'{path}/{file_name}')
            return file_name

    def get_toastr_notification_caption(self):
        """gets the toastr notification confirmation text after performing a type of action such as deletion of a row"""
        toastr = self.page.locator(self._toastr_locator)
        toastr_visibility = toastr.is_visible()
        if toastr_visibility:
            toastr_inner_text = toastr.inner_text()
            return toastr_inner_text
        raise Exception("the toastr was not shown")

    def get_all_row_cell_values(self, row_text: str, expected_values: list[str]):
        """get all row's inner text and validate that the expected value list exist on that specific row"""
        table_row = self.page.locator(self._dynamic_table_row_locator, has_text=row_text)
        row_inner_text = table_row.inner_text().strip()
        for value in expected_values:
            if value in row_inner_text:
                return True
        raise ValueError(f"one or more cell values {expected_values} were not found on table row")

    def count_client_side_validation_errors_on_empty_fields(self, input_fields: Union[str, Locator],
                                                            validation_error_locator: Union[str, Locator]):
        """returns all inner texts of all validation errors  if all fields are emtpy - else return the index of the
        specific inputs that remained empty that contains the validation error after submitting """
        input_values = self.get_input_fields_values(input_fields)
        validation_error_element = self.page.locator(validation_error_locator)
        validation_error_count = validation_error_element.count()
        if all(len(input_element) == 0 for input_element in input_values):
            all_validation_error_text = validation_error_element.all_inner_texts()
            return validation_error_count, all_validation_error_text
        else:
            empty_fields_indices = [i for i, element in enumerate(input_values) if len(element) == 0]
            return validation_error_count, empty_fields_indices

    def count_client_side_validation_errors(self, validation_error_locator: Union[str, Locator],
                                            field_with_error_locator: Union[str, Locator] = None,
                                            error_name: str = None):
        """returns the index of each field that contains an error to validate the correct field contains an error"""
        client_side_validation_locator = self.page.locator(validation_error_locator)
        client_side_validation_count = client_side_validation_locator.count()
        if not client_side_validation_count:
            raise Exception(
                "there are no validation errors displayed or the locator of the validation error does not exist")
        field_with_error_indices_list: list = []
        field_with_error_inner_text_list: list = []
        input_fields_wrapper_locator = self.page.locator(field_with_error_locator).all()
        for i in range(len(input_fields_wrapper_locator)):
            field_inner_text = input_fields_wrapper_locator[i].inner_text()
            if error_name in field_inner_text:
                field_with_error_indices_list.append(i)
                field_with_error_inner_text_list.append(field_inner_text)
        return client_side_validation_count, field_with_error_indices_list, field_with_error_inner_text_list

    def get_current_active_module_name(self):
        return self.page.locator(self._active_module_name_locator).inner_text().strip()
