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

prog_day = scraper.get_element_by_class('abaProgDay')
prog_day_info = prog_day.text.split('\n')

movies_data = list()
last_list_break_index = 0
for info in prog_day_info:
    info_index = prog_day_info.index(info)
    next_info = ''
    next_info_index = info_index + 1
    if next_info_index < len(prog_day_info):
        next_info = prog_day_info[next_info_index]
    else:
        next_info = prog_day_info[info_index]

    if info[-1:] == ':':
        prog_day_info.pop(info_index)
    elif len(info) > 2 and info[2] == ':' and ':' not in next_info[2] and 'Sala' not in next_info:
        movie_data = []
        if last_list_break_index == 0:
            movie_data = prog_day_info[last_list_break_index:info_index+1]
        else:
            movie_data = prog_day_info[last_list_break_index+1:info_index+1]
        movies_data.append(movie_data)
        last_list_break_index = info_index

movies_without_session_data = []
movies = {
    'titulo_filme': [],
    'titulo_ano': [],
    'classificacao_indicativa': [],
    'genero': [],
    'duracao': [],
    'distribuidora': [],
    'estreia': [],
    'sessoes': []
}

for movie_data in movies_data:
    movies['titulo_filme'].append(movie_data[0])
    movies['titulo_ano'].append(movie_data[1])
    movies['classificacao_indicativa'].append(movie_data[2])
    movies['genero'].append(movie_data[3])
    movies['duracao'].append(movie_data[4])
    movies['distribuidora'].append(movie_data[5])
    movies['estreia'].append(movie_data[6])
    movies['sessoes'].append(movie_data[7:])

movie_info_df = pd.DataFrame(data=movies)
print(movie_info_df.columns)

