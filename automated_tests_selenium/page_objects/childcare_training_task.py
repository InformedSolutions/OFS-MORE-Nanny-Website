from django.test import TestCase


class ChildcareTrainingTask(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(ChildcareTrainingTask, self).__init__(*args, **kwargs)

    def complete_childcare_training(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)
        driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/span").click()
        driver.find_element_by_id("id_continue").click()
        self.task_executor.click_element_by_id("id_childcare_training_0")
        self.task_executor.click_element_by_id("id_childcare_training_1")
        self.task_executor.click_element_by_id("id_continue")
        self.task_executor.wait_until_page_load("Check your answers: childcare training")
        self.assertEqual("Check your answers: childcare training", driver.title)
        self.task_executor.click_element_by_id("id_continue")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_training']/td/a/strong").text)
