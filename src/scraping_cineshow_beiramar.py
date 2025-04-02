import pandas as pd

from src.scrapers.Scraper import Scraper

"""
START FUNCTIONS
"""
def get_site_data(scraper):
    scraper.open_url('https://www.cineshow.com.br/beiramar/programacao')
    scraper.click_button('//*[@id="modalCinemas"]/div/div/div[2]/div/div[5]/button')

    # Percorrer todas as abas/dias de exibição de filme.
    # for i in range(1, 12):
    #     print(i)
    #     scraper.switch_element_display(f'.content-programacao.abaProgDay.aba_{i}')

    scraper.switch_element_display(f'.content-programacao.abaProgDay.aba_0')
    return scraper.get_elements_by_class('filme')[1:]


def filter_html_elements(movie_html_element):
    movie_html_element_value = movie_html_element.text
    movie_data = movie_html_element_value.split('\n')
    if movie_data[0] != '':
        return True
    return False

def remove_labels_from_movie_data(movie_data:list):
    for data in movie_data:
        if data[-1:] == ':':
            movie_data.pop(movie_data.index(data))

def separate_sessions(sessions_data, i, rooms, audios, sessions):
    data = sessions_data[i]

    if 'Sala' in data:
        rooms.append(data)

        if len(sessions) > 0:
            movie_sessions.append(sessions.copy())
            sessions.clear()
    elif len(data) == 3:
        audios.append(data)
    else:
        sessions.append(data)

    sessions_data.pop(sessions_data.index(data))

def append_movie_data(movie, rooms, audios, movie_sessions):
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

def get_date():
    aba_select = scraper.get_element_by_class('abaSelect')
    aba_select_content = aba_select.text.split('\n')
    return aba_select_content[0]

def add_date_on_df(df, date):
    date_series = pd.Series([date])
    date_series = date_series.repeat(repeats=df.shape[0]).reset_index(drop=True)
    df['data'] = date_series
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

movie_html_elements = get_site_data(scraper)
filtered_movie_html_elements = filter(filter_html_elements, movie_html_elements)

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
            separate_sessions(sessions_data, i, rooms, audios, sessions)

        movie_sessions.append(sessions)
        append_movie_data(movie, rooms, audios, movie_sessions)

df = pd.DataFrame(data=movies)
df = df.explode(['sala', 'audio', 'sessoes']).reset_index(drop=True)
df = df.explode('sessoes').reset_index(drop=True)

date = get_date()
add_date_on_df(df, date)
