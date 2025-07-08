# src/pages/cart_page.py

from selenium.webdriver.common.by import By
from base.base_page import BasePage

class CartPage(BasePage):
    def get_item_names(self):
        item_names = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [item.text for item in item_names]

    def get_item_prices(self):
        item_prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [item.text for item in item_prices]

    def get_quantity(self):
        quantity_element = self.driver.find_element(By.CLASS_NAME, "cart_quantity")
        return quantity_element.text

    def is_cart_empty(self):
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        return len(items) == 0
