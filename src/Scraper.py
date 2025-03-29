from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

class Scraper:
    driver = Chrome()

    def open_url(self, url:str):
        self.driver.get(url)

    def close_url(self):
        self.driver.quit()

    def get_elements_by_class(self, html_class:str):
        return self.driver.find_elements(by=By.CLASS_NAME, value=html_class)

    def get_element_by_id(self, element_id:str):
        return self.driver.find_element(by=By.ID, value=element_id)

    def get_element_by_xpath(self, xpath:str):
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def click_button(self, xpath:str):
        return self.get_element_by_xpath(xpath).click()

    def switch_element_display(self, element_class:str):
        self.driver.execute_script(f"document.querySelector('{element_class}').style.display = 'block';")
