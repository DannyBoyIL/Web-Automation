"""
These tests cover Wikipedia searches.
"""

import pytest

from pages.result import WikipediaResultPage
from pages.search import WikipediaSearchPage

@pytest.mark.parametrize('phrase', ['python', 'panda', 'polar bear'])
def test_basic_wikipedia_search(browser, phrase):
    search_page = WikipediaSearchPage(browser)
    result_page = WikipediaResultPage(browser)
    PHRASE = 'python'

    # Given the Wikipedia home page is displayed
    search_page.load()

    # When the user searches for "panda"
    search_page.search(PHRASE)

    # Then the search result page body header contains "python"
    assert  PHRASE == result_page.header_value().lower()

    # And content body is present
    assert result_page.body_content().is_displayed()

    # And the first paragraph exists and has text
    assert result_page.first_paragraph().lower().find(PHRASE) != -1

    # And the search result page title contains "python"
    assert result_page.title().lower().find(PHRASE) != -1

    # And the URL ends with "/wiki/Python"
    assert result_page.url().lower().endswith(f"wiki/{PHRASE}")

    # raise Exception("Incomplete test")