"""
This module contains WikipediaResultPage,
The page object for the Wikipedia search result page.
"""

from selenium.webdriver.common.by import By

class WikipediaResultPage:

    # Locators
    PAGE_HEADER = (By.ID, 'firstHeading')
    BODY_CONTENT = (By.ID, 'bodyContent')

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def header_value(self):
        page_header = self.browser.find_element(*self.PAGE_HEADER)
        value = page_header.find_element(By.TAG_NAME, 'span').get_attribute("textContent")
        return value

    def body_content(self):
        return self.browser.find_element(*self.BODY_CONTENT)

    def first_paragraph(self):
        page_body = self.browser.find_element(*self.BODY_CONTENT)
        paragraph = page_body.find_element(By.CSS_SELECTOR, '.mw-parser-output > p')
        return paragraph.text.strip()

    def title(self):
        return self.browser.title

    def url(self):
        url = self.browser.current_url
        parts = url.rstrip("/").split("/")
        return "/" + "/".join(parts[-2:])
