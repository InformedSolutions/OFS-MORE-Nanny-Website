from django.test import TestCase


class FirstAidTrainingTask(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(FirstAidTrainingTask, self).__init__(*args, **kwargs)

    def complete_First_aid_training(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/span").click()
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.send_keys_by_id("id_first_aid_training_organisation", "First aid taining organisation")
        self.task_executor.send_keys_by_id("id_title_of_training_course", "Title of training course")
        self.task_executor.send_keys_by_id("id_course_date_0", "12")
        self.task_executor.send_keys_by_id("id_course_date_1", "12")
        self.task_executor.send_keys_by_id("id_course_date_2", "2017")
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.assertPageTitleAtTaskSummaryPage("Check your answers: first aid training")
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.task_executor.wait_until_page_load("Register as a nanny")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='first_aid_training']/td/a/strong").text)
