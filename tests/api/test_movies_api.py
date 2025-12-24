from api.api_manager import ApiManager

class TestPositiveMoviesApi:

    def test_get_movie_list(self, api_manager:ApiManager):

        response = api_manager.movies_api.get_movies_list()
        response_data = response.json()

        assert "movies" in response_data, "Список фильмов отсутствует"
        assert isinstance(response_data["movies"], list), "movies вернулся не как список"

    def test_get_movie_list_with_parameters(self, api_manager:ApiManager, data_for_filter):

        response = api_manager.movies_api.test_get_movies_list_with_parameters(minPrice=data_for_filter[0], maxPrice=data_for_filter[1])
        response_data = response.json()

        #Обычные проверки без for не подходят, т.к. не покрывают полностью
        assert all(i["price"] >= data_for_filter[0] for i in response_data["movies"]), "Фильтр по мин. и макс. цене работает некорректно"
        assert all(i["price"] <= data_for_filter[1] for i in response_data["movies"]), "Фильтр по мин. и макс. цене работает некорректно"

    def test_create_movie(self, api_manager:ApiManager, test_movie, creds_super_admin):

        login = api_manager.auth_api.authenticate(creds_super_admin)
        response = api_manager.movies_api.create_movie(test_movie)
        response_data = response.json()

        assert "id" in response_data, "id фильма отсутствует"
        assert test_movie["name"] == response_data["name"], "Имя фильма не совпадает"
        assert test_movie["price"] == response_data["price"], "Цена фильма не совпадает"

    def test_get_movie(self, api_manager, created_movie):

        response = api_manager.movies_api.get_movie(created_movie["id"])
        response_data = response.json()

        assert "reviews" in response_data, "Отзывы фильма отсутствуют"
        assert created_movie["location"] == response_data["location"], "Локация фильма не совпадает"
        assert created_movie["published"] == response_data["published"], "Опубликованность фильма не совпадает"

    def test_delete_movie(self, api_manager, created_movie, check_movie_for_delete):
        response = api_manager.movies_api.delete_movie(created_movie["id"])
        response_data = response.json()

        assert check_movie_for_delete(created_movie["id"]), "Фильм не удалился"



