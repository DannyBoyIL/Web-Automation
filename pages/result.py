"""
This module contains WikipediaResultPage,
The page object for the Wikipedia search result page.
"""

from urllib.parse import urlparse

from pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log

class WikipediaResultPage(BasePage):

    # Locators
    PAGE_HEADER = (By.ID, 'firstHeading')
    BODY_CONTENT = (By.ID, 'bodyContent')

    def __init__(self, browser):
        super().__init__(browser)
        log.info("Initialized WikipediaResultPage object.")

    # Interaction Methods

    def header_value(self):
        log.info("Attempting to get the page header value.")
        page_header = WebDriverWait(self.browser, 15).until(
            EC.visibility_of_element_located(self.PAGE_HEADER)
        )
        log.debug(f"Found element with locator: {self.PAGE_HEADER}")
        value = page_header.find_element(By.TAG_NAME, 'span').get_attribute("textContent")
        log.info(f"Retrieved page header value: '{value}'")
        return value

    def body_content(self):
        log.info("Attempting to find the main body content element.")
        element = WebDriverWait(self.browser, 15).until(
            EC.visibility_of_element_located(self.BODY_CONTENT)
        )
        log.debug(f"Body content element located.")
        return element

    def title(self):
        title = self.browser.title
        log.info(f"Retrieved page title: '{title}'")
        return title

    def url(self):
        raw = self.browser.current_url
        path = urlparse(raw).path.rstrip("/")
        log.info(f"Retrieved current URL path: '{path}'")
        return path
