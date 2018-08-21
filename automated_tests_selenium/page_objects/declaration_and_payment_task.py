from django.test import TestCase
from selenium.webdriver.support.select import Select


class DeclarationAndPaymentTask(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(DeclarationAndPaymentTask, self).__init__(*args, **kwargs)

    def complete_declaration_and_payment(self):
        driver = self.web_util.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='review']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='review']/td/a/span").click()
        self.web_util.wait_until_page_load("Check all your details")
        self.assertEqual("Check all your details", driver.title)
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.web_util.click_element_by_link_text("Continue")
        self.web_util.click_element_by_id("id_follow_rules")
        self.web_util.click_element_by_id("id_share_info_declare")
        self.web_util.click_element_by_id("id_information_correct_declare")
        self.web_util.click_element_by_id("id_change_declare")
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_id("id_card_type")
        Select(driver.find_element_by_id("id_card_type")).select_by_visible_text("Visa")
        self.web_util.click_element_by_id("id_card_type")
        self.web_util.send_keys_by_id("id_card_number", "5454545454545454")
        self.web_util.send_keys_by_id("id_expiry_date_0", "12")
        self.web_util.send_keys_by_id("id_expiry_date_1", "21")
        self.web_util.send_keys_by_id("id_cardholders_name", "wew")
        self.web_util.send_keys_by_id("id_card_security_code", "121")
        self.web_util.click_element_by_xpath("//input[@value='Pay and apply']")
