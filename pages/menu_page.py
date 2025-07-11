from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.base_page import BasePage
from locators.locators import InventoryLocators
from locators.locators import MenuLocators

from base.base_page import BasePage
from locators.locators import MenuLocators

class MenuPage(BasePage):
    def open_menu(self):
        self.click(MenuLocators.MENU_BUTTON)


    def is_visible(self, locator):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def is_menu_item_visible(self, locator):
        return self.is_visible(locator)

    def all_menu_items_visible(self):
        expected_items = [
            MenuLocators.ALL_ITEMS,
            MenuLocators.ABOUT,
            MenuLocators.LOGOUT,
            MenuLocators.RESET_STATE
        ]
        return all(self.is_menu_item_visible(item) for item in expected_items)

    def click_all_items(self):
        self.click(MenuLocators.ALL_ITEMS)

    def click_about(self):
        self.click(MenuLocators.ABOUT)

    def is_redirected_to_about_page(self):
        expected_url = "https://saucelabs.com/"
        return expected_url in self.driver.current_url

