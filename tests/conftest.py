"""
This module contains shared fixtures.
"""

import pytest
import json
import yaml
import allure
import os
import selenium.webdriver as webdriver
from utils.logger import log


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for tests: chrome | firefox | headless"
    )

    parser.addoption(
        "--implicit-wait",
        action="store",
        default=10,
        type=int,
        help="Implicit wait time in seconds"
    )


def load_grid_url_from_docker_compose():

    with open("docker-compose.yml", "r") as f:
        compose = yaml.safe_load(f)

    hub = compose["services"]["selenium-hub"]

    # Extract port mapping (e.g., "4444:4444")
    port_mapping = hub["ports"][0]
    host_port = port_mapping.split(":")[0]

    return f"http://localhost:{host_port}/wd/hub"


@pytest.fixture(scope="session")
def config(pytestconfig):

    grid_url = load_grid_url_from_docker_compose()

    # Read CLI args
    browser = pytestconfig.getoption("--browser")
    implicit_wait = pytestconfig.getoption("--implicit-wait")

    # Validate
    assert browser in ["chrome", "firefox", "headless"], f"Invalid browser: {browser}"
    assert implicit_wait > 0

    return {
        "grid_url": grid_url,
        "browser": browser,
        "implicit_wait": implicit_wait
    }


@pytest.fixture(scope="session")
def json_config():

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

    grid_url = config["grid_url"]
    browser_name = config["browser"]

    # Initialize the WebDriver instance

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()

    elif browser_name == "safari":
        options = webdriver.SafariOptions()

    elif browser_name == "headless":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    else:
        raise Exception(f"Unsupported browser: {browser_name}")

    browser = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )

    # Make its calls wait up to 10 seconds for elements to appear
    browser.implicitly_wait(config['implicit_wait'])

    # Return the WebDriver instance for the setup
    log.info("Setting up and initializing WebDriver browser for the test...")
    yield browser

    # Quit the WebDriver instance for the cleanup
    log.info("Tearing down WebDriver browser.")
    browser.quit()


@pytest.fixture
def json_browser(json_config):

    # Initialize the WebDriver instance
    if json_config['browser'] == 'chrome':
        browser = webdriver.Chrome()
    elif json_config['browser'] == 'firefox':
        browser = webdriver.Firefox()
    elif json_config['browser'] == 'safari':
        opts = webdriver.SafariOptions()
        opts.set_capability("safari:useNonPersistentSession", True)
        browser = webdriver.Safari(options=opts)
    elif json_config['browser'] == 'Headless Chrome':
        opts = webdriver.ChromeOptions()
        opts.add_argument('headless')
        # opts.add_argument('--headless')
        # opts.headless = True
        browser = webdriver.Chrome(options=opts)
    else:
        raise Exception(f"Unsupported browser: {json_config['browser']}")

    # Make its calls wait up to 10 seconds for elements to appear
    browser.implicitly_wait(json_config['implicit_wait'])

    # Return the WebDriver instance for the setup
    log.info("Setting up and initializing WebDriver browser for the test...")
    yield browser

    # Quit the WebDriver instance for the cleanup
    log.info("Tearing down WebDriver browser.")
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        # Grab the WebDriver even for BDD-style tests
        try:
            driver = item._request.getfixturevalue("browser")
        except Exception as e:
            # Prevents Pytest failure for screenshots
            log.error(f"An error occurred during screenshot process: {e}")
            driver = None
            pass

        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            test_name = report.nodeid.replace("::", "_").replace("/", "_").replace(".py", "")
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}_FAILURE.png")

            # Save screenshot to disk
            driver.save_screenshot(screenshot_path)

            # Log
            log.error(f"Screenshot saved to: {screenshot_path}")

            # Attach to Allure
            allure.attach.file(
                screenshot_path,
                name=f"Failure Screenshot - {test_name}",
                attachment_type=allure.attachment_type.PNG,
            )
        else:
            log.warning("WebDriver unavailable; screenshot not saved.")
