from django.test import TestCase


class FirstAidTrainingTask(TestCase):

    def __init__(self, web_util, *args, **kwargs):
        """
        Default constructor
        """
        self.web_util = web_util
        super(FirstAidTrainingTask, self).__init__(*args, **kwargs)

    def complete_First_aid_training(self):
        driver = self.web_util.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/span").click()
        self.web_util.click_element_by_link_text("Continue")
        self.web_util.send_keys_by_id("id_training_organisation", "First aid taining organisation")
        self.web_util.send_keys_by_id("id_course_title", "Title of training course")
        self.web_util.send_keys_by_id("id_course_date_0", "12")
        self.web_util.send_keys_by_id("id_course_date_1", "12")
        self.web_util.send_keys_by_id("id_course_date_2", "2017")
        self.web_util.click_element_by_name("action")
        self.web_util.click_element_by_link_text("Continue")
        self.web_util.assert_page_title("Check your answers: first aid training")
        self.web_util.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.web_util.wait_until_page_load("Register as a nanny")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)
