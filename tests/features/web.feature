@web @wikipedia
Feature: Wikipedia Web Browsing
  As a web surfer,
  I want to find information online,
  So I can learn new things and get tasks done.

  Scenario Outline: Basic Wikipedia Search
    Given the Wikipedia home page is displayed
    When the user searches for "<phrase>"
    Then the Wikipedia search result page body header contains "<phrase>"
    And the Wikipedia body content is present
    And the Wikipedia search result page title contains "<phrase>"
    And the Wikipedia search result page URL ends with "/wiki/<phrase>"

    @positive
    Examples: Positive Query
    | phrase     |
    | python     |
    | polar bear |

    @negative
    Examples: Negative Query (intentional fail for Allure demo)
    | phrase     |
    | panda      |
