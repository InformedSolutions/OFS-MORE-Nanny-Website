"""
Selenium test cases for the nanny service
"""

import os
from datetime import datetime

from django.test import LiveServerTestCase, override_settings, tag

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automated_tests_selenium.util.web_util import WebUtil
from automated_tests_selenium.page_objects.personal_details_task import PersonalDetailsTask
from automated_tests_selenium.page_objects.childcare_address_task import ChildcareAddressTask
from automated_tests_selenium.page_objects.first_aid_training_task import FirstAidTrainingTask
from automated_tests_selenium.page_objects.childcare_training_task import ChildcareTrainingTask
from automated_tests_selenium.page_objects.criminal_record_check_task import CriminalRecordCheckTask
from automated_tests_selenium.page_objects.insurance_cover_task import InsuranceCoverTask
from automated_tests_selenium.page_objects.declaration_and_payment_task import DeclarationAndPaymentTask
from automated_tests_selenium.page_objects.account_registration import Registration
from automated_tests_selenium.page_objects.login import Login

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
            # Destroy session upon test failure.
            args[0].selenium_driver.delete_all_cookies()
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
class ApplyAsANanny(LiveServerTestCase):
    port = 8000

    if os.environ.get('LOCAL_SELENIUM_DRIVER') == 'True':
        host = '127.0.0.1'
    else:
        host = '0.0.0.0'

    current_year = datetime.now().year

    @classmethod
    def setUpClass(cls):
        base_url = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS')

        if os.environ.get('LOCAL_SELENIUM_DRIVER') == 'True':
            # If running on a windows host, make sure to drop the
            # geckodriver.exe into your Python/Scripts installation folder
            cls.launch_local_browser()
        else:
            # If not using local driver, default requests to a selenium grid server
            cls.launch_remote_browser()

        cls.selenium_driver.implicitly_wait(15)

        cls.verification_errors = []
        cls.accept_next_alert = True

        cls.web_util = WebUtil(cls.selenium_driver, base_url)
        cls.registration = Registration(cls.web_util)
        cls.login = Login(cls.web_util)
        cls.personal_details_task = PersonalDetailsTask(cls.web_util)
        cls.childcare_address_task = ChildcareAddressTask(cls.web_util)
        cls.first_aid_training_task = FirstAidTrainingTask(cls.web_util)
        cls.childcare_training_task = ChildcareTrainingTask(cls.web_util)
        cls.criminal_record_check_task = CriminalRecordCheckTask(cls.web_util)
        cls.insurance_cover_task = InsuranceCoverTask(cls.web_util)
        cls.declaration_and_payment_task = DeclarationAndPaymentTask(cls.web_util)

        global selenium_driver_out
        selenium_driver_out = cls.selenium_driver

        super(ApplyAsANanny, cls).setUpClass()

    @classmethod
    def launch_local_browser(cls):
        """
        If the HEADLESS_CHROME value in Environment variables is set to true then it will launch chrome headless
        browser, else it will launch firefox.
        """
        if os.environ.get('HEADLESS_CHROME') == 'True':
            # To install chromedriver on an ubuntu machine:
            # https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
            # For the latest version:
            # https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py3/py3.6-selenium/Dockerfile
            path_to_chromedriver = os.popen("which chromedriver").read().rstrip()
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            cls.selenium_driver = webdriver.Chrome(path_to_chromedriver, chrome_options=chrome_options)
        else:
            cls.selenium_driver = webdriver.Firefox()
        cls.selenium_driver.maximize_window()

    @classmethod
    def launch_remote_browser(cls):
        """
        If the HEADLESS_CHROME value in Environment variables is set to true then it will launch chrome headless
        browser, else it will launch firefox.
        """
        # Steps to get the IP required previously required for remote execution.
        # ip = os.popen("ifconfig enp0s3 | grep 'inet ' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | cut -d ' ' -f 2").read()
        # ip = ip.strip('\n')

        if os.environ.get('HEADLESS_CHROME') == 'True':
            chrome_options = webdriver.ChromeOptions()
            URL = os.environ['SELENIUM_HOST']
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            # chrome_options.add_argument('--disable-web-security')
            # chrome_options.binary_location("/usr/bin/chromedriver.exe")
            # chrome_options.add_argument("--log-path=D:\\qc1.log")

            desired_capabilities = chrome_options.to_capabilities()
            # desired_capabilities['browserConnectionEnabled'] = True

            cls.selenium_driver = webdriver.Remote(
                command_executor=URL,
                desired_capabilities=desired_capabilities
            )

        else:
            cls.selenium_driver = webdriver.Remote(
                command_executor=os.environ['SELENIUM_HOST'],
                desired_capabilities={'platform': 'ANY', 'browserName': 'firefox', 'version': ''}
            )
        cls.selenium_driver.maximize_window()

    @try_except_method
    def test_submit_application_with_not_lived_abroad_option(self):
        """
        Tests that a user can successfully submit a nanny application with
        """
        self.web_util.navigate_to_base_url()

        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)

        self.personal_details_task.complete_details_with_not_lived_abroad_option(faker.first_name(), faker.last_name())

        self.childcare_address_task.complete_childcare_address()

        self.first_aid_training_task.complete_First_aid_training()

        self.childcare_training_task.complete_childcare_training()

        self.criminal_record_check_task.complete_criminal_record()

        self.insurance_cover_task.complete_insurance_cover()

        self.declaration_and_payment_task.complete_declaration_and_payment()

        self.web_util.click_element_by_link_text('Sign out')

    @try_except_method
    def test_submit_application_with_lived_abroad_option(self):
        """
        Test that a user can complete personal details task with lived abroad option
        """
        self.web_util.navigate_to_base_url()
        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)

        self.personal_details_task.complete_details_with_lived_abroad_option(faker.first_name(), faker.last_name())

        self.web_util.click_element_by_link_text('Sign out')

    # @try_except_method
    # def test_can_access_costs_without_authenticating(self):
    #     """
    #     Tests the costs page can be accessed without logging in.
    #     """
    #     driver = self.web_util.get_driver()
    #     self.web_util.navigate_to_base_url()
    #     self.web_util.click_element_by_link_text("Costs")
    #     self.assertEqual("Costs", driver.title)
    #
    # @try_except_method
    # def test_can_access_costs_when_authenticated(self):
    #     """
    #     Tests the costs page can be accessed when logged in.
    #     """
    #     driver = self.web_util.get_driver()
    #     self.web_util.navigate_to_base_url()
    #
    #     test_email = faker.email()
    #     test_phone_number = self.web_util.generate_random_mobile_number()
    #     test_alt_phone_number = self.web_util.generate_random_mobile_number()
    #     self.registration.register_email_address(test_email)
    #     self.login.login_to_the_application(test_phone_number, test_alt_phone_number)
    #     self.web_util.click_element_by_link_text("Costs")
    #     self.assertEqual("Costs", driver.title)
    #     self.web_util.click_element_by_link_text('Sign out')
    #
    # @try_except_method
    # def test_can_return_to_task_list_from_help_and_costs_when_authenticated(self):
    #     """
    #     Test to make sure that task list is accessible from cost page
    #     """
    #     driver = self.web_util.get_driver()
    #     self.web_util.navigate_to_base_url()
    #
    #     test_email = faker.email()
    #     test_phone_number = self.web_util.generate_random_mobile_number()
    #     test_alt_phone_number = self.web_util.generate_random_mobile_number()
    #     self.registration.register_email_address(test_email)
    #
    #     self.login.login_to_the_application(test_phone_number, test_alt_phone_number)
    #
    #     self.personal_details_task.complete_details_with_not_lived_abroad_option(faker.first_name(), faker.last_name())
    #
    #     # Costs page
    #     self.web_util.click_element_by_link_text("Costs")
    #     self.web_util.assert_page_title("Costs")
    #
    #     # Go back to task list
    #     self.web_util.click_element_by_link_text("Return to application")
    #
    #     self.web_util.assert_page_title("Register as a nanny")
    #
    #     # Help page
    #     self.web_util.click_element_by_link_text("Help and contacts")
    #     self.web_util.assert_page_title("Help and contacts")
    #
    #     # Go back to task list
    #     self.web_util.click_element_by_link_text("Return to application")
    #
    #     self.web_util.assert_page_title("Register as a nanny")
    #
    #     self.web_util.click_element_by_link_text('Sign out')

    @try_except_method
    def test_user_should_not_be_able_to_submit_the_application(self):
        """
        Test to make sure that the user can't be able to submit application when selected none for type of course
        """
        self.web_util.navigate_to_base_url()
        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)
        self.childcare_training_task.childcare_training_with_none_option_for_type_of_course()

        self.web_util.click_element_by_link_text('Sign out')

    @try_except_method
    def test_can_cancel_application(self):
        """
        Test that cancel application functionality is working
        """
        self.web_util.navigate_to_base_url()

        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)

        self.web_util.click_element_by_link_text("Cancel application")
        self.web_util.click_element_by_xpath("//input[@value='Cancel application']")
        self.web_util.assert_page_title("Application cancelled")

        # verifying the deletion was successful by using the same email id for re registration
        # if the cancellation was not successful then the application will land on sms page
        # as existing user where our tests will fail
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.web_util.navigate_to_base_url()
        self.registration.register_email_address(test_email)
        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)
        self.web_util.click_element_by_link_text('Sign out')

    @try_except_method
    def test_user_cannot_resend_sms_code_more_than_three_times(self):
        """
        Test to ensure that, if the user requests to resend their SMS security code a fourth time, they are instead
        asked to enter their security question details.
        """
        self.web_util.navigate_to_base_url()
        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()

        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)
        self.web_util.click_element_by_link_text('Sign out')
        self.login.navigate_to_SMS_validation_page(test_email)

        for n in range(3):
            self.web_util.click_element_by_link_text("Didn't get a code?")
            self.web_util.click_element_by_id("id_send_new_code_button")

        self.web_util.get_driver().find_element_by_link_text("Still didn't get a code?").click()
        self.assertEqual("Sign in question", self.web_util.get_driver().title)

    @try_except_method
    def test_user_can_not_use_email_link_twice(self):
        """
        Tests that using email link for sign-in more than once returns a 'bad link' page.
        """
        self.web_util.navigate_to_base_url()
        test_email = faker.email()
        self.registration.register_email_address(test_email)
        self.web_util.navigate_to_email_validation_url()
        self.web_util.navigate_to_email_validation_url()

        self.assertEqual("Link used already",
                         self.web_util.get_driver().find_element_by_class_name("form-title").text)

    @classmethod
    def tearDownClass(cls):
        cls.selenium_driver.quit()
        try:
            del os.environ['EMAIL_VALIDATION_URL']
        except KeyError:
            pass
        super(ApplyAsANanny, cls).tearDownClass()
