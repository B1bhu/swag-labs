import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from locators.locators import MenuLocators, LoginLocators


@pytest.mark.menu
def test_menu_button_displays_expected_options(driver):
    login_page = LoginPage(driver)
    menu_page = MenuPage(driver)

    login_page.login(LoginLocators.VALID_USERNAME, LoginLocators.VALID_PASSWORD)
    menu_page.open_menu()

    assert menu_page.is_menu_item_visible(MenuLocators.ALL_ITEMS)
    assert menu_page.is_menu_item_visible(MenuLocators.ABOUT)
    assert menu_page.is_menu_item_visible(MenuLocators.LOGOUT)
    assert menu_page.is_menu_item_visible(MenuLocators.RESET_STATE)


@pytest.mark.menu
def test_all_items_menu_redirect_from_cart(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    menu_page = MenuPage(driver)
    cart_page = CartPage(driver)

    # Log in
    login_page.login(LoginLocators.VALID_USERNAME,LoginLocators.VALID_PASSWORD)

    # Navigate to Cart Page first
    inventory_page.go_to_cart()

    # Open menu and click All Items
    menu_page.open_menu()
    menu_page.click_all_items()

    # Assert that URL is now inventory page
    assert inventory_page.is_at_inventory_url(), "User was not redirected to Inventory Page after clicking 'All Items'"


@pytest.mark.menu
def test_about_us_menu_redirect(driver):
    login_page = LoginPage(driver)
    menu_page = MenuPage(driver)
    cart_page = CartPage(driver)

    # Step 1: Login and move away from inventory
    login_page.login("standard_user", "secret_sauce")
    cart_page.is_cart_empty()  # optional page switch

    # Step 2: Open menu and click About
    menu_page.open_menu()
    menu_page.click_about()

    # Step 3: Assert redirection to Sauce Labs
    assert menu_page.is_redirected_to_about_page(), "Not redirected to Sauce Labs homepage as expected"