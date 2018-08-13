from django.test import TestCase


class ChildcareAddressTask(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(ChildcareAddressTask, self).__init__(*args, **kwargs)

    def complete_childcare_address(self):
        driver = self.web_util.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)
        self.web_util.click_element_by_xpath("//tr[@id='childcare_address']/td/a/span")
        self.web_util.click_element_by_xpath("//input[@value='Continue']")
        self.web_util.click_element_by_id("id_address_to_be_provided_0")
        self.web_util.click_element_by_xpath("//input[@value='Save and continue']")
        self.web_util.click_element_by_id("id_home_address_0")
        self.web_util.click_element_by_xpath("//input[@value='Save and continue']")
        self.web_util.click_element_by_xpath("//input[@value='Save and continue']")
        self.web_util.click_element_by_xpath("//*[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)
