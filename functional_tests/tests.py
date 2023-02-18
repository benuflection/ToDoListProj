from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#import unittest
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element('id', 'id_list_table')
                rows = table.find_elements('tag name', 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_for_one_user(self):
        #Go to homepage
        self.browser.get(self.live_server_url)

        #Does the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element('tag name', 'h1').text
        self.assertIn('To-Do', header_text)

        #Enter a to-do item
        inputbox = self.browser.find_element('id', 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #"type "Buy cribbage boards" into a text box
        inputbox.send_keys('Buy cribbage boards')

        # hitting enter, the page updates and now the page lists "1: Buy cribbage boards" item in to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cribbage boards')

######This Section commented out 2/17/23
        # table = self.browser.find_element('id', 'id_list_table')
        # rows = table.find_elements('tag name', 'tr')
        #
        # self.assertIn('1: Buy cribbage boards', [row.text for row in rows])

        # There is still a text box for another item.  Enter "Use cribbage board to play cribbage"
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Use cribbage board to play cribbage')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)

        self.wait_for_row_in_list_table('2: Use cribbage board to play cribbage')
        self.wait_for_row_in_list_table('1: Buy cribbage boards')


        #The page updates and shows both list items.


    def test_multiple_users_can_start_lists_at_different_urls(self):
        #User starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Buy cribbage boards')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cribbage boards')

        #The site has generated a unique URL  -- text explains this has happened
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Frank, a new user, visits the site
        #we use a new browser session so no cookies etc. are held over
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Frank visits homepage: no sign of edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element('tag name', 'body').text
        self.assertNotIn('Buy cribbage boards', page_text)
        self.assertNotIn('Use cribbage board to play cribbage', page_text)

        #Frank enters a new item
        inputbox = self.browser.find_element('id', 'id_new_item')
        inputbox.send_keys('Buy food')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy food')

        # Frank gets his own URL
        frank_list_url = self.browser.current_url
        self.assertRegex(frank_list_url, '/lists/.+')
        self.assertNotEqual(frank_list_url, edith_list_url)

        #no trace of previous list
        page_text = self.browser.find_element('tag name', 'body').text
        self.assertNotIn('Buy cribbage boards', page_text)
        self.assertIn('Buy food', page_text)
        #visiting the URL the to-do list remains


        #self.fail('Finish the test!')

#The end
