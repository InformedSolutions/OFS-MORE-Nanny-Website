from django.test import TestCase


class CriminalRecordCheckTask(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(CriminalRecordCheckTask, self).__init__(*args, **kwargs)

    def complete_criminal_record(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='criminal_record']/td/a/span")
        self.task_executor.click_element_by_link_text("Continue")
        self.task_executor.click_element_by_id("id_dbs_number")
        self.task_executor.send_keys_by_id("id_dbs_number", "123456789098")
        self.task_executor.click_element_by_id("id_convictions_1")
        self.task_executor.click_element_by_name("action")
        self.task_executor.click_element_by_xpath("//input[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='criminal_record']/td/a/strong").text)
