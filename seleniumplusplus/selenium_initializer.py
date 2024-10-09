# driver_initializer.py
from typing import Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os
import csv
import json

from selenium.webdriver.chrome.webdriver import WebDriver


def init_driver(url) -> WebDriver:
    """
    Initialize the WebDriver with specified options and navigate to the given URL.

    Args:
        url (str): The URL to navigate to.

    Returns:
        WebDriver: The initialized WebDriver instance.
    """
    opt = Options()
    opt.add_argument("--search-engine-choice-country")
    opt.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(options=opt)
    driver.maximize_window()
    try:
        driver.get(url)
    except Exception as e:
        print("Error navigating to URL:", e)
        driver.quit()
    time.sleep(2)
    return driver


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


def save_csv(path, data, delimiter = ";", encoding = "utf-8") -> None:
    """
    Saves the data to a CSV file at the specified path.

    Args:
        path (str): The path to the CSV file.
        data (list): The data to be saved as a list of dictionaries.
        delimiter (str): The delimiter to use for separating fields in the CSV file. Default is ";".
        encoding (str): The encoding to use for the CSV file. Default is "utf-8".

    Returns:
        bool: True if the data was saved successfully, False otherwise.
    """
    # Save the updated data back to the CSV file
    try:
        with open(path, "w", newline="", encoding=encoding) as csvfile:
            fieldnames = [
                key for key in data[0].keys()
            ]  # Get the fieldnames from the first row
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
            print("Data saved successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


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