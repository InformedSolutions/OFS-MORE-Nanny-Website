import random
import time

from django.test import TestCase
import os
from faker.generator import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class WebUtil(TestCase):
    """
    Helper class for executing reusable selenium steps
    """

    __driver = None
    __base_url = None
    delay = 15

    def __init__(self, driver, base_url, *args, **kwargs):
        """
        Default constructor
        :param driver: the selenium driver to be used for executing steps
        :param base_url: the base url against which tests are to be executed
        """
        self.__driver = driver
        self.__base_url = base_url
        super(WebUtil, self).__init__(*args, **kwargs)

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

    def click_element_by_id(self, element_id):
        try:
            element = WebDriverWait(self.get_driver(), self.delay).until(
                ec.element_to_be_clickable((By.ID, element_id)))
            element.click()
        except TimeoutException as e:
            print("Element is not in expected state")
            raise e

    def send_keys_by_id(self, element_id, text):
        try:
            element = WebDriverWait(self.get_driver(), self.delay).until(
                ec.element_to_be_clickable((By.ID, element_id)))
            element.send_keys(text)
        except TimeoutException as e:
            print("Element is not in an expected state or rendered correctly")
            raise e

    def click_element_by_name(self, element_name):
        try:
            element = WebDriverWait(self.get_driver(), self.delay).until(
                ec.element_to_be_clickable((By.NAME, element_name)))
            element.click()
        except TimeoutException as e:
            print("Element is not clickable")
            raise e

    def click_element_by_xpath(self, xpath):
        try:
            element = WebDriverWait(self.get_driver(), self.delay).until(
                ec.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except TimeoutException as e:
            print("Element is not clickable ")
            raise e

    def click_element_by_link_text(self, link_text):
        try:
            element = WebDriverWait(self.get_driver(), self.delay).until(
                ec.presence_of_element_located((By.LINK_TEXT, link_text)))
            element.click()
        except TimeoutException as e:
            print("Element is not clickable ")
            raise e

    def wait_until_page_load(self, page_title):
        driver = self.get_driver()
        try:
            WebDriverWait(driver, self.delay).until(
                ec.title_contains(page_title))
        except TimeoutException as e:
            self.assertEqual(page_title, driver.title)
            raise e

    def assert_page_title(self, expected):
        self.wait_until_page_load(expected)
        driver = self.get_driver()
        expected_title = expected
        actual_title = driver.title
        self.assertEqual(expected_title, actual_title)

    def is_return_link_present(self):
        """
        Tests 'Return to list' link is present in the page
        :return: True if the link is present
        """
        try:
            self.get_driver().find_element_by_link_text("Return to list").is_displayed()
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def generate_random_mobile_number():
        """
        Generates a random UK mobile number for testing purposes
        :return: A random UK mobile phone number
        """
        return '0779' + ''.join(str(random.randint(0, 9)) for _ in range(7))
