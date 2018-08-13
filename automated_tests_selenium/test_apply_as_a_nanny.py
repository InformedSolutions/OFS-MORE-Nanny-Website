"""
Selenium test cases for the nanny service
"""

import os
import time
from datetime import datetime
from django.test import LiveServerTestCase, override_settings, tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from automated_tests_selenium.page_objects.task_executor import TaskExecutor
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

        self.task_executor = TaskExecutor(self.selenium_driver, base_url)
        self.registration = Registration(self.task_executor)
        self.login = Login(self.task_executor)
        self.personal_details_task = PersonalDetailsTask(self.task_executor)
        self.childcare_address_task = ChildcareAddressTask(self.task_executor)
        self.first_aid_training_task = FirstAidTrainingTask(self.task_executor)
        self.childcare_training_task = ChildcareTrainingTask(self.task_executor)
        self.criminal_record_check_task = CriminalRecordCheckTask(self.task_executor)
        self.insurance_cover_task = InsuranceCoverTask(self.task_executor)
        self.declaration_and_payment_task = DeclarationAndPaymentTask(self.task_executor)

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
    def test_nanny_can_submit_application(self):
        """
        Tests that a user can successfully submit a nanny application
        """
        self.task_executor.navigate_to_base_url()

        test_email = faker.email()
        test_phone_number = self.task_executor.generate_random_mobile_number()
        test_alt_phone_number = self.task_executor.generate_random_mobile_number()
        self.registration.register_email_address(test_email)

        self.login.login_to_the_application(test_phone_number, test_alt_phone_number)

        self.personal_details_task.complete_details_with_not_lived_abroad_option(faker.first_name(), faker.last_name())

        self.childcare_address_task.complete_childcare_address()

        self.first_aid_training_task.complete_First_aid_training()

        self.childcare_training_task.complete_childcare_training()

        self.criminal_record_check_task.complete_criminal_record()

        self.insurance_cover_task.complete_insurance_cover()

        self.declaration_and_payment_task.complete_declaration_and_payment()

        return test_email

    def tearDown(self):
        self.selenium_driver.quit()
        del os.environ['EMAIL_VALIDATION_URL']
        super(ApplyAsANanny, self).tearDown()
        self.assertEqual([], self.verification_errors)
