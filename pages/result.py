"""
This module contains WikipediaResultPage,
The page object for the Wikipedia search result page.
"""

from selenium.webdriver.common.by import By

class WikipediaResultPage:

    # Locators
    PAGE_HEADER = (By.CSS_SELECTOR, 'mw-page-title-main')
    SEARCH_INPUT = (By.ID, 'search_form_input')

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def page_header_value(self):
        page_header = self.browser.find_element(*self.PAGE_HEADER)
        value = page_header.get_attribute('value')
        return value

    def title(self):
        return self.browser.title
