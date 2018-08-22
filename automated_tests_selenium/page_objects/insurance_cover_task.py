from django.test import TestCase


class InsuranceCoverTask(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(InsuranceCoverTask, self).__init__(*args, **kwargs)

    def complete_insurance_cover(self):
        driver = self.web_util.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)
        self.web_util.click_element_by_xpath("//tr[@id='insurance_cover']/td/a/span")
        self.web_util.click_element_by_link_text("Continue")
        self.web_util.click_element_by_id("id_public_liability_0")
        self.web_util.click_element_by_xpath("//input[@value='Save and continue']")
        self.web_util.wait_until_page_load("Check your answers: insurance cover")
        self.assertEqual("Check your answers: insurance cover", driver.title)
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)
