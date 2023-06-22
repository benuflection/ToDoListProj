from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
#User = get_user_model()


class MyListsTest(FunctionalTest):


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # email = 'edith@example.com'
        # self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_out(email)
        #
        # #Edith is a Logged-in user
        # self.create_pre_authenticated_session(email)
        # self.browser.get(self.live_server_url)
        # self.wait_to_be_logged_in(email)

        # Edith is a logged in user
        self.create_pre_authenticated_session('edith@example.com')

        # She goes to the homepage and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # She notices a "my lists" link
        self.browser.find_element('link text', 'My lists').click()

        # She sees that her list is in there, named after its first list item
        self.wait_for(
            lambda: self.browser.find_element('link text', 'Reticulate splines')
        )
        self.browser.find_element('link text', 'Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under 'my Lists", her new list appears
        self.browser.find_element('link text', 'My lists').click()
        self.wait_for(
            lambda: self.browser.find_element('link text', 'Click cows')
        )
        self.browser.find_element('link text', 'Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "my lists" option disappears
        self.browser.find_element('link text', 'Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements('link text', 'My lists'),
            []
        ))