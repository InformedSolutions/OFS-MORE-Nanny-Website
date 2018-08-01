import json
import os
import random
import time
from unittest import mock

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class TaskExecutor:
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

    def complete_your_login_details(self, email_address, phone_number, additional_phone_number):
        """
        Selenium steps to create a new application by completing the login details task
        :param email_address: the email address to be registered
        :param phone_number: the phone number to be registered
        :param additional_phone_number: an optional additional phone number to be registered
        """
        self.register_email_address(email_address)
        self.navigate_to_email_validation_url()

        driver = self.get_driver()

        self.type_into_field_by_id("id_mobile_number", phone_number)

        if additional_phone_number is not None:
            driver.find_element_by_id("id_other_phone_number").send_keys(additional_phone_number)

        driver.find_element_by_xpath("//input[@value='Continue']").click()

        # Summary page
        driver.find_element_by_xpath("//input[@value='Continue']").click()

    def register_email_address(self, email_address):
        """
        Selenium steps for registering an email address against an application
        """
        driver = self.get_driver()
        driver.find_element_by_xpath("//input[@value='Sign in']").click()
        driver.find_element_by_id("id_account_selection_0-label").click()
        driver.find_element_by_xpath("//input[@value='Continue']").click()
        driver.find_element_by_id("id_email_address").click()
        driver.find_element_by_id("id_email_address").send_keys(email_address)
        driver.find_element_by_xpath("//input[@value='Continue']").click()

    def click_element_by_id(self, element_id):
        try:
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_id(element_id).click())
        except TimeoutException:
            print("Element is not clickable")

    def click_element_by_xpath(self, xpath):
        try:
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_xpath(xpath).click())
        except TimeoutException:
            print("Element is not clickable ")

    def type_into_field_by_id(self, element_id, text):

        try:
            expected_conditions.element_to_be_clickable(
                    self.get_driver().find_element_by_id(element_id).send_keys(text))
        except TimeoutException:
            print("Element is not in expected state to type")

    @staticmethod
    def generate_random_mobile_number():
        """
        Generates a random UK mobile number for testing purposes
        :return: A random UK mobile phone number
        """
        return '0779' + ''.join(str(random.randint(0, 9)) for _ in range(7))
