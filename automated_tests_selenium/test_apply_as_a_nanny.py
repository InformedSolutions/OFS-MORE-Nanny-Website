"""
Selenium test cases for the Childminder service
"""

import os
import random
import time
from datetime import datetime

from django.core.management import call_command
from django.test import LiveServerTestCase, override_settings, tag
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from .selenium_task_executor import SeleniumTaskExecutor

from faker import Faker

# Configure faker to use english locale
faker = Faker('en_GB')
selenium_driver_out = None


def try_except_method(func):
    """
    :param func: assert method to be used in try/except statement
    :return: decorated method to use in try/except statement
    """

    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            capture_screenshot(func)
            raise e

    return func_wrapper


def capture_screenshot(func):
    global selenium_driver_out
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    scr = selenium_driver_out.find_element_by_tag_name('html')
    scr.screenshot('selenium/screenshot-%s-%s.png' % (func.__name__, now))


@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class ApplyAsAChildminder(LiveServerTestCase):
    port = 8000

    if os.environ.get('LOCAL_SELENIUM_DRIVER') == 'True':
        host = '127.0.0.1'
    else:
        host = '0.0.0.0'

    current_year = datetime.now().year

    def setUp(self):
        base_url = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS')
        # "http://0.0.0.0:8000/nanny/sign-in/new-application/"

        if os.environ.get('LOCAL_SELENIUM_DRIVER') == 'True':
            # If running on a windows host, make sure to drop the
            # geckodriver.exe into your Python/Scripts installation folder
            self.launch_local_browser()
        else:
            # If not using local driver, default requests to a selenium grid server
            self.launch_remote_browser()

        self.selenium_driver.implicitly_wait(30)

        self.verification_errors = []
        self.accept_next_alert = True

        self.selenium_task_executor = SeleniumTaskExecutor(self.selenium_driver, base_url)

        global selenium_driver_out
        selenium_driver_out = self.selenium_driver

        super(ApplyAsAChildminder, self).setUp()

    def launch_local_browser(self):
        """
        If the HEADLESS_CHROME value in Environment variables is set to true then it will launch chrome headless
        browser, else it will launch firefox.
        """

        if os.environ.get('HEADLESS_CHROME') == 'True':
            path_to_chromedriver = '/usr/lib/chromium-browser/chromedriver'
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            self.selenium_driver = webdriver.Chrome(path_to_chromedriver, chrome_options=chrome_options)
        else:
            self.selenium_driver = webdriver.Firefox()
        self.selenium_driver.maximize_window()

    def launch_remote_browser(self):
        """
        If the HEADLESS_CHROME value in Environment variables is set to true then it will launch chrome headless
        browser, else it will launch firefox.
        """

        if os.environ.get('HEADLESS_CHROME') == 'True':
            self.selenium_driver = webdriver.Remote(
                command_executor=os.environ['SELENIUM_HOST'],
                desired_capabilities={'platform': 'ANY', "headless": 'true', 'browserName': 'chrome', 'version': ''}
            )

        else:
            self.selenium_driver = webdriver.Remote(
                command_executor=os.environ['SELENIUM_HOST'],
                desired_capabilities={'platform': 'ANY', 'browserName': 'firefox', 'version': ''}
            )
            self.selenium_driver.maximize_window()

    @tag('ragha')
    @try_except_method
    def test_untitled_test_case(self):
        """
        Tests that a user is directed toward guidance advising them to contact their local authority if
        the ages of children they are minding does not
        """
        self.selenium_task_executor.navigate_to_base_url()

        # test_email = faker.email()
        # test_phone_number = self.selenium_task_executor.generate_random_mobile_number()
        # test_alt_phone_number = self.selenium_task_executor.generate_random_mobile_number()
        #
        # self.selenium_task_executor.complete_your_login_details(test_email, test_phone_number, test_alt_phone_number)
        #
        # # Guidance page
        # self.selenium_task_executor.get_driver().find_element_by_xpath("//input[@value='Continue']").click()
        #
        # # Choose 5 to 7 year olds option
        # self.selenium_task_executor.get_driver().find_element_by_id("id_type_of_childcare_1").click()
        #
        # # Confirm selection
        # self.selenium_task_executor.get_driver().find_element_by_xpath("//input[@value='Save and continue']").click()
        #
        # WebDriverWait(self.selenium_task_executor.get_driver(), 10).until(
        #     expected_conditions.title_contains("Childcare Register"))
        #
        # self.assertEqual("Childcare Register",
        #                  self.selenium_task_executor.get_driver().find_element_by_xpath(
        #                      "//html/body/main/div[2]/form/div/h1").text)
        driver = self.selenium_task_executor.get_driver()
        driver.find_element_by_xpath("//input[@value='Sign in']").click()
        driver.find_element_by_id("id_account_selection_0-label").click()
        driver.find_element_by_xpath("//input[@value='Continue']").click()
        time.sleep(3)
        driver.find_element_by_id("id_email_address").click()
        driver.find_element_by_id("id_email_address").send_keys(faker.email())
        driver.find_element_by_xpath("//input[@value='Continue']").click()
        driver.find_element_by_id("id_1-email_address").click()
        driver.find_element_by_name("add_person").click()
        driver.find_element_by_id("id_2-first_name").click()
        driver.find_element_by_id("id_2-first_name").clear()
        driver.find_element_by_id("id_2-first_name").send_keys("second")
        driver.find_element_by_id("id_2-middle_names").click()
        driver.find_element_by_id("id_2-middle_names").clear()
        driver.find_element_by_id("id_2-middle_names").send_keys("midle")
        driver.find_element_by_id("id_2-last_name").click()
        driver.find_element_by_id("id_2-last_name").clear()
        driver.find_element_by_id("id_2-last_name").send_keys("last")
        driver.find_element_by_id("id_2-date_of_birth_0").click()
        driver.find_element_by_id("id_2-date_of_birth_0").clear()
        driver.find_element_by_id("id_2-date_of_birth_0").send_keys("12")
        driver.find_element_by_id("id_2-date_of_birth_1").click()
        driver.find_element_by_id("id_2-date_of_birth_1").clear()
        driver.find_element_by_id("id_2-date_of_birth_1").send_keys("12")
        driver.find_element_by_id("id_2-date_of_birth_2").click()
        driver.find_element_by_id("id_2-date_of_birth_2").clear()
        driver.find_element_by_id("id_2-date_of_birth_2").send_keys("1987")
        driver.find_element_by_id("id_2-relationship").click()
        driver.find_element_by_id("id_2-relationship").clear()
        driver.find_element_by_id("id_2-relationship").send_keys("Friend")
        driver.find_element_by_id("id_2-email_address").click()
        driver.find_element_by_id("id_2-email_address").clear()
        driver.find_element_by_id("id_2-email_address").send_keys("tester@informed.com")
        driver.find_element_by_id("adult-details-save").click()
        driver.find_element_by_xpath("//div[@id='id_2-email_address-group']/span").click()
        self.assertEqual("Their email address cannot be the same as another person in your home",
                         driver.find_element_by_xpath("//div[@id='id_2-email_address-group']/span").text)
        try:
            self.assertEqual("Register as a nanny", driver.title)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//input[@value='Sign in']").click()
        driver.find_element_by_id("id_account_selection_0").click()
        driver.find_element_by_xpath("//input[@value='Continue']").click()
        driver.find_element_by_id("id_email_address").click()
        driver.find_element_by_id("id_email_address").clear()
        driver.find_element_by_id("id_email_address").send_keys("raghavendra.kalakonda@informed.com")
        driver.find_element_by_xpath("//input[@value='Continue']").click()




def tearDown(self):
        self.selenium_driver.quit()

        try:
            del os.environ['EMAIL_VALIDATION_URL']
        except:
            pass

        super(ApplyAsAChildminder, self).tearDown()
        self.assertEqual([], self.verification_errors)
