import pandas as pd

from src.cineshow_beiramar.service.CineshowDataHandler import CineshowDataHandler


class CineshowDataframe:
    __data_handler = CineshowDataHandler()

    def create(self, elements, date):
        filtered_movie_html_elements = list(filter(self.__data_handler.filter_html_elements, elements))
        movies = self.__data_handler.handle_html_elements(filtered_movie_html_elements)
        movies_dict = movies.as_dict()
        self.__data_handler.clear_final_data()

        df = pd.DataFrame(data=movies_dict)
        df = df.explode(['sala', 'audio', 'sessoes']).reset_index(drop=True)
        df = df.explode('sessoes').reset_index(drop=True)
        df_date_column = self.__create_df_date_column(df.shape[0], date)
        df['data'] = df_date_column
        return df

    def __create_df_date_column(self, repeats: int, date: str):
        date_series = pd.Series([date])
        date_series = date_series.repeat(repeats=repeats).reset_index(drop=True)
        return date_series

