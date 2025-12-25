from api.api_manager import ApiManager

class TestPositiveMoviesApi:

    def test_negative_get_movie_list_with_parameters(self, api_manager:ApiManager, negative_data_for_filter):

        """
        Негативный тест на получение списка фильмов с ФИЛЬТРАМИ по цене
        """

        response = api_manager.movies_api.test_get_movies_list_with_parameters(400, minPrice=negative_data_for_filter[0], maxPrice=negative_data_for_filter[1])
        response_data = response.json()

        assert response.status_code == 400, "Неверный статус код"
        assert "message" in response.text, "Отсутствует сообщение об ошибке"
        assert response_data["message"][0] == "Поле minPrice имеет минимальную величину 1", "Отсутствует сообщение об ошибке minPrice_мин.велечина_1"
        assert response_data["message"][1] == "Поле minPrice должно быть числом", "Отсутствует сообщение об ошибке minPrice_число"
        assert response_data["message"][2] == "Поле minPrice имеет минимальную величину 1", "Отсутствует сообщение об ошибке minPrice_мин.велечина_2"


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

    def test_negative_double_create_movie(self, api_manager:ApiManager, test_movie, creds_super_admin, clean_movie):

        """
        Негативный тест на создание 2-го фильма с аналогичными данными
        """

        login = api_manager.auth_api.authenticate(creds_super_admin)
        response = api_manager.movies_api.create_movie(test_movie)
        response_wrong = api_manager.movies_api.create_movie(test_movie, 409)

        # response_data = response.json()
        # request_from_response_wrong_data = response_wrong.request.body
        #
        # # assert "message" in response.text, "Отсутствует сообщение об ошибке"
        # assert response_data["name"] == test_movie["name"], "Имена у фильмов не совпадают. Ошибка выходит некорректно"
        #
        # # Подчищаем данные
        # clean_movie(response_data["id"])

    # def test_negative_get_movie(self, api_manager, created_movie):
    #
    #     """
    #     Негативный тест на получение фильма по АЙДИ
    #     """
    #
    #     response = api_manager.movies_api.get_movie(created_movie["id"])
    #     response_data = response.json()
    #
    #     assert "reviews" in response_data, "Отзывы фильма отсутствуют"
    #     assert created_movie["location"] == response_data["location"], "Локация фильма не совпадает"
    #     assert created_movie["published"] == response_data["published"], "Опубликованность фильма не совпадает"
    #
    #
    # def test_negative_delete_movie(self, api_manager, created_movie, check_movie_for_delete):
    #
    #     """
    #     Негативный тест на удаление фильма
    #     """
    #
    #     response = api_manager.movies_api.delete_movie(created_movie["id"])
    #     response_data = response.json()
    #
    #     assert check_movie_for_delete(created_movie["id"]), "Фильм не удалился"
    #
    # def test_negative_patch_movie(self, api_manager, created_movie, test_movie_for_patch):
    #
    #     """
    #     Негативный тест на изменение фильма
    #     """
    #
    #     response = api_manager.movies_api.edit_movie(created_movie["id"], test_movie_for_patch)
    #     response_data = response.json()
    #
    #     assert test_movie_for_patch["name"] == response_data["name"], "Имя не изменилось"
    #     assert test_movie_for_patch["description"] == response_data["description"], "Имя не изменилось"
