import os
import random
import time

from django.test import TestCase
import os
from faker.generator import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class WebUtil(TestCase):
    """
    Helper class for executing reusable selenium steps
    """

    __driver = None
    __base_url = None
    delay = 10

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
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_id(element_id).click())
        except TimeoutException as e:
            print("Element is not in expected state")
            raise e

    def send_keys_by_id(self, element_id, text):
        try:
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_id(element_id).send_keys(text))
        except TimeoutException as e:
            print("Element is not in an expected state or rendered correctly")
            raise e

    def click_element_by_name(self, element_name):
        try:
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_name(element_name).click())
        except TimeoutException as e:
            print("Element is not clickable")
            raise e

    def click_element_by_xpath(self, xpath):
        try:
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_xpath(xpath).click())
        except TimeoutException as e:
            print("Element is not clickable ")
            raise e

    def click_element_by_link_text(self, link_text):
        try:
            expected_conditions.element_to_be_clickable(self.get_driver().find_element_by_link_text(link_text).click())
        except TimeoutException as e:
            print("Element is not clickable ")
            raise e

    def wait_until_page_load(self, page_title):
        driver = self.get_driver()
        try:
            WebDriverWait(driver, self.delay).until(
                expected_conditions.title_contains(page_title))
        except TimeoutException as e:
            self.assertEqual(page_title, driver.title)
            raise e

    def assertPageTitleAtTaskSummaryPage(self, expected_title):
        driver = self.get_driver()

        WebDriverWait(driver, self.delay).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//input[@value='Confirm and continue']")))
        self.assertEqual(expected_title, driver.title)

    def assert_page_title_at_task_summary_page(self, expected_title):
        driver = self.get_driver()

        WebDriverWait(driver, self.delay).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//input[@value='Confirm and continue']")))

        self.assertEqual(expected_title, driver.title)

    @staticmethod
    def generate_random_mobile_number():
        """
        Generates a random UK mobile number for testing purposes
        :return: A random UK mobile phone number
        """
        return '0779' + ''.join(str(random.randint(0, 9)) for _ in range(7))
