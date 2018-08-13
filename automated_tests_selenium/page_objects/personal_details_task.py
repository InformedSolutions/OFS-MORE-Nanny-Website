from django.test import TestCase
from faker import Faker
from faker.generator import random


class PersonalDetailsTask(TestCase):
    # Configure faker to use english locale
    faker = Faker('en_GB')

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(PersonalDetailsTask, self).__init__(*args, **kwargs)

    def complete_details_with_not_lived_abroad_option(self, first_name, last_name):
        driver = self.task_executor.get_driver()
        page_title = "Register as a nanny"
        self.task_executor.wait_until_page_load(page_title)
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='personal_details']/td/a/span")
        self.task_executor.click_element_by_id("id_first_name")
        self.task_executor.send_keys_by_id("id_first_name", first_name)
        self.task_executor.send_keys_by_id("id_middle_names", "MiddleName")
        self.task_executor.send_keys_by_id("id_last_name", last_name)
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
        self.task_executor.assert_page_title_at_task_summary_page("Check your answers: your personal details")
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.task_executor.wait_until_page_load(page_title)
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='personal_details']/td/a/strong").text)

