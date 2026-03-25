"""
This module contains step definitions for web.feature.
"""

import allure
from pytest_bdd import scenarios, when, then, parsers, given
from pages.result import WikipediaResultPage
from pages.search import WikipediaSearchPage

# Scenarios

scenarios('../features/web.feature')

# Given Steps

@given(parsers.parse('the Wikipedia home page is displayed'))
@allure.step("Load Wikipedia home page")
def load(browser):
    search_page = WikipediaSearchPage(browser)
    search_page.load()
    allure.attach(browser.current_url, "Loaded URL", allure.attachment_type.TEXT)

# When Steps

@when(parsers.parse('the user searches for "{phrase}"'))
@allure.step("Search Wikipedia for '{phrase}'")
def search(browser, phrase):
    search_page = WikipediaSearchPage(browser)
    search_page.search(phrase)
    allure.attach(phrase, "Search phrase", allure.attachment_type.TEXT)

# Then Steps

@then(parsers.parse('the Wikipedia search result page body header contains "{phrase}"'))
@allure.step("Validate result page header contains '{phrase}'")
def header_value(browser, phrase):
    result_page = WikipediaResultPage(browser)
    header = result_page.header_value().lower()

    allure.attach(header, "Header text", allure.attachment_type.TEXT)

    assert phrase == header, f"Expected: '{phrase}', Actual: '{header}'"

@then(parsers.parse('the Wikipedia body content is present'))
@allure.step("Check that #bodyContent exists and is visible")
def content(browser):
    result_page = WikipediaResultPage(browser)
    content = result_page.body_content()

    is_visible = content.is_displayed()
    allure.attach(str(is_visible), "Body content visible?", allure.attachment_type.TEXT)

    assert is_visible, "Body content is not visible"

@then(parsers.parse('the Wikipedia search result page title contains "{phrase}"'))
@allure.step("Validate page title contains '{phrase}'")
def title(browser, phrase):
    result_page = WikipediaResultPage(browser)
    page_title = result_page.title().lower()

    allure.attach(page_title, "Page title", allure.attachment_type.TEXT)

    assert phrase in page_title, f"'{phrase}' not found in '{page_title}'"

@then(parsers.parse('the Wikipedia search result page URL ends with "/wiki/{phrase}"'))
@allure.step("Validate URL ends with '/wiki/{phrase}'")
def url(browser, phrase):
    result_page = WikipediaResultPage(browser)
    expected = f"wiki/{phrase.replace(' ', '_')}"
    actual = result_page.url().lower()

    allure.attach(actual, "Current URL", allure.attachment_type.TEXT)
    allure.attach(expected, "Expected ending", allure.attachment_type.TEXT)

    assert actual.endswith(expected), f"Expected URL to end with '{expected}' but got '{actual}'"
