# testcase/conftest.py
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, ERP_URL

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.login(USERNAME, PASSWORD)
    yield driver