from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_MOVIES, MOVIES_ENDPOINT

class MoviesApi(CustomRequester):
    """
    Класс для работы с фильмами
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_MOVIES)

    def get_movies_list(self, expected_status=200):
        """
        Получение всех фильмов
        :param expected_status: ожидаемый статус-код
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status
        )

    def test_get_movies_list_with_parameters(self, expected_status=200, **kwargs):

        # https://api.dev-cinescope.coconutqa.ru/movies?pageSize=10&page=1&minPrice=1&maxPrice=1000&locations=MSK&locations=SPB&published=true&genreId=1&createdAt=asc

        """
        :param expected_status: ожидаемый статус-код
        :param kwargs: передаваемые фильтры в формате ключ=значение. Пример: pageSize=10, page=1
        """

        #Составляем строку из GET параметров, чтобы подставить ее в эндпоинт.
        get_parameters = ""
        max = len(kwargs)
        count = 0

        # Формируем строку формата "ключ=знач&ключ=знач&ключ=знач..."на неогр. число параметров
        for i, k in kwargs.items():
            together = f"{i}={str(k)}"
            get_parameters+=together
            if count < (max - 1):
                get_parameters+="&"
                count += 1

        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}?{get_parameters}",
            expected_status=expected_status
        )

    def create_movie(self, create_movie_data, expected_status=201):
        """
        Создание фильма
        :param create_movie_data: данные для создания фильма
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=create_movie_data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        """
        Получение конкретного фильма по ID
        :param movie_id: ID фильма
        :param expected_status: ожидаемый статус-код
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление фильма по ID
        :param movie_id: ID фильма
        :param expected_status: ожидаемый статус-код
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
        )

    def edit_movie(self, movie_id, edit_movie_data, expected_status=200):
        """
        Редактирование конкретного фильма по ID
        :param movie_id: ID фильма
        :param edit_movie_data: измененный JSON c данными фильма
        :return:
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=edit_movie_data,
            expected_status=expected_status

        )
