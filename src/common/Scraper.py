from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Scraper:
    driver = Chrome()

    def open_url(self, url:str):
        self.driver.get(url)

    def get_elements_by_class(self, html_class:str):
        return self.driver.find_elements(by=By.CLASS_NAME, value=html_class)

    def get_element_by_class(self, html_class:str):
        return self.driver.find_element(by=By.CLASS_NAME, value=html_class)

    def get_element_by_id(self, element_id:str):
        return self.driver.find_element(by=By.ID, value=element_id)

    def get_element_by_xpath(self, xpath:str):
        return self.driver.find_element(by=By.XPATH, value=xpath)

    @staticmethod
    def click_on_element(element:WebElement):
        element.click()

    @staticmethod
    def get_element_children_by_class(element:WebElement, children_class:str):
        return element.find_elements(by=By.CLASS_NAME, value=children_class)

    def set_elements_display_to_block(self, element_class:str):
        self.driver.execute_script(f"document.querySelector('{element_class}').style.display = 'block';")

