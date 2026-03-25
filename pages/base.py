"""
Base page class shared by all page objects.
"""

class BasePage:

    def __init__(self, browser):
        self.browser = browser
