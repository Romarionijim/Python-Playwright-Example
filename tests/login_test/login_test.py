import pytest
import allure
from tests.login_test.login_test_data import *


@allure.epic("Login Sanity")
@allure.suite('Login test suite')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
def test_valid_login(load_app_and_login):
    with allure.step("load application and login to the website from the fixture dependency injection"):
        orange_hr_base_page, login = load_app_and_login
    with allure.step("validate user is logged in successfully to the dashboard page"):
        actual = orange_hr_base_page.get_current_active_module_name()
        assert actual == 'noooo'


@allure.epic("Login Sanity")
@allure.suite('Login test suite')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.SANITY
def test_login_with_invalid_credentials(load_application, instantiate_login_page_class):
    with allure.step("load app instantiate the login page class via pytest fixture"):
        login_page = instantiate_login_page_class
    with allure.step("login with invalid credentials and validate invalid credentials error is displayed"):
        result = login_page.login_to_orange_hr("invalid", "password", invalid_credentials=True)
        assert result == INVALID_CREDENTIALS


@allure.epic("Login Sanity")
@allure.suite('Login test suite')
@allure.title('login negative test')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.SANITY
def test_login_with_empty_fields(load_application, instantiate_login_page_class):
    with allure.step("set up  login page class via pytest fixture"):
        login_page = instantiate_login_page_class
    with allure.step("login with leaving all fields empty and validate 2 validation errors occur"):
        result = login_page.login_to_orange_hr('', '', all_fields_empty=True)
        assert result == (2, ['Required', 'Required'])


@allure.epic("Login Sanity")
@allure.suite('Login test suite')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.SANITY
def test_login_with_empty_username_field(load_application, instantiate_login_page_class):
    with allure.step("load app and setup login class object"):
        login_page = instantiate_login_page_class
    with allure.step("login by leaving the username field empty and validate a required error is displayed on that "
                     "field"):
        result = login_page.login_to_orange_hr('', partial_fields_empty=True, error_name=REQUIRED)
        assert result == (1, [0], ['Username\nRequired'])


@allure.epic("Login Sanity")
@allure.suite('Login test suite')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.SANITY
def test_login_with_empty_password_field(load_application, instantiate_login_page_class):
    with allure.step("load app and setup login class object"):
        login_page = instantiate_login_page_class
    with allure.step(
            "login by leaving the password field empty and validate a required error is displayed on that field"):
        result = login_page.login_to_orange_hr('Admin', '', partial_fields_empty=True, error_name=REQUIRED)
        assert result == (1, [1], ['Password\nRequired'])
