from django.test import TestCase


class Login(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(Login, self).__init__(*args, **kwargs)

    def login_to_the_application(self, phone_number, additional_phone_number):
        """
        Selenium steps to create a new application by completing the login details task
        :param phone_number: the phone number to be registered
        :param additional_phone_number: an optional additional phone number to be registered
        """
        self.web_util.navigate_to_email_validation_url()

        driver = self.web_util.get_driver()

        self.web_util.send_keys_by_id("id_mobile_number", phone_number)

        if additional_phone_number is not None:
            self.web_util.send_keys_by_id("id_other_phone_number", additional_phone_number)

        self.web_util.click_element_by_xpath("//input[@value='Continue']")

        # Summary page
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='account_details']/td/a/strong").text)

    def navigate_to_SMS_validation_page(self, email_id):
        """
        Selenium steps for signing back into the application, but stopping at SMS validation page unlike sign_back_in()
        :param email_id: Email address to be used during the sign in process.
        """
        # Start sign in process.
        self.web_util.navigate_to_base_url()
        self.web_util.click_element_by_xpath("//input[@value='Sign in']")
        self.web_util.click_element_by_id("id_account_selection_0-label")
        self.web_util.click_element_by_xpath("//input[@value='Continue']")
        self.web_util.click_element_by_id("id_email_address")
        self.web_util.send_keys_by_id("id_email_address", email_id)
        self.web_util.click_element_by_xpath("//input[@value='Continue']")
        self.web_util.wait_until_page_load("Check your email")

        # Reach SMS validation page.
        self.web_util.navigate_to_email_validation_url()


