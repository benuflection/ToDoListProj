from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith submits and empty list item, home page represhes. there is an error message
        # She tries again with a real item which works. she tries another empty list item: another error message.

        self.fail('write me!')
#The end
