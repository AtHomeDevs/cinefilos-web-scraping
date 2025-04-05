class CineshowMovieScheduleData:
    __movie_title = []
    __indicative_rating = []
    __genre = []
    __minutes = []
    __studio = []
    __premiere_date = []
    __movie_theater_room = []
    __audio = []
    __session_hour = []

    def append_movie_title(self, new_movie_title:str):
        self.__movie_title.append(new_movie_title)

    def append_indicative_rating(self, new_indicative_rating:str):
        self.__indicative_rating.append(new_indicative_rating)

    def append_genre(self, new_genre:str):
        self.__genre.append(new_genre)

    def append_minutes(self, new_minutes):
        self.__minutes.append(new_minutes)

    def append_studio(self, new_studio):
        self.__studio.append(new_studio)

    def append_premiere_date(self, new_premiere_date):
        self.__premiere_date.append(new_premiere_date)

    def append_movie_theater_room(self, new_movie_theater_room):
        self.__movie_theater_room.append(new_movie_theater_room)

    def append_audio(self, new_audio):
        self.__audio.append(new_audio)

    def append_session_hour(self, new_session_hour):
        self.__session_hour.append(new_session_hour)

    def as_dict(self):
        return {
            'titulo_filme': self.__movie_title,
            'classificacao_indicativa': self.__indicative_rating,
            'genero': self.__genre,
            'duracao': self.__minutes,
            'distribuidora': self.__studio,
            'estreia': self.__premiere_date,
            'sala': self.__movie_theater_room,
            'audio': self.__audio,
            'sessoes': self.__session_hour
        }

    def clear_values(self):
        self.__movie_title = []
        self.__indicative_rating = []
        self.__genre = []
        self.__minutes = []
        self.__studio = []
        self.__premiere_date = []
        self.__movie_theater_room = []
        self.__audio = []
        self.__session_hour = []