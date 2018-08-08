"""
Selenium test cases for the nanny service
"""

import os
from datetime import datetime

from django.test import LiveServerTestCase, override_settings, tag
from faker.generator import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from .task_executor import TaskExecutor

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

        global selenium_driver_out
        selenium_driver_out = self.selenium_driver

        super(ApplyAsANanny, self).setUp()

    def launch_local_browser(self):
        """
        If the HEADLESS_CHROME value in Environment variables is set to true then it will launch chrome headless
        browser, else it will launch firefox.
        """
        if os.environ.get('HEADLESS_CHROME') == 'True':
            # To install chromedriver on an ubuntu machine:
            # https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
            path_to_chromedriver = os.popen("which chromedriver").read().rstrip()
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
    def test_can_apply_as_a_nanny_full_question_set(self):
        """
        Tests that a user can successfully submit a nanny application
        """
        self.task_executor.navigate_to_base_url()
        applicant_email = self.create_standard_application()

    def create_standard_application(self):
        """
        Helper method for starting a new application
        :return: email address used to register the application
        """
        self.task_executor.navigate_to_base_url()

        test_email = faker.email()
        test_phone_number = self.task_executor.generate_random_mobile_number()
        test_alt_phone_number = self.task_executor.generate_random_mobile_number()

        self.task_executor.complete_your_login_details(test_email, test_phone_number, test_alt_phone_number)

        self.complete_your_personal_details()

        self.complete_childcare_address_task()

        self.complete_First_aid_training_task()

        self.complete_childcare_training_task()

        self.complete_criminal_record_check_task()

        self.complete_insurance_cover_task()

        self.complete_declaration_and_payment_task()

        return test_email

    def complete_childcare_address_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='childcare_address']/td/a/span")
        self.task_executor.click_element_by_xpath("//input[@value='Continue']")
        self.task_executor.click_element_by_id("id_address_to_be_provided_0")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_id("id_home_address_0")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_xpath("//*[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)

    def complete_your_personal_details(self):
        driver = self.task_executor.get_driver()
        page_title = "Register as a nanny"
        self.waitUntilPageLoad(page_title)
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='personal_details']/td/a/span")
        self.task_executor.click_element_by_id("id_first_name")
        self.task_executor.send_keys_by_id("id_first_name",faker.first_name())
        self.task_executor.send_keys_by_id("id_middle_names", "MiddleName")
        self.task_executor.send_keys_by_id("id_last_name", faker.last_name())
        self.task_executor.click_element_by_name("action")
        self.task_executor.send_keys_by_id("id_date_of_birth_0", random.randint(1, 28))
        self.task_executor.send_keys_by_id("id_date_of_birth_1", random.randint(1, 12))
        self.task_executor.send_keys_by_id("id_date_of_birth_2", random.randint(1950, 1990))
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_id("manual")
        self.task_executor.send_keys_by_id("id_street_line1", "AddressLine1")
        self.task_executor.send_keys_by_id("id_street_line2", "Line2")
        self.task_executor.send_keys_by_id("id_town", "Town")
        self.task_executor.send_keys_by_id("id_county", "County")
        self.task_executor.send_keys_by_id("id_postcode", "WA14 4PA")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_id("id_lived_abroad_1")
        self.task_executor.click_element_by_name("action")
        self.assertPageTitleAtTaskSummaryPage("Check your answers: your personal details")
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.waitUntilPageLoad(page_title)
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)

    def complete_First_aid_training_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/span").click()
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.send_keys_by_id("id_first_aid_training_organisation", "First aid taining organisation")
        self.task_executor.send_keys_by_id("id_title_of_training_course", "Title of training course")
        self.task_executor.send_keys_by_id("id_course_date_0", "12")
        self.task_executor.send_keys_by_id("id_course_date_1", "12")
        self.task_executor.send_keys_by_id("id_course_date_2", "2017")
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_link_text("Continue")
        self.assertPageTitleAtTaskSummaryPage("Check your answers: first aid training")
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.waitUntilPageLoad("Register as a nanny")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)

    def complete_childcare_training_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/span").click()
        driver.find_element_by_id("id_continue").click()
        self.task_executor.click_element_by_id("id_childcare_training_0")
        self.task_executor.click_element_by_id("id_childcare_training_1")
        self.task_executor.click_element_by_id("id_continue")
        self.waitUntilPageLoad("Check your answers: childcare training")
        self.assertEqual("Check your answers: childcare training", driver.title)
        self.task_executor.click_element_by_id("id_continue")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)

    def complete_criminal_record_check_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='criminal_record']/td/a/span")
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.click_element_by_id("id_dbs_number")
        self.task_executor.send_keys_by_id("id_dbs_number", "123456789098")
        self.task_executor.click_element_by_id("id_convictions_1")
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)

    def complete_insurance_cover_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='insurance_cover']/td/a/span")
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.click_element_by_id("id_public_liability_0")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.waitUntilPageLoad("Check your answers: insurance cover")
        self.assertEqual("Check your answers: insurance cover", driver.title)
        self.task_executor.click_element_by_id("id_continue")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)

    def complete_declaration_and_payment_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='review']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='review']/td/a/span").click()
        self.waitUntilPageLoad("Check all your details")
        self.assertEqual("Check all your details", driver.title)
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.click_element_by_id("id_follow_rules")
        self.task_executor.click_element_by_id("id_share_info_declare")
        self.task_executor.click_element_by_id("id_information_correct_declare")
        self.task_executor.click_element_by_id("id_change_declare")
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_id("id_card_type")
        Select(driver.find_element_by_id("id_card_type")).select_by_visible_text("Visa")
        self.task_executor.click_element_by_id("id_card_type")
        self.task_executor.send_keys_by_id("id_card_number", "5454545454545454")
        self.task_executor.send_keys_by_id("id_expiry_date_0", "12")
        self.task_executor.send_keys_by_id("id_expiry_date_1", "21")
        self.task_executor.send_keys_by_id("id_cardholders_name", "wew")
        self.task_executor.send_keys_by_id("id_card_security_code", "121")
        self.task_executor.click_element_by_xpath("//input[@value='Pay and apply']")

    def waitUntilPageLoad(self, page_title):
        delay = 5  # seconds
        driver = self.task_executor.get_driver()
        try:
            WebDriverWait(driver, delay).until(
                expected_conditions.title_contains(page_title))
        except TimeoutException:
            self.assertEqual(page_title, driver.title)


    def assertPageTitleAtTaskSummaryPage(self, expected_title):
        driver = self.task_executor.get_driver()

        WebDriverWait(driver, 3).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//input[@value='Confirm and continue']")))
        self.assertEqual(expected_title, driver.title)

    def tearDown(self):
        self.selenium_driver.quit()
        del os.environ['EMAIL_VALIDATION_URL']
        super(ApplyAsANanny, self).tearDown()
        self.assertEqual([], self.verification_errors)
