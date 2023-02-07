from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Go to homepage
        self.browser.get(self.live_server_url)

        #Does the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #Enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #"type "Buy cribbage boards" into a text box
        inputbox.send_keys('Buy cribbage boards')

        # hitting enter, the page updates and now the page lists "1: Buy cribbage boards" item in to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        #self.assertTrue(
        #    any(row.text == '1: Buy cribbage boards' for row in rows),
        #    f"New to-do item did not appear in table. Contents were:\n{table.text}"
        #)
        self.assertIn('1: Buy cribbage boards', [row.text for row in rows])

        # There is still a text box for another item.  Enter "Use cribbage board to play cribbage"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use cribbage board to play cribbage')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #The page updates and shows both list items.
        self.check_for_row_in_list_table('1: Buy cribbage boards')
        self.check_for_row_in_list_table('2: Use cribbage board to play cribbage')


        #The site has generated a unique URL  -- text explains this has happened

        #visiting the URL the to-do list remains
        self.fail('Finish the test!')
##if __name__ == '__main__':
##    unittest.main()
#The end
