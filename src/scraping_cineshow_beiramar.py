import pandas as pd

from Scraper import Scraper


scraper = Scraper()

scraper.open_url('https://www.cineshow.com.br/beiramar/programacao')
button = scraper.click_button('//*[@id="modalCinemas"]/div/div/div[2]/div/div[5]/button')

# For para percorrer todas as abas/dias de exibição de filme.
# for i in range(1, 12):
#     print(i)
#     scraper.switch_element_display(f'.content-programacao.abaProgDay.aba_{i}')

scraper.switch_element_display(f'.content-programacao.abaProgDay.aba_0')

prog_day = scraper.get_elements_by_class('filme')[1:]

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

def remove_unnecessary_session_data(session:list):
    for data in session:
        if 'Sala' in data:
            session.pop(session.index(data))
    for data in session:
        if len(data) == 3:
            session.pop(session.index(data))

def get_date():
    aba_select = scraper.get_element_by_class('abaSelect')
    aba_select_content = aba_select.text.split('\n')
    return aba_select_content[0]

for info in prog_day:
    movie_data = info.text.split('\n')
    if len(movie_data) > 1:
        for data in movie_data:
            if data[-1:] == ':':
                movie_data.pop(movie_data.index(data))

        movie = movie_data[:9]
        sessions_data = movie_data[7:]
        last_list_break_index = 0
        rooms = []
        audios = []
        movie_sessions = []
        for data in sessions_data:
            if 'Sala' in data:
                rooms.append(data)
            elif len(data) == 3:
                audios.append(data)

            current_index = sessions_data.index(data)
            if current_index + 1 < len(sessions_data):
                next_index = current_index + 1
                next_data = sessions_data[next_index]

                if ':' in data and ':' not in next_data:
                    session = sessions_data[last_list_break_index:next_index]
                    remove_unnecessary_session_data(session)
                    movie_sessions.append(session)
                    last_list_break_index = next_index
            else:
                session = sessions_data[last_list_break_index:]
                remove_unnecessary_session_data(session)
                movie_sessions.append(session)

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

df = pd.DataFrame(data=movies).explode(['sala', 'audio', 'sessoes']).explode('sessoes').reset_index(drop=True)

date = get_date()
date_series = pd.Series([date])
date_series = date_series.repeat(repeats=df.shape[0]).reset_index(drop=True)
df['data'] = date_series
