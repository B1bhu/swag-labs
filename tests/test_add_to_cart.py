import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.add_to_cart
def test_add_single_item_to_cart(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.login(username, password)
    inventory_page.add_to_cart_by_name(product_name)

    cart_count = inventory_page.get_cart_count()
    assert cart_count == "1", f"Expected cart count to be 1 but got {cart_count}"

@pytest.mark.add_to_cart
def test_item_details_in_cart(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"
    expected_price = "$29.99"
    expected_quantity = "1"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.login(username, password)
    inventory_page.add_to_cart_by_name(product_name)
    inventory_page.go_to_cart()

    names = cart_page.get_item_names()
    prices = cart_page.get_item_prices()
    quantity = cart_page.get_quantity()

    assert product_name in names, f"{product_name} not found in cart items"
    assert expected_price in prices, f"Expected price {expected_price} not found in cart prices"
    assert quantity == expected_quantity, f"Expected quantity {expected_quantity}, but got {quantity}"

@pytest.mark.add_to_cart
def test_add_multiple_items_to_cart(driver):
    username = "standard_user"
    password = "secret_sauce"
    products = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"]

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.login(username, password)

    # Add each item
    for item in products:
        inventory_page.add_to_cart_by_name(item)

    # Verify cart icon count
    cart_count = inventory_page.get_cart_count()
    assert cart_count == str(len(products)), f"Expected cart count {len(products)}, got {cart_count}"

    inventory_page.go_to_cart()

    # Verify all items exist in cart
    cart_items = cart_page.get_item_names()
    for item in products:
        assert item in cart_items, f"{item} not found in cart items"

@pytest.mark.add_to_cart
def test_cart_is_empty_on_login(driver):
    username = "standard_user"
    password = "secret_sauce"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.login(username, password)
    inventory_page.go_to_cart()

    is_empty = cart_page.is_cart_empty()
    assert is_empty, "Cart is not empty for a fresh login"

    # Bonus: check if cart icon badge exists (shouldn't)
    cart_icon_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(cart_icon_badge) == 0, "Cart badge should not be visible for empty cart"


@pytest.mark.add_to_cart
def test_add_button_changes_to_remove_and_back(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.login(username, password)

    # Verify button initially says "Add to cart"
    initial_text = inventory_page.get_button_text(product_name)
    assert initial_text.lower() == "add to cart", f"Expected 'Add to cart' but got '{initial_text}'"

    # Add item
    inventory_page.add_to_cart_by_name(product_name)
    after_add_text = inventory_page.get_button_text(product_name)
    assert after_add_text.lower() == "remove", f"Expected 'Remove' after adding but got '{after_add_text}'"

    # Remove item
    inventory_page.remove_from_cart_by_name(product_name)
    after_remove_text = inventory_page.get_button_text(product_name)
    assert after_remove_text.lower() == "add to cart", f"Expected 'Add to cart' after removing but got '{after_remove_text}'"


@pytest.mark.add_to_cart
def test_add_and_remove_item_cart_empty(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    wait = WebDriverWait(driver, 10)

    login_page.login(username, password)

    # Add item
    inventory_page.add_to_cart_by_name(product_name)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    cart_count = inventory_page.get_cart_count()
    assert cart_count == "1", f"Cart count should be 1 after adding item, got {cart_count}"

    # Remove item
    inventory_page.remove_from_cart_by_name(product_name)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    cart_count_after_removal = inventory_page.get_cart_count()
    assert cart_count_after_removal is None, "Cart badge should disappear after removing all items"

    # Verify cart page is empty
    inventory_page.go_to_cart()
    assert cart_page.is_cart_empty(), "Cart should be empty after removing the item"


@pytest.mark.add_to_cart
def test_cart_badge_increases_with_each_item(driver):
    username = "standard_user"
    password = "secret_sauce"
    products = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt", "Sauce Labs Onesie"]

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.login(username, password)

    for idx, product in enumerate(products, start=1):
        inventory_page.add_to_cart_by_name(product)
        cart_count = inventory_page.get_cart_count()
        assert cart_count == str(idx), f"Expected cart count '{idx}' after adding '{product}', but got '{cart_count}'"


@pytest.mark.add_to_cart
def test_cart_persists_after_page_refresh(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.login(username, password)

    # Add product to cart
    inventory_page.add_to_cart_by_name(product_name)

    # Refresh the page
    driver.refresh()

    # Verify cart count still shows 1
    cart_count = inventory_page.get_cart_count()
    assert cart_count == "1", f"Expected cart count '1' after refresh, got '{cart_count}'"

    # Navigate to cart and verify item still present
    inventory_page.go_to_cart()
    item_names = cart_page.get_item_names()
    assert product_name in item_names, f"{product_name} not found in cart after refresh"

import pytest

@pytest.mark.add_to_cart
def test_same_item_not_added_twice(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.login(username, password)

    # Add product once
    inventory_page.add_to_cart_by_name(product_name)
    cart_count = inventory_page.get_cart_count()
    assert cart_count == "1", f"Expected cart count to be 1 after first add, got {cart_count}"

    # Try to click "Add to Cart" again (should be "Remove" now)
    # If clicked again, it would remove — so don’t click it again
    # Instead, assert the button says "Remove"
    button_text = inventory_page.get_button_text(product_name)
    assert button_text.lower() == "remove", f"Expected button text to be 'Remove', got '{button_text}'"

    # Re-check cart count (should still be 1)
    cart_count_after = inventory_page.get_cart_count()
    assert cart_count_after == "1", f"Cart count should still be 1, but got {cart_count_after}"


def test_cart_persists_after_logout_and_login(driver):
    username = "standard_user"
    password = "secret_sauce"
    product_name = "Sauce Labs Backpack"

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    # Login and add item
    login_page.login(username, password)
    inventory_page.add_to_cart_by_name(product_name)
    assert inventory_page.get_cart_count() == "1"

    # Logout
    inventory_page.logout()

    # Login again
    login_page.login(username, password)

    # Go to cart and verify item still exists
    inventory_page.go_to_cart()
    cart_items = cart_page.get_item_names()
    assert product_name in cart_items, "Cart should contain previously added item after logout and login"
    assert inventory_page.get_cart_count() == str(len(cart_items)), "Cart icon count should match cart items after re-login"


@pytest.mark.add_to_cart
def test_rapid_add_multiple_items(driver):
    username = "standard_user"
    password = "secret_sauce"
    products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)",
        "Sauce Labs Bike Light",
        "Sauce Labs Fleece Jacket"
    ]

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.login(username, password)

    for product in products:
        inventory_page.add_to_cart_by_name(product)

    # Verify cart badge count
    cart_count = inventory_page.get_cart_count()
    assert cart_count == str(len(products)), f"Expected {len(products)} items, got {cart_count}"

    inventory_page.go_to_cart()
    cart_items = cart_page.get_item_names()
    for product in products:
        assert product in cart_items, f"{product} missing in cart"

