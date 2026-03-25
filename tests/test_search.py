"""
These tests cover Wikipedia searches.
"""

import pytest
import allure

from pages.result import WikipediaResultPage
from pages.search import WikipediaSearchPage

@pytest.mark.parametrize('phrase', ['python', 'polar bear'])#, 'panda'])
def test_basic_wikipedia_search(json_browser, phrase):

    allure.dynamic.title(f"Basic Wikipedia search: {phrase}")

    search_page = WikipediaSearchPage(json_browser)
    result_page = WikipediaResultPage(json_browser)

    with allure.step("Load Wikipedia home page"):
        search_page.load()
        allure.attach(json_browser.current_url, "Loaded URL", allure.attachment_type.TEXT)

    with allure.step(f"Search Wikipedia for '{phrase}'"):
        search_page.search(phrase)
        allure.attach(phrase, "Search phrase", allure.attachment_type.TEXT)

    with allure.step(f"Validate result page header contains '{phrase}'"):
        header = result_page.header_value().lower()
        allure.attach(header, "Header text", allure.attachment_type.TEXT)
        assert phrase == header, f"Expected: '{phrase}', Actual: '{header}'"

    with allure.step("Check that #bodyContent exists and is visible"):
        is_visible = result_page.body_content().is_displayed()
        allure.attach(str(is_visible), "Body content visible?", allure.attachment_type.TEXT)
        assert is_visible, "Body content is not visible"

    with allure.step(f"Validate page title contains '{phrase}'"):
        page_title = result_page.title().lower()
        allure.attach(page_title, "Page title", allure.attachment_type.TEXT)
        assert phrase in page_title, f"'{phrase}' not found in '{page_title}'"

    with allure.step(f"Validate URL ends with '/wiki/{phrase}'"):
        expected = f"wiki/{phrase.replace(' ', '_')}"
        actual = result_page.url().lower()
        allure.attach(actual, "Current URL", allure.attachment_type.TEXT)
        allure.attach(expected, "Expected ending", allure.attachment_type.TEXT)
        assert actual.endswith(expected), f"Expected URL to end with '{expected}' but got '{actual}'"
