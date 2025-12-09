"""
This module contains shared fixtures.
"""

import json
import pytest
import selenium.webdriver
from selenium.webdriver import SafariOptions

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
    yield browser

    # Quit the WebDriver instance for the cleanup
    browser.quit()