import pandas as pd
from selenium.webdriver.remote.webelement import WebElement

from src.scrapers.Scraper import Scraper

"""
START FUNCTIONS
"""
def open_site(scraper:Scraper):
    scraper.open_url('https://www.cineshow.com.br/beiramar/programacao')
    button_to_click = scraper.get_element_by_xpath('//*[@id="modalCinemas"]/div/div/div[2]/div/div[5]/button')
    scraper.click_on_element(button_to_click)

def get_site_data(scraper:Scraper):
    return scraper.get_elements_by_class('filme')[1:]

def get_daily_buttons_row_element(scraper:Scraper):
    return scraper.get_element_by_class('owl-stage')

def switch_schedule_tab(scraper:Scraper, daily_button_element:WebElement, button_next:WebElement):
    scraper.click_on_element(daily_button_element)
    scraper.click_on_element(button_next)

def get_date(date_element:WebElement):
    daily_button_element_content = date_element.text.split('\n')
    return daily_button_element_content[0]

def filter_html_elements(movie_html_element:WebElement):
    movie_html_element_value = movie_html_element.text
    movie_data = movie_html_element_value.split('\n')
    if movie_data[0] != '':
        return True
    return False

def remove_labels_from_movie_data(movie_data:list):
    for data in movie_data:
        if data[-1:] == ':':
            movie_data.pop(movie_data.index(data))

""" 
TODO: Precisamos tratar o if/else desta função para pegar a informação 3D/2D. O site só informa quando é 3D, ou seja, 2D é o 
padrão
"""
def separate_sessions(sessions_data:list, i:int, rooms:list, audios:list, sessions:list, movie_sessions:list):
    data = sessions_data[i]

    if 'Sala' in data:
        rooms.append(data)

        if len(sessions) > 0:
            movie_sessions.append(sessions.copy())
            sessions.clear()
    elif len(data) == 3:
        audios.append(data)
    elif ':' in data:
        sessions.append(data)

    sessions_data.pop(sessions_data.index(data))

def append_movie_data(movie:dict, rooms:list, audios:list, movie_sessions:list):
    movies['titulo_filme'].append(movie[0])
    movies['titulo_ano'].append(movie[1])
    movies['classificacao_indicativa'].append(movie[2])
    movies['genero'].append(movie[3])
    movies['duracao'].append(movie[4])
    movies['distribuidora'].append(movie[5])
    movies['estreia'].append(movie[6])
    movies['sala'].append(rooms)
    movies['audio'].append(audios)
    movies['sessoes'].append(movie_sessions)

def create_df_date_column(repeats:int, date:str):
    date_series = pd.Series([date])
    date_series = date_series.repeat(repeats=repeats).reset_index(drop=True)
    return date_series

def clear_movies_dictionary(movies:dict):
    movies['titulo_filme'] = []
    movies['titulo_ano'] = []
    movies['classificacao_indicativa'] = []
    movies['genero'] = []
    movies['duracao'] = []
    movies['distribuidora'] = []
    movies['estreia'] = []
    movies['sala'] = []
    movies['audio'] = []
    movies['sessoes'] = []

def create_daily_schedule_dataframe(movies:dict, filtered_movie_html_elements, date:str):
    for movie_html_element in filtered_movie_html_elements:
        movie_html_element_value = movie_html_element.text
        movie_data = movie_html_element_value.split('\n')

        if len(movie_data) > 1:
            remove_labels_from_movie_data(movie_data)
            movie = movie_data[:9]
            sessions_data = movie_data[7:]
            rooms = []
            audios = []
            sessions = []
            movie_sessions = []
            i = 0
            while i < len(sessions_data):
                separate_sessions(sessions_data, i, rooms, audios, sessions, movie_sessions)

            movie_sessions.append(sessions)
            append_movie_data(movie, rooms, audios, movie_sessions)

    df = pd.DataFrame(data=movies)
    df = df.explode(['sala', 'audio', 'sessoes']).reset_index(drop=True)
    df = df.explode('sessoes').reset_index(drop=True)

    df_date_column = create_df_date_column(df.shape[0], date)
    df['data'] = df_date_column
    clear_movies_dictionary(movies)
    return df

"""
END FUNCTIONS
"""

movies = {
    'titulo_filme': [],
    'titulo_ano': [],
    'classificacao_indicativa': [],
    'genero': [],
    'duracao': [],
    'distribuidora': [],
    'estreia': [],
    'sala': [],
    'audio': [],
    'sessoes': []
}

scraper = Scraper()

open_site(scraper)

daily_buttons_row_element = get_daily_buttons_row_element(scraper)
button_next = scraper.get_element_by_class('owl-next')
daily_button_elements = scraper.get_element_children_by_class(daily_buttons_row_element, 'item.abaSelect')

schedule_df = pd.DataFrame(data=movies)
for daily_button_element in daily_button_elements:
    element_index = daily_button_elements.index(daily_button_element)
    if element_index > 1:
        switch_schedule_tab(scraper, daily_button_element, button_next)

    date = get_date(daily_button_element)
    movie_html_elements = get_site_data(scraper)
    filtered_movie_html_elements = filter(filter_html_elements, movie_html_elements)
    daily_schedule_df = create_daily_schedule_dataframe(movies, filtered_movie_html_elements, date)
    schedule_df = pd.concat(objs=[schedule_df, daily_schedule_df], join='outer', axis=0, ignore_index=True)
