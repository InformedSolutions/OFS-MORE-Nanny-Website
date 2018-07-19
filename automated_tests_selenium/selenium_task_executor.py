import json
import os
import random
import time
from unittest import mock

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumTaskExecutor:
    """
    Helper class for executing reusable selenium steps
    """

    __driver = None
    __base_url = None

    def __init__(self, driver, base_url):
        """
        Default constructor
        :param driver: the selenium driver to be used for executing steps
        :param base_url: the base url against which tests are to be executed
        """
        self.__driver = driver
        self.__base_url = base_url

    def set_driver(self, driver):
        """
        Method for setting the Selenium driver instance to use for testing purposes
        :param driver: the selenium driver instance to use for testing purposes
        """
        self.__driver = driver

    def get_driver(self):
        """
        Method for getting the current Selenium driver instance
        :return: Current Selenium driver instance
        """
        if self.__driver is None:
            raise Exception("A Selenium driver has not been set. Please use the set_driver method to "
                            "configure which driver to use for tests.")
        return self.__driver

    def set_base_url(self, base_url):
        """
        Method for setting the base url against which tests will be executed
        :param base_url: the base url against which tests will be executed
        """
        self.__base_url = base_url

    def get_base_url(self):
        """
        Method for getting the base url against which tests will be executed
        :return: the base url against which tests will be executed
        """
        if self.__base_url is None:
            raise Exception("No base URL for tests has been set. Please use the set_base_url method"
                            "to configure an appropriate target URL.")
        return self.__base_url

    def navigate_to_base_url(self):
        """
        Method for navigating to the base url of a site
        """
        driver = self.get_driver()
        driver.get(self.__base_url)

    def register_email_address(self, email_address):
        """
        Selenium steps for registering an email address against an application
        """
        driver = self.get_driver()
        driver.find_element_by_xpath("//input[@value='Sign in']").click()
        driver.find_element_by_id("id_acc_selection_0-label").click()
        driver.find_element_by_xpath("//input[@value='Continue']").click()

        driver.find_element_by_id("id_email_address").send_keys(email_address)
        driver.find_element_by_xpath("//input[@value='Continue']").click()

    def sign_back_in(self, email_address):
        """
        Selenium steps for signing back into an application
        :param email_address: the email address to be used during the sign in process.
        """
        driver = self.get_driver()
        self.navigate_to_base_url()
        driver.find_element_by_xpath("//input[@value='Sign in']").click()
        driver.find_element_by_id("id_acc_selection_1-label").click()
        driver.find_element_by_xpath("//input[@value='Continue']").click()

        driver.find_element_by_id("id_email_address").send_keys(email_address)
        driver.find_element_by_xpath("//input[@value='Continue']").click()

        WebDriverWait(driver, 10).until(
            expected_conditions.title_contains("Check your email"))

        self.navigate_to_email_validation_url()
        sms_validation_code = os.environ.get('SMS_VALIDATION_CODE')
        driver.find_element_by_id("id_magic_link_sms").send_keys(sms_validation_code)
        driver.find_element_by_xpath("//input[@value='Continue']").click()

    def navigate_to_SMS_validation_page(self, email_address):
        '''
        Selenium steps for signing back into the application, but stopping at SMS validation page unlike sign_back_in()
        :param email_address: Email address to be used during the sign in process.
        '''
        driver = self.get_driver()
        # Start sign in process.
        self.navigate_to_base_url()
        driver.find_element_by_xpath("//input[@value='Sign in']").click()
        driver.find_element_by_id("id_acc_selection_1-label").click()
        driver.find_element_by_xpath("//input[@value='Continue']").click()

        # Generate new validation link (was previously used in standard_eyfs_application).
        driver.find_element_by_id("id_email_address").send_keys(email_address)
        driver.find_element_by_xpath("//input[@value='Continue']").click()

        WebDriverWait(driver, 10).until(
            expected_conditions.title_contains("Check your email"))

        # Reach SMS validation page.
        self.navigate_to_email_validation_url()

    def navigate_to_email_validation_url(self):
        """
        Selenium steps for navigating to the email validation page in the login journey
        """
        driver = self.get_driver()
        validation_url = os.environ.get('EMAIL_VALIDATION_URL')

        if validation_url is None:
            time.sleep(1)
            return self.navigate_to_email_validation_url()

        driver.get(validation_url)

        return validation_url

    def complete_mandatory_registration(self):
        pass



    @staticmethod
    def generate_random_mobile_number():
        """
        Generates a random UK mobile number for testing purposes
        :return: A random UK mobile phone number
        """
        return '0779' + ''.join(str(random.randint(0, 9)) for _ in range(7))
