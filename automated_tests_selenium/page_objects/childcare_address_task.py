from django.test import TestCase


class ChildcareAddressTask(TestCase):

    def __init__(self, task_executor, *args, **kwargs):
        """
        Default constructor
        """
        self.task_executor = task_executor
        super(ChildcareAddressTask, self).__init__(*args, **kwargs)

    def complete_childcare_address(self):
        driver = self.task_executor.get_driver()
        self.assertEqual("To do", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)
        self.task_executor.click_element_by_xpath("//tr[@id='childcare_address']/td/a/span")
        self.task_executor.click_element_by_xpath("//input[@value='Continue']")
        self.task_executor.click_element_by_id("id_address_to_be_provided_0")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_id("id_home_address_0")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_xpath("//input[@value='Save and continue']")
        self.task_executor.click_element_by_xpath("//*[@value='Confirm and continue']")
        self.assertEqual("Done", driver.find_element_by_xpath("//tr[@id='childcare_address']/td/a/strong").text)
