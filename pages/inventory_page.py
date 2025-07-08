# src/pages/inventory_page.py
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_page import BasePage

class InventoryPage(BasePage):
    def logout(self):
        menu_btn = (By.ID, "react-burger-menu-btn")
        logout_btn = (By.ID, "logout_sidebar_link")

        self.click(menu_btn)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(logout_btn))
        self.click(logout_btn)

    def add_to_cart_by_name(self, product_name):
        add_button = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        self.click(add_button)

    def get_cart_count(self):
        cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(cart_badge)
            ).text
        except:
            return None  # Means cart is empty (no badge)

    def go_to_cart(self):
        cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.click(cart_icon)

    def add_multiple_items_to_cart(self, product_names: list):
        for name in product_names:
            self.add_to_cart_by_name(name)

    def remove_from_cart_by_name(self, product_name):
        # Same locator as add button, it toggles text to "Remove"
        btn = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        self.click(btn)

    def is_visible(self, locator):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def get_button_text(self, product_name):
        btn = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(btn)
            ).text
        except:
            return None



