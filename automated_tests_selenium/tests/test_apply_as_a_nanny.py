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
            capture_screenshot(func)
            raise e

    return func_wrapper


def capture_screenshot(func):
    global selenium_driver_out
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    scr = selenium_driver_out.find_element_by_tag_name('html')
    scr.screenshot('selenium/screenshot-%s-%s.png' % (func.__name__, now))


@tag('smoke')
@override_settings(ALLOWED_HOSTS=['*'])
class ApplyAsANanny(LiveServerTestCase):
    port = 8000

    if os.environ.get('LOCAL_SELENIUM_DRIVER') == 'True':
        host = '127.0.0.1'
    else:
        host = '0.0.0.0'

    current_year = datetime.now().year

    def setUp(self):
        base_url = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS')

        if os.environ.get('LOCAL_SELENIUM_DRIVER') == 'True':
            # If running on a windows host, make sure to drop the
            # geckodriver.exe into your Python/Scripts installation folder
            self.launch_local_browser()
        else:
            # If not using local driver, default requests to a selenium grid server
            self.launch_remote_browser()

        self.selenium_driver.implicitly_wait(15)

        self.verification_errors = []
        self.accept_next_alert = True

        self.web_util = WebUtil(self.selenium_driver, base_url)
        self.registration = Registration(self.web_util)
        self.login = Login(self.web_util)
        self.personal_details_task = PersonalDetailsTask(self.web_util)
        self.childcare_address_task = ChildcareAddressTask(self.web_util)
        self.first_aid_training_task = FirstAidTrainingTask(self.web_util)
        self.childcare_training_task = ChildcareTrainingTask(self.web_util)
        self.criminal_record_check_task = CriminalRecordCheckTask(self.web_util)
        self.insurance_cover_task = InsuranceCoverTask(self.web_util)
        self.declaration_and_payment_task = DeclarationAndPaymentTask(self.web_util)

        global selenium_driver_out
        selenium_driver_out = self.selenium_driver

        super(ApplyAsANanny, self).setUp()

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

    @try_except_method
    def test_can_access_costs_without_authenticating(self):
        """
        Tests the costs page can be accessed without logging in.
        """
        driver = self.web_util.get_driver()
        self.web_util.navigate_to_base_url()
        self.web_util.click_element_by_link_text("Costs")
        self.assertEqual("Costs", driver.title)

    @try_except_method
    def test_can_access_costs_when_authenticated(self):
        """
        Tests the costs page can be accessed when logged in.
        """
        driver = self.web_util.get_driver()
        self.web_util.navigate_to_base_url()

        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.registration.register_email_address(test_email)
        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)
        self.web_util.click_element_by_link_text("Costs")
        self.assertEqual("Costs", driver.title)

    @try_except_method
    def test_can_return_to_task_list_from_help_and_costs_when_authenticated(self):
        """
        Test to make sure that task list is accessible from cost page
        """
        driver = self.web_util.get_driver()
        self.web_util.navigate_to_base_url()

        test_email = faker.email()
        test_phone_number = self.web_util.generate_random_mobile_number()
        test_alt_phone_number = self.web_util.generate_random_mobile_number()
        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)

        self.personal_details_task.complete_details_with_not_lived_abroad_option(faker.first_name(), faker.last_name())

        # Costs page
        self.web_util.click_element_by_link_text("Costs")
        self.assertEqual("Costs", driver.title)

        # Go back to task list
        self.web_util.click_element_by_link_text("Return to application")

        self.assertEqual("Register as a nanny",
                         driver.title)

        # Help page
        self.web_util.click_element_by_link_text("Help and contacts")
        self.assertEqual("Help and contacts", driver.title)

        # Go back to task list
        self.web_util.click_element_by_link_text("Return to application")

        self.assertEqual("Register as a nanny", driver.title)

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

    def tearDown(self):
        self.selenium_driver.quit()
        try:
            del os.environ['EMAIL_VALIDATION_URL']
        except:
            pass
        super(ApplyAsANanny, self).tearDown()
        self.assertEqual([], self.verification_errors)
