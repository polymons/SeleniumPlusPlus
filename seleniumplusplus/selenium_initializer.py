# driver_initializer.py
from typing import Any, Optional, Dict, Tuple, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebDriver
import logging
import time
from dotenv import load_dotenv
import os
import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Union

logger = logging.getLogger(__name__)

def init_driver(url: str, 
                headless: bool = False,
                custom_options: Optional[Dict[str, Any]] = None) -> WebDriver:
    """
    Enhanced driver initialization with more options
    
    :param url: The URL to navigate to
    :param headless: Whether to run in headless mode
    :param custom_options: Dictionary of additional Chrome options
    :return: Initialized WebDriver
    """
    opt = Options()
    opt.add_argument("--search-engine-choice-country")
    opt.add_argument("--disable-search-engine-choice-screen")
    
    if headless:
        opt.add_argument("--headless")
        
    if custom_options:
        for arg in custom_options.get('arguments', []):
            opt.add_argument(arg)
        for exp in custom_options.get('experimental_options', {}):
            opt.add_experimental_option(exp['name'], exp['value'])

    try:
        driver = webdriver.Chrome(options=opt)
        driver.maximize_window()
        driver.get(url)
        time.sleep(2)  # Consider replacing with explicit wait
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize driver: {str(e)}")
        raise

def read_login_env(username_id, password_id) -> tuple[str | None, str | None]:
    """
    Reads environment variables for username and password IDs.

    Args:
        username_id (str): The environment variable for the username for example: "LOGIN_NAME".
        password_id (str): The environment variable for the password for example: "PASSWORD".
    """
    load_dotenv()
    return os.getenv(username_id), os.getenv(password_id)


def read_csv(path, delimiter = ";", encoding = "utf-8-sig") -> list:
    '''
    Reads a CSV file and returns its content as a list of dictionaries.

    Args:
    - path (str): The path to the CSV file.
    - delimiter (str): The delimiter used in the CSV file (default is ";").
    - encoding (str): The encoding of the CSV file (default is "utf-8-sig").

    Returns:
    - list: A list of dictionaries where each dictionary represents a row in the CSV file.
    '''
    data = []
    try:
        with open(file=path, mode="rb") as csvfile:
            content = csvfile.read().decode(encoding=encoding)  # Remove BOM if present
            csvreader = csv.DictReader(content.splitlines(), delimiter=delimiter)

            # Iterate through each row in the CSV
            for row in csvreader:
                # Append each row (as a dictionary) to the data list
                data.append(row)

    except FileNotFoundError:
        # Print the current working directory
        print("Current working directory:", os.getcwd())
        print(f"File not found at path: {os.getcwd()}{path}")
        print("File not found.")
    except Exception as e:
        print("Error reading CSV file.")
        print(e)

    return data

def safe_file_operation(func):
    """Decorator for safe file operations with proper error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            raise
        except PermissionError as e:
            logger.error(f"Permission denied: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Operation failed: {str(e)}")
            raise
    return wrapper

@safe_file_operation
def save_csv(path: Union[str, Path], 
             data: List[Dict], 
             fieldnames: Optional[List[str]] = None,
             delimiter: str = ";", 
             encoding: str = "utf-8") -> bool:
    """Enhanced CSV saving with better path handling and validation"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if not data:
        raise ValueError("No data provided to save")
        
    fieldnames = fieldnames or list(data[0].keys())
    
    with path.open("w", newline="", encoding=encoding) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)
        logger.info(f"Successfully saved CSV to {path}")
        return True

def read_json(path, encoding='utf-8') -> Any | list:
    """
    Reads a JSON file and returns the data as a list of dictionaries.

    Args:
        path (str): The path to the JSON file.
        data (list): The list to append the data to. Defaults to an empty list.

    Returns:
        list: The data from the JSON file as a list of dictionaries.

    """
    data = []
    try:
        with open(path, "r", encoding=encoding) as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError:
        print(f"File not found at path: {path}")
    except Exception as e:
        print("Error reading JSON file.")
        print(e)

    return data


def save_json(path, data, encoding='utf-8') -> bool:
    """
    Saves the data to a JSON file at the specified path.

    Args:
        path (str): The path to the JSON file.
        data (list): The data to be saved as a list of dictionaries.

    Returns:
        bool: True if the data was saved successfully, False otherwise.
    """
    # Save the updated data back to the JSON file
    try:
        with open(path, "w", encoding=encoding) as jsonfile:
            json.dump(data, jsonfile, indent=4)
            print("Data saved successfully.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return False
    
    return True


def clear_console() -> None:
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Mac and Linux (os.name is 'posix')
    else:
        os.system("clear")