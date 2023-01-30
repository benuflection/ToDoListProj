from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Go to homepage
        self.browser.get('http://localhost:8000')

        #Does the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #Enter a to-do item

 #browser = webdriver.Firefox()


 #browser.get('http://localhost:8000')

#assert 'Django' in browser.title

#Does the page title and header mention to-do lists
 #assert 'To-Do' in browser.title


#"type "Buy cribbage boards" into a text box

# hitting enter, the page updates and now the page lists "1: Buy cribbage boards" item in to-do list

# There is still a text box for another item.  Enter "Use cribbage board to play cribbage"

#The page updates and shows both list items.

#The site has generated a unique URL  -- text explains this has happened

#visiting the URL the to-do list remains
if __name__ == '__main__':
    unittest.main()
#The end

