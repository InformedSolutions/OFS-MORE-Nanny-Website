from django.test import TestCase


class Login(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(Login, self).__init__(*args, **kwargs)

    def login_to_the_application(self, phone_number, additional_phone_number):
        """
        Selenium steps to create a new application by completing the login details task
        :param email_address: the email address to be registered
        :param phone_number: the phone number to be registered
        :param additional_phone_number: an optional additional phone number to be registered
        """
        self.task_executor.navigate_to_email_validation_url()

        driver = self.task_executor.get_driver()

        self.task_executor.send_keys_by_id("id_mobile_number", phone_number)

        if additional_phone_number is not None:
            self.task_executor.send_keys_by_id("id_other_phone_number", additional_phone_number)

        self.task_executor.click_element_by_xpath("//input[@value='Continue']")

        # Summary page
        self.task_executor.click_element_by_xpath("//input[@value='Continue']")
