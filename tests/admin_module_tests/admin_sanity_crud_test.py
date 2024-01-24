import pytest

from tests.conftest import *
from pages.admin.admin_module_main_page.admin_main_page import AdminMainPage
from app_enums.navigation_enums.sidebar.sidebar_modules import SideBarModules


@pytest.mark.ADMIN
def test_add_admin_user(load_app_and_login, page):
    admin_module_main_page = AdminMainPage(page)
    admin_module_main_page.navigate_to_module(SideBarModules.ADMIN)
    admin_module_main_page.button.click_add()
