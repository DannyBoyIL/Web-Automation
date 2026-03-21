"""
This module contains WikipediaSearchPage,
The page object for the Wikipedia search page.
"""

from utils.logger import log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

class WikipediaSearchPage:

    # URL
    URL = 'https://www.wikipedia.com/'

    # Locators
    SEARCH_INPUT = (By.ID, 'searchInput')

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
    def load(self):
        log.info("Loading Wikipedia Search Page")
        self.browser.get(self.URL)

    def search(self, query):
        log.info(f"Attempting to search for: {query}")
        try:
            search_input = WebDriverWait(self.browser, 15).until(
                EC.visibility_of_element_located(self.SEARCH_INPUT)
            )
            search_input.send_keys(query + Keys.RETURN)
            log.debug("Query successfully entered into search field.")
        except Exception as e:
            log.error(f"Failed to perform search: {e}")
            raise e
