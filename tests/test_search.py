"""
These tests cover Wikipedia searches.
"""

import pytest

from pages.result import WikipediaResultPage
from pages.search import WikipediaSearchPage

@pytest.mark.parametrize('phrase', ['panda'])#, 'python', 'polar bear'])
def test_basic_duckduckgo_search(browser, phrase):
    search_page = WikipediaSearchPage(browser)
    result_page = WikipediaResultPage(browser)

    # Given the Wikipedia home page is displayed
    search_page.load()

    # When the user searches for "panda"
    search_page.search(phrase)

    # Then the redirect search result is "panda"
    assert  phrase == result_page.page_header_value()

    # And the search result query is "panda"
    assert  phrase == result_page.page_header_value()

    # And the search result title contains "panda"
    assert phrase in result_page.title()

    # raise Exception("Incomplete test")