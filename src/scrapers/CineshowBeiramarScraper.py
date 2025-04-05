from selenium.webdriver.remote.webelement import WebElement

from src.scrapers.Scraper import Scraper


class CineshowBeiramarScraper(Scraper):

    def open_site(self):
        self.open_url('https://www.cineshow.com.br/beiramar/programacao')
        button_to_click = self.get_element_by_xpath('//*[@id="modalCinemas"]/div/div/div[2]/div/div[5]/button')
        Scraper.click_on_element(button_to_click)

    def switch_schedule_tab(self, daily_button_element: WebElement, button_next: WebElement):
        Scraper.click_on_element(daily_button_element)
        Scraper.click_on_element(button_next)

    def get_date(self, date_element: WebElement):
        daily_button_element_content = date_element.text.split('\n')
        return daily_button_element_content[0]