from pages.application_main_page import ApplicationMainPage
from playwright.sync_api import Page, Locator
import os
from dotenv import load_dotenv
import logging

load_dotenv()


class LoginPage(ApplicationMainPage):
    __username_locator = '[name="username"]'
    __password_locator = '[name="password"]'
    __login_button_locator = '.orangehrm-login-button'
    __forgot_password_locator = '.orangehrm-login-forgot-header'
    __validation_error_caption_locator = '.oxd-input-field-error-message'
    __input_fields_wrapper = '[class="oxd-input-group oxd-input-field-bottom-space"]'
    __invalid_credentials_caption_locator = '.oxd-alert-content-text'
    __input_field_generic_class = '.oxd-input'

    def __init__(self, page: Page):
        super().__init__(page)

    def login_to_orange_hr(self, username: str = os.getenv("ADMIN_USER"), password: str = os.getenv("ADMIN_PASSWORD"),
                           all_fields_empty: bool = None, partial_fields_empty: bool = None, error_name: str = None,
                           invalid_credentials: bool = None):
        """login method with default params that are found in the dotenv file - the function provides flexible
        options to handle errors for negative testing scenarios based on the optional params provided"""
        try:
            self.fill_text(self.__username_locator, username)
            self.fill_text(self.__password_locator, password)
            login_button = self.page.locator(self.__login_button_locator)
            self.click_element(login_button)
            if all_fields_empty is not None:
                return self.count_client_side_validation_errors_on_empty_fields(self.__input_field_generic_class,
                                                                                self.__validation_error_caption_locator)
            if partial_fields_empty is not None:
                field_with_error_index = self.count_client_side_validation_errors(
                    self.__validation_error_caption_locator, self.__input_fields_wrapper, error_name)
                return field_with_error_index
            if invalid_credentials is not None:
                invalid_credentials_text = self.page.locator(self.__invalid_credentials_caption_locator).inner_text()
                return invalid_credentials_text.strip()

        except Exception as error:
            raise RuntimeError(
                f"something went wrong in one of the conditions inside the login function - please check the count "
                f"client side validation function {error}")
