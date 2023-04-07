from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith submits and empty list item,

        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # home page refreshes. there is an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element('css selector', '.has-error').text,
            "You can't have an empty list item"
        ))
        #She tries again with a real item which works.
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #  she tries another empty list item.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Gets another error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element('css selector', '.has-error').text,
            "You can't have an empty list item"
        ))

        # She can fill some text in
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

        self.fail('Finish the test!')
#The end
