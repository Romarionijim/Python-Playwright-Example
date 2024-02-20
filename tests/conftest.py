import os

import pytest
from playwright.async_api import async_playwright

from pages.login_page.login_page import LoginPage
from pages.orange_hr_base_page import OrangeHrBasePage
from app_enums.navigation_enums.urls.application_url import ApplicationUrl
from playwright.sync_api import Page, sync_playwright
from dotenv import load_dotenv
import allure
from slugify import slugify

load_dotenv()


def pytest_runtest_makereport(item, call) -> None:
    """attach screenshot and video to allure report on test failure/exception is thrown"""
    if call.when == "call":
        if call.excinfo is not None and "page" in item.funcargs:
            page: Page = item.funcargs["page"]
            allure.attach(
                page.screenshot(type='png', full_page=True),
                name=f"{slugify(item.nodeid)}.png",
                attachment_type=allure.attachment_type.PNG
            )

            video_path = page.video.path()
            page.context.close()
            allure.attach(
                open(video_path, 'rb').read(),
                name=f"{slugify(item.nodeid)}.webm",
                attachment_type=allure.attachment_type.WEBM
            )


@pytest.fixture(scope="session", autouse=True)
def browser_context_args_fixture(browser_context_args, tmpdir_factory: pytest.TempdirFactory):
    temp_dir = tmpdir_factory.mktemp('videos')
    print(f"Temporary directory: {temp_dir}")
    return {
        **browser_context_args,
        "viewport": {
            "width": 1400,
            "height": 900,
        },
        "record_video_dir": temp_dir
    }


@pytest.fixture(scope="function")
def load_app_and_login(page: Page):
    """loads the orange hr app website and logs in to the application for reusable code in each test"""
    base = OrangeHrBasePage(page)
    base.load_application(ApplicationUrl.ORANGE_HR_WEBSITE)
    login_page = LoginPage(page)
    login_page.login_to_orange_hr()
    yield login_page, base


@pytest.fixture(scope="function")
def load_application(page: Page):
    """load the app and login to the website - purpose to prevent code duplication since this method is called in each test function"""
    base = OrangeHrBasePage(page)
    base.load_application(ApplicationUrl.ORANGE_HR_WEBSITE)
    yield base


@pytest.fixture(scope="function")
def instantiate_login_page_class(page: Page):
    """instantiate the login page to prevent code duplication - this fixture is for login negative tests """
    login_page = LoginPage(page)
    yield login_page


@pytest.fixture()
def page(page: Page):
    yield page


# @pytest.fixture(scope='session', autouse=True)
# def browser_mode():
#     """Runs chromium browser headless in CI environment, else runs headed."""
#     if os.getenv('CI'):
#         with async_playwright() as p:
#             browser = p.chromium.launch(headless=)


# @pytest.fixture(scope="session", autouse=True)
# def head():
#     async with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         yield page
#     if os.getenv("HEADED"):
#         pass
#     else:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context()
#         page = context.new_page()
#         yield page
