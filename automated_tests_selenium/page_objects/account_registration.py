import faker
from django.test import TestCase


class Registration(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(Registration, self).__init__(*args, **kwargs)

    def register_email_address(self, email_address):
        """
        Selenium steps for registering an email address against an application
        """
        self.task_executor.click_element_by_xpath("//input[@value='Sign in']")
        self.task_executor.click_element_by_id("id_account_selection_0-label")
        self.task_executor.click_element_by_xpath("//input[@value='Continue']")
        self.task_executor.click_element_by_id("id_email_address")
        self.task_executor.send_keys_by_id("id_email_address", email_address)
        self.task_executor.click_element_by_xpath("//input[@value='Continue']")
