"""
These tests cover Wikipedia searches.
"""

import pytest

from pages.result import WikipediaResultPage
from pages.search import WikipediaSearchPage

@pytest.mark.parametrize('phrase', ['python', 'polar bear'])#, 'panda'])
def test_basic_wikipedia_search(browser, phrase):
    search_page = WikipediaSearchPage(browser)
    result_page = WikipediaResultPage(browser)

    # Given the Wikipedia home page is displayed
    search_page.load()

    # When the user searches for "panda"
    search_page.search(phrase)

    # Then the search result page body header contains "python"
    assert  phrase == result_page.header_value().lower()

    # And content body is present
    assert result_page.body_content().is_displayed()

    # And the search result page title contains "python"
    assert result_page.title().lower().find(phrase) != -1

    # And the URL ends with "/wiki/Python"
    assert result_page.url().lower().endswith(f"wiki/{phrase.replace(" ", "_")}")

    # raise Exception("Incomplete test")