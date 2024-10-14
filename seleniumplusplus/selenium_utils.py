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
from typing import Optional, List, Literal


class WaitUtils:
    """
    Utility class to handle waiting for elements using Selenium WebDriver.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        Initializes the WaitUtils with the WebDriver instance and a default timeout.

        :param driver: The WebDriver instance to use.
        :param timeout: The maximum time to wait for elements (in seconds).
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(
        self,
        by: Literal[
            "id",
            "xpath",
            "link_text",
            "partial_link_text",
            "name",
            "tag_name",
            "class_name",
            "css_selector",
        ],
        value: str,
    ) -> WebElement:
        """
        Waits for the presence of an element located by a specific selector.

        :param by: The method to locate the element (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'button-id').
        :return: The WebElement if found, otherwise raises TimeoutException.
        """
        locator = (
            str(by),
            value,
        )  # TODO: Check if this is correct, should be (By.XPATH, value) str cast might not be necessary
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(
        self,
        by: Literal[
            "id",
            "xpath",
            "link_text",
            "partial_link_text",
            "name",
            "tag_name",
            "class_name",
            "css_selector",
        ],
        value: str,
    ) -> WebElement:
        """
        Waits for an element to be clickable, located by a specific selector.

        :param by: The method to locate the element (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'button-id').
        :return: The WebElement if found and clickable, otherwise raises TimeoutException.
        """
        locator = (str(by), value)
        return self.wait.until(EC.element_to_be_clickable(locator))


class SeleniumUtils:
    """
    Utility class to perform common actions using Selenium WebDriver.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        Initializes SeleniumUtils with WebDriver, timeout, and related utilities.

        :param driver: The WebDriver instance to use.
        :param timeout: The maximum time to wait for elements (in seconds).
        """
        self.driver = driver
        self.wait_utils = WaitUtils(driver, timeout)
        self.action_chains = ActionChains(driver)

    def move_to_element(self, element: WebElement) -> None:
        """
        Moves the mouse pointer to the specified WebElement.

        :param element: The WebElement to move to.
        """
        if element:
            try:
                self.action_chains.move_to_element(element).perform()
            except WebDriverException as e:
                print(f"Failed to move to element: {e}")
        else:
            print("Element is null.")

    def find_element(
        self,
        by: Literal[
            "id",
            "xpath",
            "link_text",
            "partial_link_text",
            "name",
            "tag_name",
            "class_name",
            "css_selector",
        ],
        value: str,
        move_to_element: bool = False,
    ) -> WebElement:
        """
        Finds an element based on the provided locator and optionally moves to it.

        :param by: The method to locate the element (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'button-id').
        :param move_to_element: Whether to move to the element after finding it.
        :return: The located WebElement.
        """
        element = self.wait_utils.wait_for_element(by, value)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def fill_input(
        self,
        by: Literal[
            "id",
            "xpath",
            "link_text",
            "partial_link_text",
            "name",
            "tag_name",
            "class_name",
            "css_selector",
        ],
        value: str,
        input_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        """
        Fills an input field with the specified text.

        :param by: The method to locate the input field (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'input-id').
        :param input_text: The text to input.
        :param exact_match: Whether to match the locator exactly.
        :param move_to_element: Whether to move to the element after finding it.
        """
        input_element = self.find_element(by, value, move_to_element)
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
        by: Literal[
            "id",
            "xpath",
            "link_text",
            "partial_link_text",
            "name",
            "tag_name",
            "class_name",
            "css_selector",
        ],
        value: str,
        option_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        """
        Selects an option in a dropdown by visible text.

        :param by: The method to locate the dropdown (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'select-id').
        :param option_text: The visible text of the option to select.
        :param exact_match: Whether to match the locator exactly.
        :param move_to_element: Whether to move to the element after finding it.
        """
        select_element = self.find_element(by, value, move_to_element)
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
        by: Literal[
            "id",
            "xpath",
            "link_text",
            "partial_link_text",
            "name",
            "tag_name",
            "class_name",
            "css_selector",
        ],
        value: str,
        option_value: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        """
        Selects an option in a dropdown by value.

        :param by: The method to locate the dropdown (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'select-id').
        :param option_value: The value attribute of the option to select.
        :param exact_match: Whether to match the locator exactly.
        :param move_to_element: Whether to move to the element after finding it.
        """
        select_element = self.find_element(by, value, move_to_element)
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
        Constructs an XPath expression based on the provided tag, attribute, value, and match type.

        :param tag: The HTML tag to search for (e.g., 'input', 'select').
        :param attribute: The attribute to match on (e.g., 'id', 'name').
        :param value: The value of the attribute to match.
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :return: The constructed XPath string.
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
    ) -> WebElement:
        """
        Finds an element by its text or various attributes (e.g., class, aria-label, placeholder).

        :param text: The text or attribute value to search for.
        :param tag: The HTML tag to search within (default is any tag).
        :param exact_match: If True, matches the text exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        :return: The found WebElement.
        """
        xpath = (
            f".//{tag}[descendant-or-self::*[text()='{text}']]"
            if exact_match
            else f".//{tag}[descendant-or-self::*[contains(text(), '{text}') or contains(@class, '{text}') or contains(@aria-label, '{text}') or contains(@placeholder, '{text}')]]"
        )
        return self.find_element(By.XPATH, xpath, move_to_element)

    def fill_input_by_attribute(
        self,
        attribute: str,
        attribute_name: str,
        input_text: str,
        exact_match: bool = False,
        move_to_element: bool = False,
    ) -> None:
        """
        Fills an input field located by a specific attribute and value.

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_name: The value of the attribute.
        :param input_text: The text to input into the field.
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        """
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
        """
        Selects an option in a dropdown by visible text, located by a specific attribute and value.

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_name: The value of the attribute.
        :param option_text: The visible text of the option to select.
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        """
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
        """
        Selects an option in a dropdown by value, located by a specific attribute and value.

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_name: The value of the attribute.
        :param option_value: The value of the option to select.
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        """
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
        """
        Selects an option in a dropdown based on a boolean value (Yes/No).

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_name: The value of the attribute.
        :param value: The boolean value (True for 'Yes', False for 'No').
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        """
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
        """
        Fills a date input field located by a specific attribute and value.

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_name: The value of the attribute.
        :param date: The date to input (e.g., '2024-10-14').
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        """
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
        """
        Fills a datetime input field located by a specific attribute and value.

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_name: The value of the attribute.
        :param datetime_str: The datetime to input (e.g., '2024-10-14T12:00').
        :param exact_match: If True, matches the attribute exactly; otherwise, uses 'contains'.
        :param move_to_element: Whether to move to the element after finding it.
        """
        self.fill_date_input(
            attribute, attribute_name, datetime_str, exact_match, move_to_element
        )

    def find_element_by_id(
        self, element_id: str, exact_match: bool = False, move_to_element: bool = False
    ) -> WebElement:
        """
        Finds an element by its ID.

        :param element_id: The ID of the element to search for.
        :param exact_match: If True, matches the ID exactly.
        :param move_to_element: Whether to move to the element after finding it.
        :return: The found WebElement.
        """
        return self.find_element(By.ID, element_id, move_to_element)

    def get_element_by_attribute(
        self,
        attribute: str,
        attribute_value: str,
        wait_condition,
        tag: str = "*",
        exact_match: bool = True,
        move_to_element: bool = False,
    ) -> WebElement:
        """
        Waits for an element to be located by a specific attribute and value.

        :param attribute: The HTML attribute to search for (e.g., 'id', 'name').
        :param attribute_value: The value of the attribute.
        :param wait_condition: The condition to wait for (e.g., presence, visibility).
        :param tag: The HTML tag to search within (default is any tag).
        :param exact_match: If True, matches the attribute exactly.
        :param move_to_element: Whether to move to the element after finding it.
        :return: The located WebElement.
        """
        xpath = self.construct_xpath(tag, attribute, attribute_value, exact_match)
        element = self.wait_utils.wait.until(wait_condition((By.XPATH, xpath)))
        if element and move_to_element:
            self.move_to_element(element)
        return element

    # BUG: Does not get the actual clickable element but probably the text above it
    def get_clickable_element_by_text(
        self,
        text: str,
        tag: str = "*",
        exact_match: bool = False,
        move_to_element: bool = True,
    ) -> WebElement:
        """
        Finds a clickable element by its text.

        :param text: The text to search for.
        :param tag: The HTML tag to search within (default is any tag).
        :param exact_match: If True, matches the text exactly.
        :param move_to_element: Whether to move to the element after finding it.
        :return: The clickable WebElement.
        """
        xpath = (
            f".//{tag}[text()='{text}']"
            if exact_match
            else f".//{tag}[contains(text(), '{text}')]"
        )
        element = self.wait_utils.wait_for_clickable(By.XPATH, xpath)
        if element and move_to_element:
            self.move_to_element(element)
        return element

    def get_clickable_elements_by_text(
        self, text: str, exact_match: bool = False, move_to_element: bool = False
    ) -> List[WebElement]:
        """
        Finds all clickable elements matching the specified text.

        :param text: The text to search for.
        :param exact_match: If True, matches the text exactly.
        :param move_to_element: Whether to move to the element after finding it.
        :return: A list of matching clickable WebElements.
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
    ) -> WebElement:
        """
        Finds a button element by its label.

        :param label: The label of the button to search for.
        :param exact_match: If True, matches the label exactly.
        :param move_to_element: Whether to move to the button after finding it.
        :return: The found button WebElement.
        """
        xpath = (
            f".//button[normalize-space(text())='{label}']"
            if exact_match
            else f".//button[contains(text(), '{label}')]"
        )
        button = self.wait_utils.wait_for_clickable(By.XPATH, xpath)
        if button and move_to_element:
            self.move_to_element(button)
        return button

    def get_buttons_by_label(
        self, label: str, exact_match: bool = False, move_to_element: bool = False
    ) -> List[WebElement]:
        """
        Finds all button elements matching the specified label.

        :param label: The label of the buttons to search for.
        :param exact_match: If True, matches the label exactly.
        :param move_to_element: Whether to move to the buttons after finding them.
        :return: A list of matching button WebElements.
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
