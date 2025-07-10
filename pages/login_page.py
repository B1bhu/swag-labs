# from selenium.webdriver.common.by import By
# from base.base_page import BasePage
#
# class LoginPage(BasePage):
#     USERNAME = (By.ID, "user-name")
#     PASSWORD = (By.ID, "password")
#     LOGIN_BUTTON = (By.ID, "login-button")
#
#     def login(self, username, password):
#         self.type(self.USERNAME, username)
#         self.type(self.PASSWORD, password)
#         self.click(self.LOGIN_BUTTON)

# src/pages/login_page.py

from base.base_page import BasePage
from locators.locators import LoginLocators


class LoginPage(BasePage):
    def login(self, username, password):
        self.type(LoginLocators.USERNAME, username)
        self.type(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.LOGIN_BUTTON)