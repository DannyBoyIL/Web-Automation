"""
This module contains WikipediaSearchPage,
The page object for the Wikipedia search page.
"""

from selenium.webdriver.common.by import By
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
        self.browser.get(self.URL)

    def search(self, query):
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(query + Keys.RETURN)
