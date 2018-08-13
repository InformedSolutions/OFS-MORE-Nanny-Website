from django.test import TestCase


class InsuranceCoverTask(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(InsuranceCoverTask, self).__init__(*args, **kwargs)

    def complete_insurance_cover(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='insurance_cover']/td/a/span")
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.click_element_by_id("id_public_liability_0")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.wait_until_page_load("Check your answers: insurance cover")
        self.assertEqual("Check your answers: insurance cover", driver.title)
        self.task_executor.click_element_by_id("id_continue")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='insurance_cover']/td/a/strong").text)
