from django.test import TestCase


class CriminalRecordCheckTask(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(CriminalRecordCheckTask, self).__init__(*args, **kwargs)

    def complete_criminal_record(self):
        driver = self.web_util.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)
        self.web_util.click_element_by_xpath("//tr[@id='criminal_record']/td/a/span")
        self.web_util.click_element_by_link_text("Continue")
        self.web_util.click_element_by_id("id_dbs_number")
        self.web_util.send_keys_by_id("id_dbs_number", "123456789098")
        self.web_util.click_element_by_id("id_convictions_1")
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)
