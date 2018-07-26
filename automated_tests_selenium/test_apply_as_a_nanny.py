"""
Selenium test cases for the Childminder service
"""

import os
import time
from datetime import datetime

from django.test import LiveServerTestCase, override_settings, tag
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

        self.selenium_driver.implicitly_wait(30)

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
    def test_can_apply_as_a_nanny_full_question_set(self):
        """
        Tests that a user is directed toward guidance advising them to contact their local authority if
        the ages of children they are minding does not
        """
        self.task_executor.navigate_to_base_url()
        self.complete_full_question_set()

    def complete_full_question_set(self):
        applicant_email = self.create_standard_eyfs_application()



    def create_standard_eyfs_application(self):
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
        self.task_executor.click_element_by_xpath("//input[@value='Continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)

    def complete_your_personal_details(self):

        driver=self.task_executor.get_driver()
        page_title = "Register as a nanny"
        self.waitUntilPageLoad(page_title)
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/span").click()
        driver.find_element_by_id("id_first_name").click()
        driver.find_element_by_id("id_first_name").send_keys("Raghavendra")
        driver.find_element_by_id("id_middle_names").send_keys("MiddleName")
        driver.find_element_by_id("id_last_name").send_keys("Kalakonda")
        driver.find_element_by_name("action").click()
        driver.find_element_by_id("id_date_of_birth_0").send_keys("12")
        driver.find_element_by_id("id_date_of_birth_1").send_keys("12")
        driver.find_element_by_id("id_date_of_birth_2").send_keys("1989")
        driver.find_element_by_name("action").click()
        driver.find_element_by_id("manual").click()
        driver.find_element_by_id("id_street_line1").send_keys("AddressLine1")
        driver.find_element_by_id("id_street_line2").send_keys("Line2")
        driver.find_element_by_id("id_town").send_keys("Town")
        driver.find_element_by_id("id_county").send_keys("County")
        driver.find_element_by_id("id_postcode").send_keys("LS10 2HU")
        driver.find_element_by_xpath("//input[@value='Save and continue']").click()
        driver.find_element_by_name("action").click()
        driver.find_element_by_id("id_lived_abroad_1").click()
        driver.find_element_by_name("action").click()
        self.assertPageTitleAtTaskSummaryPage("Check your answers: your personal details")
        # self.assertEqual("Check your answers: your personal details", driver.title)
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        # driver.find_element_by_xpath("//input[@value='Confirm and continue']").click()
        self.waitUntilPageLoad(page_title)
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)

    def complete_First_aid_training_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/span").click()
        driver.find_element_by_link_text("Continue").click()
        driver.find_element_by_id("id_first_aid_training_organisation").click()
        driver.find_element_by_id("id_first_aid_training_organisation").clear()
        driver.find_element_by_id("id_first_aid_training_organisation").send_keys("First aid taining organisation")
        driver.find_element_by_id("id_title_of_training_course").click()
        driver.find_element_by_id("id_title_of_training_course").clear()
        driver.find_element_by_id("id_title_of_training_course").send_keys("Title of training course")
        driver.find_element_by_id("id_course_date_0").click()
        driver.find_element_by_id("id_course_date_0").clear()
        driver.find_element_by_id("id_course_date_0").send_keys("12")
        driver.find_element_by_id("id_course_date_1").click()
        driver.find_element_by_id("id_course_date_1").clear()
        driver.find_element_by_id("id_course_date_1").send_keys("12")
        driver.find_element_by_id("id_course_date_2").click()
        driver.find_element_by_id("id_course_date_2").clear()
        driver.find_element_by_id("id_course_date_2").send_keys("2017")
        driver.find_element_by_name("action").click()
        driver.find_element_by_link_text("Continue").click()
        self.assertEqual("Check your answers: first aid training", driver.title)
        driver.find_element_by_xpath("//input[@value='Confirm and continue']").click()
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)

    def complete_childcare_training_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/span").click()
        driver.find_element_by_id("id_continue").click()
        driver.find_element_by_id("id_childcare_training_0").click()
        driver.find_element_by_id("id_childcare_training_1").click()
        driver.find_element_by_id("id_continue").click()
        self.assertEqual("Check your answers: childcare training", driver.title)
        driver.find_element_by_id("id_continue").click()
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)

    def complete_criminal_record_check_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/span").click()
        driver.find_element_by_link_text("Continue").click()
        driver.find_element_by_id("id_dbs_number").click()
        driver.find_element_by_id("id_dbs_number").clear()
        driver.find_element_by_id("id_dbs_number").send_keys("123456789098")
        driver.find_element_by_id("id_convictions_1").click()
        driver.find_element_by_name("action").click()
        driver.find_element_by_xpath("//input[@value='Confirm and continue']").click()
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)

    def complete_insurance_cover_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/span").click()
        driver.find_element_by_link_text("Continue").click()
        driver.find_element_by_id("id_public_liability_0").click()
        driver.find_element_by_xpath("//input[@value='Save and continue']").click()
        self.waitUntilPageLoad("Check your answers: insurance cover")
        self.assertEqual("Check your answers: insurance cover", driver.title)
        driver.find_element_by_id("id_continue").click()
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)

    def complete_declaration_and_payment_task(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='review']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='review']/td/a/span").click()
        self.waitUntilPageLoad("Check all your details")
        self.assertEqual("Check all your details", driver.title)
        driver.find_element_by_xpath("//input[@value='Confirm and continue']").click()
        driver.find_element_by_link_text("Continue").click()
        driver.find_element_by_id("id_follow_rules").click()
        driver.find_element_by_id("id_share_info_declare").click()
        driver.find_element_by_id("id_information_correct_declare").click()
        driver.find_element_by_id("id_change_declare").click()
        driver.find_element_by_name("action").click()
        driver.find_element_by_id("id_card_type").click()
        Select(driver.find_element_by_id("id_card_type")).select_by_visible_text("Visa")
        driver.find_element_by_id("id_card_type").click()
        driver.find_element_by_id("id_card_number").click()
        driver.find_element_by_id("id_card_number").clear()
        driver.find_element_by_id("id_card_number").send_keys("5454545454545454")
        driver.find_element_by_id("id_expiry_date_0").click()
        driver.find_element_by_id("id_expiry_date_0").clear()
        driver.find_element_by_id("id_expiry_date_0").send_keys("12")
        driver.find_element_by_id("id_expiry_date_1").click()
        driver.find_element_by_id("id_expiry_date_1").clear()
        driver.find_element_by_id("id_expiry_date_1").send_keys("21")
        driver.find_element_by_id("id_cardholders_name").click()
        driver.find_element_by_id("id_cardholders_name").clear()
        driver.find_element_by_id("id_cardholders_name").send_keys("wew")
        driver.find_element_by_id("id_card_security_code").click()
        driver.find_element_by_id("id_card_security_code").clear()
        driver.find_element_by_id("id_card_security_code").send_keys("121")
        driver.find_element_by_xpath("//input[@value='Pay and apply']").click()
        self.waitUntilPageLoad("Thank you for applying")
        driver.find_element_by_xpath("//main[@id='content']/div/div[2]/h1").click()
        self.assertEqual("Thank you for applying",
                         driver.find_element_by_xpath("//main[@id='content']/div/div[2]/h1").text)
        self.assertEqual("Thank you for applying", driver.title)

    def waitUntilPageLoad(self, page_title):
        delay = 4  # seconds
        try:
            # myElem = WebDriverWait(self.selenium_task_executor.get_driver(),
            #                        delay).until(expected_conditions.title_contains("Register as a nanny"))
            WebDriverWait(self.task_executor.get_driver(), delay).until(
                expected_conditions.title_contains(page_title))
        except TimeoutException:
            print("Loading took too much time!")

    def assertPageTitleAtTaskSummaryPage(self, expected_title):
        driver=self.task_executor.get_driver()

        WebDriverWait(driver, 3).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//input[@value='Confirm and continue']")))
        self.assertEqual(expected_title, driver.title)

    def tearDown(self):

        self.selenium_driver.quit()

        try:
            del os.environ['EMAIL_VALIDATION_URL']
        except:
            pass

        super(ApplyAsANanny, self).tearDown()
        self.assertEqual([], self.verification_errors)