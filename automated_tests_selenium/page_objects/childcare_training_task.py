from django.test import TestCase


class ChildcareTrainingTask(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(ChildcareTrainingTask, self).__init__(*args, **kwargs)

    def complete_childcare_training(self):
        driver = self.web_util.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/span").click()
        driver.find_element_by_id("id_continue").click()
        self.web_util.click_element_by_id("id_childcare_training_0")
        self.web_util.click_element_by_id("id_childcare_training_1")
        self.web_util.click_element_by_id("id_continue")
        self.web_util.wait_until_page_load("Check your answers: childcare training")
        self.assertEqual("Check your answers: childcare training", driver.title)
        self.web_util.click_element_by_id("id_continue")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)

    def childcare_training_with_none_option_for_type_of_course(self):
        driver = self.web_util.get_driver()
        self.web_util.wait_until_page_load("Register as a nanny")
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)
        self.web_util.click_element_by_xpath("//tr[@id='childcare_training']/td/a/span")
        self.web_util.click_element_by_xpath("//input[@id='id_continue']")
        self.web_util.click_element_by_id("id_childcare_training_2")
        self.web_util.click_element_by_xpath("//input[@id='id_continue']")
        self.assertTrue("Go on a training course", driver.title)
        self.web_util.is_return_link_present()
        self.web_util.click_element_by_xpath("//input[@id='id_continue']")
        self.web_util.wait_until_page_load("Register as a nanny")
        self.assertEqual("Started", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)