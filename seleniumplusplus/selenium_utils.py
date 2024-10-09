from selenium import webdriver
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
    """
    Class for handling waiting operations in Selenium.

    Args:
        driver (webdriver): The WebDriver instance to use for waiting.
        timeout (int): The maximum time to wait for an element to be located (default is 10 seconds).

    Methods:
        wait_for_element(by, value, exact_match): Waits for an element to be located on the page.
        wait_for_clickable(by, value, exact_match): Waits for an element to be clickable on the page.

    Returns:
        Optional[WebElement]: The located WebElement if found, None otherwise.
    """

    def __init__(self, driver: webdriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(
        self, by: By, value: str, exact_match: bool = False
    ) -> Optional[WebElement]:
        """
        Waits for an element to be located on the page.

        Args:
            by (By): The locator strategy to use.
            value (str): The value of the locator.
            exact_match (bool): Whether to match the value exactly.

        Returns:
            Optional[WebElement]: The located WebElement if found, None otherwise.
        """
        locator = (by, value)
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException as e:
            print(f"Element with locator {by} and value '{value}', exact_match was set to {exact_match} not found: {e}")
            return None

    def wait_for_clickable(
        self, by: By, value: str, exact_match: bool = False
    ) -> Optional[WebElement]:
        """
        Waits for an element to be clickable on the page.

        Args:
            by (By): The locator strategy to use.
            value (str): The value of the locator.
            exact_match (bool): Whether to match the value exactly.

        Returns:
            Optional[WebElement]: The located WebElement if found, None otherwise.
        """
        locator = (by, value)
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException as e:
            print(
                f"Clickable element with locator {by} and value '{value}', exact_match was set to {exact_match} not found: {e}"
            )
            return None


class SeleniumUtils:
    """
    Class for handling various Selenium operations like moving to elements, finding elements, filling inputs, and selecting options.

    Args:
        driver (webdriver): The WebDriver instance to use for Selenium operations.
        timeout (int): The maximum time to wait for an element to be located (default is 10 seconds).

    Methods:
        move_to_element(element): Moves the mouse pointer to the specified element.
        find_element(by, value, exact_match, move_to_element): Finds an element based on the locator strategy and value.
        fill_input(by, value, input_text, exact_match, move_to_element): Fills an input field with the specified text.
        select_option_by_text(by, value, option_text, exact_match, move_to_element): Selects an option by visible text.
        select_option_by_value(by, value, option_value, exact_match, move_to_element): Selects an option by value.
        find_element_by_text_or_attribute(text, tag, exact_match, move_to_element): Finds an element based on text or attribute.
        find_button_by_text_or_attribute(text, exact_match, move_to_element): Finds a button based on text or attribute.
        fill_input_by_attribute(attribute, attribute_name, input_text, exact_match, move_to_element): Fills an input field by attribute.
        fill_select_by_text(attribute, attribute_name, option_text, exact_match, move_to_element): Selects an option in a select field by text.
        fill_select_by_value(attribute, attribute_name, option_value, exact_match, move_to_element): Selects an option in a select field by value.
        fill_boolean_select(attribute, attribute_name, value, exact_match, move_to_element): Fills a boolean select field.
        fill_date_input(attribute, attribute_name, date, exact_match, move_to_element): Fills a date input field.
        fill_datetime_input(attribute, attribute_name, datetime_str, exact_match, move_to_element): Fills a datetime input field.
        find_element_by_id(element_id, exact_match, move_to_element): Finds an element by its ID.
        get_element_by_attribute(attribute, attribute_value, wait_condition, tag, exact_match, move_to_element): Retrieves an element by attribute and value with optional wait conditions.

    Returns:
        None
    """

    def __init__(self, driver: webdriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait_utils = WaitUtils(driver, timeout)
        self.action_chains = ActionChains(driver)

    def move_to_element(self, element: WebElement) -> None:
        """
        Moves the mouse pointer to the specified element.

        Args:
            element (WebElement): The WebElement to move to.
        """
        if element:
            try:
                self.action_chains.move_to_element(element).perform()
            except WebDriverException as e:
                print(f"Failed to move to element: {e}")
        else:
            print("Element is not present and cannot be moved to.")

    def find_element(
        self,
        by: By,
        value: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> Optional[WebElement]:
        element = self.wait_utils.wait_for_element(by, value, exact_match)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def fill_input(
        self,
        by: By,
        value: str,
        input_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        input_element = self.find_element(by, value, exact_match, move_to_element)
        if input_element:
            try:
                input_element.clear()
                input_element.send_keys(input_text)
                print(
                    f"Successfully filled the input field '{value}' with text: {input_text}"
                )
            except WebDriverException as e:
                print(f"Failed to fill input field '{value}': {e}")
                raise e

    def select_option_by_text(
        self,
        by: By,
        value: str,
        option_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        select_element = self.find_element(by, value, exact_match, move_to_element)
        if select_element:
            try:
                select = Select(select_element)
                select.select_by_visible_text(option_text)
                print(
                    f"Successfully selected option '{option_text}' for field '{value}'"
                )
            except WebDriverException as e:
                print(
                    f"Failed to select option '{option_text}' for field '{value}': {e}"
                )
                raise e

    def select_option_by_value(
        self,
        by: By,
        value: str,
        option_value: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        select_element = self.find_element(by, value, exact_match, move_to_element)
        if select_element:
            try:
                select = Select(select_element)
                select.select_by_value(option_value)
                print(
                    f"Successfully selected value '{option_value}' for field '{value}'"
                )
            except WebDriverException as e:
                print(
                    f"Failed to select value '{option_value}' for field '{value}': {e}"
                )
                raise e

    def construct_xpath(
        self, tag: str, attribute: str, value: str, exact_match: bool
    ) -> str:
        """
        Constructs an XPath query based on tag, attribute, value, and match type.
        """
        return (
            f"//{tag}[@{attribute}='{value}']"
            if exact_match
            else f"//{tag}[contains(@{attribute}, '{value}')]"
        )

    def find_element_by_text_or_attribute(
        self,
        text: str,
        tag: str = "*",
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> Optional[WebElement]:
        xpath = (
            f".//{tag}[descendant-or-self::*[text()='{text}']]"
            if exact_match
            else f".//{tag}[descendant-or-self::*[contains(text(), '{text}') or contains(@class, '{text}') or contains(@aria-label, '{text}') or contains(@placeholder, '{text}')]]"
        )
        return self.find_element(By.XPATH, xpath, exact_match, move_to_element)

    def find_button_by_text_or_attribute(
        self, text: str, exact_match: bool = False, move_to_element: bool = False
    ) -> Optional[WebElement]:
        return self.find_element_by_text_or_attribute(
            text, tag="button", exact_match=exact_match, move_to_element=move_to_element
        )

    def fill_input_by_attribute(
        self,
        attribute: str,
        attribute_name: str,
        input_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        xpath = self.construct_xpath("input", attribute, attribute_name, exact_match)
        self.fill_input(By.XPATH, xpath, input_text, exact_match, move_to_element)

    def fill_select_by_text(
        self,
        attribute: str,
        attribute_name: str,
        option_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        xpath = self.construct_xpath("select", attribute, attribute_name, exact_match)
        self.select_option_by_text(
            By.XPATH, xpath, option_text, exact_match, move_to_element
        )

    def fill_select_by_value(
        self,
        attribute: str,
        attribute_name: str,
        option_value: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        xpath = self.construct_xpath("select", attribute, attribute_name, exact_match)
        self.select_option_by_value(
            By.XPATH, xpath, option_value, exact_match, move_to_element
        )

    def fill_boolean_select(
        self,
        attribute: str,
        attribute_name: str,
        value: bool,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        option_value = "Yes" if value else "No"
        self.fill_select_by_text(
            attribute, attribute_name, option_value, exact_match, move_to_element
        )

    def fill_date_input(
        self,
        attribute: str,
        attribute_name: str,
        date: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        xpath = self.construct_xpath("input", attribute, attribute_name, exact_match)
        self.fill_input(By.XPATH, xpath, date, exact_match, move_to_element)

    def fill_datetime_input(
        self,
        attribute: str,
        attribute_name: str,
        datetime_str: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        self.fill_date_input(
            attribute, attribute_name, datetime_str, exact_match, move_to_element
        )

    def find_element_by_id(
        self, element_id: str, exact_match: bool = False, move_to_element: bool = False
    ) -> Optional[WebElement]:
        return self.find_element(By.ID, element_id, exact_match, move_to_element)

    def get_element_by_attribute(
        self,
        attribute: str,
        attribute_value: str,
        wait_condition: EC = EC.presence_of_element_located,
        tag: str = "*",
        exact_match: bool = True,
        move_to_element: bool = False,
    ) -> Optional[WebElement]:
        """
        Retrieves an element by attribute and value with optional wait conditions.

        Args:
            attribute (str): The attribute name to search for.
            attribute_value (str): The value of the attribute to match.
            wait_condition (EC): The expected condition to wait for (default is presence_of_element_located).
            tag (str): The HTML tag to search for (default is '*').
            exact_match (bool): Whether to match the attribute value exactly (default is True).
            move_to_element (bool): Whether to move to the element after locating it (default is False).

        Returns:
            Optional[WebElement]: The located WebElement if found, None otherwise.
        """
        xpath = self.construct_xpath(tag, attribute, attribute_value, exact_match)
        element = self.wait_utils.wait.until(wait_condition((By.XPATH, xpath)))
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def get_clickable_element_by_text(
        self, text: str, tag: str = "*", exact_match: bool = False, move_to_element: bool = True
    ) -> Optional[WebElement]:
        """
        Gets a single clickable element based on text.

        Args:
            text (str): The text to search for.
            exact_match (bool): Whether to match the text exactly.
            move_to_element (bool): Whether to move to the element after locating it.

        Returns:
            Optional[WebElement]: The located WebElement if found, None otherwise.
        """
        xpath = (
            f".//{tag}[text()='{text}']"
            if exact_match
            else f".//{tag}[contains(., '{text}')]"
        )
        element = self.wait_utils.wait_for_clickable(By.XPATH, xpath, exact_match)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def get_clickable_elements_by_text(
        self, text: str, exact_match: bool = False, move_to_element: bool = False
    ) -> List[WebElement]:
        """
        Gets multiple clickable elements based on text.

        Args:
            text (str): The text to search for.
            exact_match (bool): Whether to match the text exactly.
            move_to_element (bool): Whether to move to the elements after locating them.

        Returns:
            List[WebElement]: The list of located WebElements if found, empty list otherwise.
        """
        xpath = (
            f".//*[text()='{text}']"
            if exact_match
            else f".//*[contains(text(), '{text}')]"
        )
        elements = self.wait_utils.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        if move_to_element:
            for element in elements:
                self.move_to_element(element)
        return elements

    def get_button_by_label(
        self, label: str, exact_match: bool = False, move_to_element: bool = False
    ) -> Optional[WebElement]:
        """
        Gets a button element based on its label text.

        Args:
            label (str): The label text to search for.
            exact_match (bool): Whether to match the label text exactly.
            move_to_element (bool): Whether to move to the button after locating it.

        Returns:
            Optional[WebElement]: The located button WebElement if found, None otherwise.
        """
        xpath = (
            f".//button[normalize-space(text())='{label}']"
            if exact_match
            else f".//button[contains(text(), '{label}')]"
        )
        button = self.wait_utils.wait_for_clickable(By.XPATH, xpath, exact_match)
        if button and move_to_element:
            self.move_to_element(button)
        return button

    def get_buttons_by_label(
        self, label: str, exact_match: bool = False, move_to_element: bool = False
    ) -> List[WebElement]:
        """
        Gets multiple button elements based on their label text.

        Args:
            label (str): The label text to search for.
            exact_match (bool): Whether to match the label text exactly.
            move_to_element (bool): Whether to move to the buttons after locating them.

        Returns:
            List[WebElement]: The list of located button WebElements if found, empty list otherwise.
        """
        xpath = (
            f".//button[normalize-space(text())='{label}']"
            if exact_match
            else f".//button[contains(text(), '{label}')]"
        )
        buttons = self.wait_utils.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        if move_to_element:
            for button in buttons:
                self.move_to_element(button)
        return buttons
