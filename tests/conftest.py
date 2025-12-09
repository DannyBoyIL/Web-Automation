"""
This module contains shared fixtures.
"""

import json
import pytest
import allure
import os
import selenium.webdriver
from selenium.webdriver import SafariOptions
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import log

@pytest.fixture(scope="session")
def config():

    # Read the file
    with open("config.json") as f:
        config = json.load(f)

    # Assert values are acceptable
    assert config['browser'] in ['chrome', 'firefox', 'safari', 'opera', 'edge', 'Headless Chrome']
    assert isinstance(config['implicit_wait'], int)
    assert config['implicit_wait'] > 0

    # Return config for use
    return config

@pytest.fixture
def browser(config):

    # Initialize the ChromeDriver instance
    if config['browser'] == 'chrome':
        browser = selenium.webdriver.Chrome()
    elif config['browser'] == 'firefox':
        browser = selenium.webdriver.Firefox()
    elif config['browser'] == 'safari':
        opts = SafariOptions()
        opts.set_capability("safari:useNonPersistentSession", True)
        browser = selenium.webdriver.Safari(options=opts)
    elif config['browser'] == 'Headless Chrome':
        opts = selenium.webdriver.ChromeOptions()
        opts.add_argument('headless')
        #opts.add_argument('--headless')
        #opts.headless = True
        browser = selenium.webdriver.Chrome(options=opts)
    else:
        raise Exception(f"Unsupported browser: {config['browser']}")


    # Make its calls wait up to 10 seconds for elements to appear
    browser.implicitly_wait(config['implicit_wait'])

    # Return the WebDriver instance for the setup
    log.info("Setting up and initializing WebDriver browser for the test...")
    yield browser

    # Quit the WebDriver instance for the cleanup
    log.info("Tearing down WebDriver browser.")
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook for each test case that creates a report and a screenshot.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:

        # Screenshot handler
        try:
            driver: WebDriver = item.funcargs.get('browser')

            if driver:
                # File path
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                test_name = report.nodeid.replace("::", "_").replace("/", "_").replace(".py", "")
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_FAILURE.png")

                # Save screenshot
                driver.save_screenshot(screenshot_path)
                log.error(f"Test '{test_name}' failed. Screenshot saved to: {screenshot_path}")

                # Append to Allure report
                allure.attach.file(
                    screenshot_path,
                    name=f"Failure Screenshot: {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
            else:
                log.warning("Driver object not available for screenshot capture.")

        except Exception as e:
            # Prevents Pytest failure for screenshots
            log.error(f"An error occurred during screenshot process: {e}")
            pass