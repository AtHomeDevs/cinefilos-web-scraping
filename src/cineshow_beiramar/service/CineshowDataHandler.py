from selenium.webdriver.remote.webelement import WebElement

from src.cineshow_beiramar.model.CineshowMovieScheduleData import CineshowMovieScheduleData


class CineshowDataHandler:
    __final_data = CineshowMovieScheduleData()
    __rooms = []
    __audios = []
    __sessions = []
    __movie_sessions = []

    def handle_html_elements(self, elements):
        for movie_html_element in elements:
            movie_data = self.__split_movie_data(movie_html_element)
            self.__remove_labels_from_movie_data(movie_data)
            movie = movie_data[:9]
            sessions_data = movie_data[7:]

            i = 0
            while i < len(sessions_data):
                self.__separate_sessions_data(sessions_data, i)

            self.__movie_sessions.append(self.__sessions)
            self.__append_movie_data(movie)
            self.__rooms = []
            self.__audios = []
            self.__sessions = []
            self.__movie_sessions = []
        return self.__final_data

    def __split_movie_data(self, element):
        movie_html_element_value = element.text
        return movie_html_element_value.split('\n')

    def __remove_labels_from_movie_data(self, movie_data: list):
        for data in movie_data:
            if data[-1:] == ':':
                movie_data.pop(movie_data.index(data))

    # TODO: Precisamos tratar o if/else desta função para pegar a informação 3D/2D
    def __separate_sessions_data(self, sessions_data: list, session_data_index: int):
        data = sessions_data[session_data_index]

        if 'Sala' in data:
            self.__rooms.append(data)
            if len(self.__sessions) > 0:
                self.__movie_sessions.append(self.__sessions.copy())
                self.__sessions.clear()
        elif len(data) == 3:
            self.__audios.append(data)
        elif ':' in data:
            self.__sessions.append(data)

        sessions_data.pop(sessions_data.index(data))

    def __append_movie_data(self, movie: dict):
        self.__final_data.append_movie_title(movie[0])
        self.__final_data.append_indicative_rating(movie[2])
        self.__final_data.append_genre(movie[3])
        self.__final_data.append_minutes(movie[4])
        self.__final_data.append_studio(movie[5])
        self.__final_data.append_premiere_date(movie[6])
        self.__final_data.append_movie_theater_room(self.__rooms)
        self.__final_data.append_audio(self.__audios)
        self.__final_data.append_session_hour(self.__movie_sessions)

    def filter_html_elements(self, movie_html_element: WebElement):
        movie_html_element_value = movie_html_element.text
        movie_data = movie_html_element_value.split('\n')
        if movie_data[0] != '':
            return True
        return False

    def clear_final_data(self):
        self.__final_data.clear_values()

