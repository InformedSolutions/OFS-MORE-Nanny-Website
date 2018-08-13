from django.test import TestCase
from selenium.webdriver.support.select import Select


class DeclarationAndPaymentTask(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(DeclarationAndPaymentTask, self).__init__(*args, **kwargs)

    def complete_declaration_and_payment(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='review']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='review']/td/a/span").click()
        self.task_executor.wait_until_page_load("Check all your details")
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
