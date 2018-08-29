import faker
from django.test import TestCase


class Registration(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(Registration, self).__init__(*args, **kwargs)

    def register_email_address(self, email_address):
        """
        Selenium steps for registering an email address against an application
        """
        self.web_util.click_element_by_xpath("//input[@value='Sign in']")
        self.web_util.click_element_by_id("id_account_selection_0-label")
        self.web_util.click_element_by_xpath("//input[@value='Continue']")
        self.web_util.click_element_by_id("id_email_address")
        self.web_util.send_keys_by_id("id_email_address", email_address)
        self.web_util.click_element_by_xpath("//input[@value='Continue']")
        self.web_util.wait_until_page_load('Check your email')
