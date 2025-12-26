from api.api_manager import ApiManager
import json

class TestPositiveMoviesApi:

    def test_negative_get_movie_list_with_parameters(self, api_manager:ApiManager, negative_data_for_filter):

        """
        Негативный тест на получение списка фильмов с ФИЛЬТРАМИ по цене
        """

        response = api_manager.movies_api.test_get_movies_list_with_parameters(400, minPrice=negative_data_for_filter[0], maxPrice=negative_data_for_filter[1])
        response_data = response.json()

        assert response.status_code == 400, "Неверный статус код"
        assert "message" in response.text, "Отсутствует сообщение об ошибке"
        assert response_data["message"][0] == "Поле minPrice имеет минимальную величину 1", "Отсутствует сообщение об ошибке minPrice_мин.величина_1"
        assert response_data["message"][1] == "Поле minPrice должно быть числом", "Отсутствует сообщение об ошибке minPrice_число"
        assert response_data["message"][2] == "Поле minPrice имеет минимальную величину 1", "Отсутствует сообщение об ошибке minPrice_мин.величина_2"


    def test_negative_create_movie_without_four_param(self, api_manager:ApiManager, negative_test_movie_without_four_param, creds_super_admin):
        """
        Негативный тест на создание фильма без 4 параметров
        """

        login = api_manager.auth_api.authenticate(creds_super_admin)
        response = api_manager.movies_api.create_movie(negative_test_movie_without_four_param, 400)
        response_data = response.json()

        assert "message" in response.text, "Отсутствует сообщение об ошибке"

    def test_negative_create_movie_with_wrong_type_data(self, api_manager:ApiManager, negative_test_movie_with_wrong_type_data, creds_super_admin):
        """
        Негативный тест на создание фильма с неправильно преданным типом данных
        """

        login = api_manager.auth_api.authenticate(creds_super_admin)
        response = api_manager.movies_api.create_movie(negative_test_movie_with_wrong_type_data, 400)
        response_data = response.json()

        assert "message" in response.text, "Отсутствует сообщение об ошибке"

    def test_negative_create_movie_with_empty_json(self, api_manager:ApiManager, creds_super_admin, negative_test_movie_empty_json):
        """
        Негативный тест на создание фильма с пустым JSON
        """

        login = api_manager.auth_api.authenticate(creds_super_admin)
        response = api_manager.movies_api.create_movie(negative_test_movie_empty_json, 400)
        response_data = response.json()

        assert "message" in response.text, "Отсутствует сообщение об ошибке"

    def test_negative_create_double_movie(self, api_manager:ApiManager, test_movie, creds_super_admin, clean_movie):

        """
        Негативный тест на создание 2-го фильма с аналогичными данными
        """

        login = api_manager.auth_api.authenticate(creds_super_admin)
        response = api_manager.movies_api.create_movie(test_movie)
        response_with_error = api_manager.movies_api.create_movie(test_movie, 409)
        response_data = response.json()

        #Декодируем байтовые данные из request.body в чпн символы с помощью .decode('utf-8')
        #Используем модуль json, чтобы преобразовать строку вида '{"key":"value"}' в dict
        request_from_response_wrong_data = json.loads(response_with_error.request.body.decode('utf-8'))

        assert "message" in response_with_error.text, "Отсутствует сообщение об ошибке"
        assert response_data["name"] == request_from_response_wrong_data["name"], "Имена у фильмов не совпадают. Ошибка выводится некорректно"

        # Подчищаем данные
        clean_movie(response_data["id"])

    def test_negative_get_movie_with_fake_id(self, api_manager, negative_id):

        """
        Негативный тест на получение фильма по АЙДИ
        """

        response = api_manager.movies_api.get_movie(negative_id, 404)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"


    def test_negative_delete_movie_without_token(self, api_manager, negative_id, clear_headers):

        """
        Негативный тест на удаление фильма без авторизации
        """

        response = api_manager.movies_api.delete_movie(negative_id, 401)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"

    def test_negative_delete_movie_with_wrong_id(self, api_manager, login_and_auth, negative_id):

        """
        Негативный тест на удаление несуществующего фильма
        """

        response = api_manager.movies_api.delete_movie(negative_id, 404)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"

    def test_negative_patch_movie_with_wrong_data(self, api_manager, created_movie, negative_test_movie_with_wrong_type_data):

        """
        Негативный тест на изменение фильма
        """

        response = api_manager.movies_api.edit_movie(created_movie["id"], negative_test_movie_with_wrong_type_data, 400)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"

    def test_negative_patch_movie_with_wrong_id(self, api_manager, created_movie, negative_id, test_movie_for_patch):
        """
        Негативный тест на изменение фильма
        """

        response = api_manager.movies_api.edit_movie(negative_id, test_movie_for_patch, 404)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"

