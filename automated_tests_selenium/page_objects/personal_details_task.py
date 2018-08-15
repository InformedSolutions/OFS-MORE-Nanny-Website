from django.test import TestCase
from faker import Faker
from faker.generator import random
from selenium.webdriver.support.select import Select


class PersonalDetailsTask(TestCase):
    # Configure faker to use english locale
    faker = Faker('en_GB')

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(PersonalDetailsTask, self).__init__(*args, **kwargs)

    def complete_details_with_not_lived_abroad_option(self, first_name, last_name):
        driver = self.web_util.get_driver()
        page_title = "Register as a nanny"
        self.web_util.wait_until_page_load(page_title)
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)
        self.web_util.click_element_by_xpath("//tr[@id='personal_details']/td/a/span")
        self.web_util.click_element_by_id("id_first_name")
        self.web_util.send_keys_by_id("id_first_name", first_name)
        self.web_util.send_keys_by_id("id_middle_names", "MiddleName")
        self.web_util.send_keys_by_id("id_last_name", last_name)
        self.web_util.click_element_by_name("action")
        self.web_util.send_keys_by_id("id_date_of_birth_0", random.randint(1, 28))
        self.web_util.send_keys_by_id("id_date_of_birth_1", random.randint(1, 12))
        self.web_util.send_keys_by_id("id_date_of_birth_2", random.randint(1950, 1990))
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_id("manual")
        self.web_util.send_keys_by_id("id_street_line1", "AddressLine1")
        self.web_util.send_keys_by_id("id_street_line2", "Line2")
        self.web_util.send_keys_by_id("id_town", "Town")
        self.web_util.send_keys_by_id("id_county", "County")
        self.web_util.send_keys_by_id("id_postcode", "WA14 4PA")
        self.web_util.click_element_by_xpath("//input[@value='Save and continue']")
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_id("id_lived_abroad_1")
        self.web_util.click_element_by_name("action")
        self.web_util.assert_page_title("Check your answers: your personal details")
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.web_util.wait_until_page_load(page_title)
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)

    def complete_details_with_lived_abroad_option(self, first_name, last_name):
        driver = self.web_util.get_driver()
        page_title = "Register as a nanny"
        self.web_util.wait_until_page_load(page_title)
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)
        self.web_util.click_element_by_xpath("//tr[@id='personal_details']/td/a/span")
        self.web_util.click_element_by_id("id_first_name")
        self.web_util.send_keys_by_id("id_first_name", first_name)
        self.web_util.send_keys_by_id("id_middle_names", "MiddleName")
        self.web_util.send_keys_by_id("id_last_name", last_name)
        self.web_util.click_element_by_name("action")
        self.web_util.send_keys_by_id("id_date_of_birth_0", random.randint(1, 28))
        self.web_util.send_keys_by_id("id_date_of_birth_1", random.randint(1, 12))
        self.web_util.send_keys_by_id("id_date_of_birth_2", random.randint(1950, 1990))
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_id("id_postcode")
        self.web_util.send_keys_by_id("id_postcode", "LS10 1ED")
        self.web_util.click_element_by_name("postcode-search")
        self.web_util.click_element_by_id("id_address")
        Select(driver.find_element_by_id("id_address")).select_by_visible_text(
            "FORTIS DEVELOPMENTS LTD, BANK HOUSE, OLD MARKET PLACE, ALTRINCHAM, WA14 4PA")
        self.web_util.click_element_by_id("id_address")
        self.web_util.click_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Select address'])[1]/following::input[2]")
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_id("id_lived_abroad_0")
        self.assertTrue(self.web_util.is_return_link_present())
        self.web_util.click_element_by_xpath("//input[@value='Save and continue']")
        self.web_util.assert_page_title("Certificates of good conduct")
        self.web_util.click_element_by_link_text("Continue")
        self.assertTrue(self.web_util.is_return_link_present())
        self.web_util.assert_page_title("Post certificates of good conduct")
        self.assertTrue(self.web_util.is_return_link_present())
        self.web_util.click_element_by_link_text("Save and continue")
        self.web_util.assert_page_title("Check your answers: your personal details")
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.web_util.wait_until_page_load(page_title)
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)

