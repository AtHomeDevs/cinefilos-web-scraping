from selenium.webdriver.remote.webelement import WebElement

from src.cineshow_beiramar.model.CineshowMovieScheduleData import CineshowMovieScheduleData


class CineshowDataHandler:
    __final_data = CineshowMovieScheduleData()

    def handle_html_elements(self, elements):
        for movie_html_element in elements:
            movie_data = self.__split_movie_data(movie_html_element)
            self.__remove_labels_from_movie_data(movie_data)
            movie = movie_data[:9]
            sessions_data = movie_data[7:]
            rooms = []
            audios = []
            sessions = []
            movie_sessions = []

            i = 0
            while i < len(sessions_data):
                separate_session_data = self.__separate_sessions(sessions_data, i)
                rooms = separate_session_data[0]
                audios = separate_session_data[1]
                movie_sessions = separate_session_data[2]

            movie_sessions.append(sessions)
            self.__append_movie_data(movie, rooms, audios, movie_sessions)
        return self.__final_data

    def __split_movie_data(self, element):
        movie_html_element_value = element.text
        return movie_html_element_value.split('\n')

    def __remove_labels_from_movie_data(self, movie_data: list):
        for data in movie_data:
            if data[-1:] == ':':
                movie_data.pop(movie_data.index(data))

    # TODO: Precisamos tratar o if/else desta função para pegar a informação 3D/2D
    def __separate_sessions(self, sessions_data: list, session_data_index: int):
        data = sessions_data[session_data_index]
        rooms = []
        audios = []
        sessions = []
        movie_sessions = []

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
        return rooms, audios, movie_sessions

    def __append_movie_data(self, movie: dict, rooms: list, audios: list, movie_sessions: list):
        self.__final_data.append_movie_title(movie[0])
        self.__final_data.append_indicative_rating(movie[2])
        self.__final_data.append_genre(movie[3])
        self.__final_data.append_minutes(movie[4])
        self.__final_data.append_studio(movie[5])
        self.__final_data.append_premiere_date(movie[6])
        self.__final_data.append_movie_theater_room(rooms)
        self.__final_data.append_audio(audios)
        self.__final_data.append_session_hour(movie_sessions)

    def filter_html_elements(self, movie_html_element: WebElement):
        movie_html_element_value = movie_html_element.text
        movie_data = movie_html_element_value.split('\n')
        if movie_data[0] != '':
            return True
        return False

    def clear_final_data(self):
        self.__final_data.clear_values()

