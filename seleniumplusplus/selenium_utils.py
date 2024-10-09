from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    ElementNotVisibleException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from typing import Optional, List


class WaitUtils:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.timeout = timeout

    def wait_for_element(self, by, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException as e:
            print(f"Element with locator {by} and value '{value}' not found: {e}")
            return None

    def wait_for_clickable(self, by, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.element_to_be_clickable((by, value)))
        except TimeoutException as e:
            print(f"Clickable element with locator {by} and value '{value}' not found: {e}")
            return None


class SeleniumUtils:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait_utils = WaitUtils(driver, timeout)
        self.action_chains = ActionChains(driver)

    def move_to_element(self, element: WebElement) -> None:
        if element:
            try:
                self.action_chains.move_to_element(element).perform()
            except WebDriverException as e:
                print(f"Failed to move to element: {e}")
        else:
            print("Element is not present and cannot be moved to.")

    def find_element(self, by, value: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> Optional[WebElement]:
        element = self.wait_utils.wait_for_element(by, value, timeout)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def fill_input(self, by, value: str, input_text: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        input_element = self.find_element(by, value, exact_match, move_to_element, timeout)
        if input_element:
            try:
                input_element.clear()
                input_element.send_keys(input_text)
                print(f"Successfully filled the input field '{value}' with text: {input_text}")
            except WebDriverException as e:
                print(f"Failed to fill input field '{value}': {e}")
                raise e

    def select_option_by_text(self, by, value: str, option_text: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        select_element = self.find_element(by, value, exact_match, move_to_element, timeout)
        if select_element:
            try:
                select = Select(select_element)
                select.select_by_visible_text(option_text)
                print(f"Successfully selected option '{option_text}' for field '{value}'")
            except WebDriverException as e:
                print(f"Failed to select option '{option_text}' for field '{value}': {e}")
                raise e

    def select_option_by_value(self, by, value: str, option_value: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        select_element = self.find_element(by, value, exact_match, move_to_element, timeout)
        if select_element:
            try:
                select = Select(select_element)
                select.select_by_value(option_value)
                print(f"Successfully selected value '{option_value}' for field '{value}'")
            except WebDriverException as e:
                print(f"Failed to select value '{option_value}' for field '{value}': {e}")
                raise e

    def construct_xpath(self, tag: str, attribute: str, value: str, exact_match: bool) -> str:
        return f"//{tag}[@{attribute}='{value}']" if exact_match else f"//{tag}[contains(@{attribute}, '{value}')]"

    def find_element_by_text_or_attribute(self, text: str, tag: str = "*", exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> Optional[WebElement]:
        xpath = f".//{tag}[descendant-or-self::*[text()='{text}']]" if exact_match else f".//{tag}[descendant-or-self::*[contains(text(), '{text}') or contains(@class, '{text}') or contains(@aria-label, '{text}') or contains(@placeholder, '{text}')]]"
        return self.find_element(By.XPATH, xpath, exact_match, move_to_element, timeout)

    def find_button_by_text_or_attribute(self, text: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> Optional[WebElement]:
        return self.find_element_by_text_or_attribute(text, tag="button", exact_match=exact_match, move_to_element=move_to_element, timeout=timeout)

    def fill_input_by_attribute(self, attribute: str, attribute_name: str, input_text: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        xpath = self.construct_xpath("input", attribute, attribute_name, exact_match)
        self.fill_input(By.XPATH, xpath, input_text, exact_match, move_to_element, timeout)

    def fill_select_by_text(self, attribute: str, attribute_name: str, option_text: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        xpath = self.construct_xpath("select", attribute, attribute_name, exact_match)
        self.select_option_by_text(By.XPATH, xpath, option_text, exact_match, move_to_element, timeout)

    def fill_select_by_value(self, attribute: str, attribute_name: str, option_value: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        xpath = self.construct_xpath("select", attribute, attribute_name, exact_match)
        self.select_option_by_value(By.XPATH, xpath, option_value, exact_match, move_to_element, timeout)

    def fill_boolean_select(self, attribute: str, attribute_name: str, value: bool, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        option_value = "Yes" if value else "No"
        self.fill_select_by_text(attribute, attribute_name, option_value, exact_match, move_to_element, timeout)

    def fill_date_input(self, attribute: str, attribute_name: str, date: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        xpath = self.construct_xpath("input", attribute, attribute_name, exact_match)
        self.fill_input(By.XPATH, xpath, date, exact_match, move_to_element, timeout)

    def fill_datetime_input(self, attribute: str, attribute_name: str, datetime_str: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> None:
        self.fill_date_input(attribute, attribute_name, datetime_str, exact_match, move_to_element, timeout)

    def find_element_by_id(self, element_id: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> Optional[WebElement]:
        return self.find_element(By.ID, element_id, exact_match, move_to_element, timeout)

    def get_element_by_attribute(self, attribute: str, attribute_value: str, tag: str = "*", exact_match: bool = True, move_to_element: bool = False, timeout: Optional[int] = None) -> Optional[WebElement]:
        xpath = self.construct_xpath(tag, attribute, attribute_value, exact_match)
        element = self.wait_utils.wait_for_element(By.XPATH, xpath, timeout)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def get_clickable_element_by_text(self, text: str, tag: str = "*", exact_match: bool = False, move_to_element: bool = True, timeout: Optional[int] = None) -> Optional[WebElement]:
        xpath = f".//{tag}[text()='{text}']" if exact_match else f".//{tag}[contains(., '{text}')]"
        element = self.wait_utils.wait_for_clickable(By.XPATH, xpath, timeout)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def get_clickable_elements_by_text(self, text: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> List[WebElement]:
        xpath = f".//*[text()='{text}']" if exact_match else f".//*[contains(text(), '{text}')]"
        elements = self.wait_utils.wait_for_element(By.XPATH, xpath, timeout)
        if elements:
            elements = [elements]  # Ensure elements is a list
            if move_to_element:
                for element in elements:
                    self.move_to_element(element)
        else:
            elements = []
        return elements

    def get_button_by_label(self, label: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> Optional[WebElement]:
        xpath = f".//button[normalize-space(text())='{label}']" if exact_match else f".//button[contains(text(), '{label}')]"
        button = self.wait_utils.wait_for_clickable(By.XPATH, xpath, timeout)
        if button and move_to_element:
            self.move_to_element(button)
        return button

    def get_buttons_by_label(self, label: str, exact_match: bool = False, move_to_element: bool = False, timeout: Optional[int] = None) -> List[WebElement]:
        xpath = f".//button[normalize-space(text())='{label}']" if exact_match else f".//button[contains(text(), '{label}')]"
        buttons = self.wait_utils.wait_for_element(By.XPATH, xpath, timeout)
        if buttons:
            buttons = [buttons]  # Ensure buttons is a list
            if move_to_element:
                for button in buttons:
                    self.move_to_element(button)
        else:
            buttons = []
        return buttons