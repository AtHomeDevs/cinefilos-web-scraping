import pandas as pd

from src.commom.Scraper import Scraper
from src.cineshow_beiramar.scrapers.CineshowBeiramarScraper import CineshowBeiramarScraper
from src.cineshow_beiramar.service.CineshowDataframe import CineshowDataframe


scraper = CineshowBeiramarScraper()
scraper.open_site()

daily_buttons_row_element = scraper.get_element_by_class('owl-stage')
button_next = scraper.get_element_by_class('owl-next')
daily_button_elements = Scraper.get_element_children_by_class(daily_buttons_row_element, 'item.abaSelect')

schedule_df = pd.DataFrame()
for daily_button_element in daily_button_elements:
    cineshow_dataframe = CineshowDataframe()
    element_index = daily_button_elements.index(daily_button_element)
    if element_index > 1:
        scraper.switch_schedule_tab(daily_button_element, button_next)

    date = scraper.get_date(daily_button_element)
    movie_html_elements = scraper.get_elements_by_class('filme')[1:]
    daily_schedule_df = cineshow_dataframe.create(movie_html_elements, date)
    schedule_df = pd.concat(objs=[schedule_df, daily_schedule_df], join='outer', axis=0, ignore_index=True)
