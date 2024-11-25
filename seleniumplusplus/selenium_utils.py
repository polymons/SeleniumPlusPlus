from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    ElementNotVisibleException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from typing import Optional, List, Literal, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        timeout: Optional[int] = None,
    ) -> WebElement:
        """Enhanced wait_for_element with better error handling and timeout override"""
        if not self.driver:
            raise WebDriverException("Driver is not initialized")
            
        try:
            wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
            by_attr = getattr(By, str(by).upper())
            if not by_attr:
                raise ValueError(f"Invalid locator method: {by}")
                
            element = wait.until(EC.presence_of_element_located((by_attr, value)))
            if not element:
                raise NoSuchElementException(f"Element not found with {by}={value}")
                
            return element
            
        except TimeoutException as e:
            logger.error(f"Element not found within timeout: {by}={value}")
            raise NoSuchElementException(f"Element not found with {by}={value}") from e
        except Exception as e:
            logger.error(f"Error waiting for element: {by}={value}, Error: {str(e)}")
            raise

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
        if not driver:
            raise ValueError("WebDriver instance is required")
        self.driver = driver
        self.wait_utils = WaitUtils(driver, timeout)
        self.action_chains = ActionChains(driver)

    def move_to_element(self, element: WebElement) -> None:
        """
        Moves the mouse pointer to the specified WebElement.

        :param element: The WebElement to move to.
        """
        if not element:
            logger.error("Cannot move to None element")
            return
            
        try:
            if not element.is_enabled() or not element.is_displayed():
                logger.warning("Element is not visible or enabled")
                return
                
            self.action_chains.move_to_element(element).perform()
        except Exception as e:
            logger.error(f"Failed to move to element: {str(e)}")

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
        move_to_element: bool = True,
    ) -> WebElement:
        """
        Finds an element based on the provided locator and optionally moves to it.

        :param by: The method to locate the element (e.g., 'id', 'xpath').
        :param value: The value of the locator (e.g., 'button-id').
        :param move_to_element: Whether to move to the element after finding it.
        :return: The located WebElement.
        """
        if not value:
            raise ValueError("Locator value cannot be empty")
            
        try:
            element = self.wait_utils.wait_for_element(by, value)
            if not element:
                raise NoSuchElementException(f"Element not found with {by}={value}")
                
            if move_to_element:
                self.move_to_element(element)
            return element
            
        except Exception as e:
            logger.error(f"Failed to find element: {by}={value}, Error: {str(e)}")
            raise

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
        move_to_element: bool = True,
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
                logger.info(
                    f"Successfully filled the input field '{value}' with text: {input_text}"
                )
            except WebDriverException as e:
                logger.error(f"Failed to fill input field '{value}': {e}")
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
        move_to_element: bool = True,
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
                logger.info(
                    f"Successfully selected option '{option_text}' for field '{value}'"
                )
            except WebDriverException as e:
                logger.error(
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
        move_to_element: bool = True,
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
                logger.info(
                    f"Successfully selected value '{option_value}' for field '{value}'"
                )
            except WebDriverException as e:
                logger.error(
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
        move_to_element: bool = True,
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
        move_to_element: bool = True,
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
        move_to_element: bool = True,
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
        move_to_element: bool = True,
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
        move_to_element: bool = True,
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
        move_to_element: bool = True,
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
        move_to_element: bool = True,
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
        self, element_id: str, exact_match: bool = False, move_to_element: bool = True
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
        move_to_element: bool = True,
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

    def get_clickable_element_by_text(
        self,
        text: str,
        tag: str = "*",
        exact_match: bool = False,
        move_to_element: bool = True,
        include_descendants: bool = True,
    ) -> WebElement:
        """
        Fixed version that properly finds clickable elements with text.
        Added include_descendants parameter to control text search scope.
        """
        text_match = "text()" if not include_descendants else ".//text()"
        xpath = (
            f".//{tag}[normalize-space({text_match})='{text}' and not(descendant::button)]"
            if exact_match
            else f".//{tag}[contains({text_match}, '{text}') and not(descendant::button)]"
        )
        try:
            element = self.wait_utils.wait_for_clickable(By.XPATH, xpath)
            if element and move_to_element:
                self.move_to_element(element)
            return element
        except TimeoutException:
            logger.error(f"No clickable element found with text: {text}")
            raise
        except Exception as e:
            logger.error(f"Error finding clickable element: {str(e)}")
            raise

    def get_clickable_elements_by_text(
        self, text: str, exact_match: bool = False, move_to_element: bool = True
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
        self, 
        label: str, 
        exact_match: bool = False, 
        move_to_element: bool = True,
        include_spans: bool = True,
        include_inputs: bool = True,
        case_sensitive: bool = False
    ) -> WebElement:
        """
        Enhanced button finder that handles various button implementations.

        :param label: The label/text of the button to search for
        :param exact_match: If True, matches the label exactly
        :param move_to_element: Whether to move to the button after finding it
        :param include_spans: Include span elements that act as buttons
        :param include_inputs: Include input elements of type button/submit
        :param case_sensitive: Whether to match text case sensitively
        :return: The found button WebElement
        """
        label_text = label if case_sensitive else label.lower()
        
        # Build xpath conditions for text matching
        text_match = (
            f"normalize-space()='{label_text}'"
            if exact_match
            else f"contains(normalize-space(),'{label_text}')"
        )
        
        if not case_sensitive:
            text_match = f"translate({text_match}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"

        # Base button selectors
        button_conditions = [
            f".//button[{text_match}]",  # Standard buttons
            f".//button[.//*[{text_match}]]",  # Buttons with nested elements
        ]

        # Add optional selectors
        if include_spans:
            button_conditions.extend([
                f".//span[{text_match} and @role='button']",
                f".//div[{text_match} and @role='button']",
                f".//a[{text_match} and @role='button']"
            ])

        if include_inputs:
            button_conditions.extend([
                f".//input[@type='button' and {text_match}]",
                f".//input[@type='submit' and {text_match}]",
                f".//input[@value and {text_match} and (@type='button' or @type='submit')]"
            ])

        # Combine all conditions
        xpath = f"({' | '.join(button_conditions)})"

        try:
            # Try to find clickable button
            button = self.wait_utils.wait_for_clickable(By.XPATH, xpath)
            if not button:
                # If not found, try finding any matching element
                button = self.wait_utils.wait_for_element(By.XPATH, xpath)

            if button and move_to_element:
                self.move_to_element(button)

            return button

        except Exception as e:
            logger.error(f"Failed to find button with label '{label}': {str(e)}")
            # Try finding buttons in iframes before giving up
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    button = self.wait_utils.wait_for_clickable(By.XPATH, xpath)
                    if button:
                        if move_to_element:
                            self.move_to_element(button)
                        return button
                except:
                    continue
                finally:
                    self.driver.switch_to.default_content()
            
            raise NoSuchElementException(f"No button found with label: {label}")

    def get_buttons_by_label(
        self, label: str, exact_match: bool = False, move_to_element: bool = True
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

    def safe_click(self, element: WebElement, retry_count: int = 3) -> bool:
        """
        New convenience method for safely clicking elements with retries
        
        :param element: The element to click
        :param retry_count: Number of retry attempts
        :return: True if click successful, False otherwise
        """
        for i in range(retry_count):
            try:
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    return True
            except StaleElementReferenceException:
                if i == retry_count - 1:
                    logger.error("Element became stale")
                    return False
                continue
            except Exception as e:
                logger.error(f"Click failed: {str(e)}")
                return False
        return False

    def wait_for_text(self, text: str, timeout: Optional[int] = None) -> bool:
        """
        New convenience method to wait for text to appear anywhere on the page
        
        :param text: Text to wait for
        :param timeout: Optional custom timeout
        :return: True if text found, False if timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout or self.wait_utils.wait._timeout)
            return wait.until(lambda driver: text in driver.page_source)
        except TimeoutException:
            return False