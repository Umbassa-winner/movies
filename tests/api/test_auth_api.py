from api.api_manager import ApiManager

class TestAuthAPI:

    def test_register_user(self, test_user, api_manager, creds_user):

        """
        Тест на регистрацию
        """

        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

        # Подчищаем данные
        api_manager.auth_api.authenticate(creds_user)
        api_manager.user_api.clean_up_user(response_data["id"])

    def test_login_user(self, api_manager: ApiManager, login_data, creds_user):
        """
        Тест на авторизацию УЖЕ зарегистрированного пользователя.
        """

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        #Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == login_data["email"], "Email не совпадает"

        # Подчищаем данные (либо через фикстуру, для этого закомментить этот блок и добавить в аргументы фикстуру clean...)
        api_manager.auth_api.authenticate(creds_user)
        api_manager.user_api.clean_up_user(response_data["user"]["id"])

    def test_delete_registered_user(self, api_manager:ApiManager, creds_user, user_id):

        """
        Тест на удаление зарегистрированного пользователя
        """

        auth = api_manager.auth_api.authenticate(creds_user)
        response = api_manager.user_api.delete_user(user_id)



        # assert response_get_user.status_code == 401, 'Пользователь не удалился'

    # def test_get_users(self, registered_user, api_manager:ApiManager):
    #
    #     # ХОЧУ ПРОВЕРИТЬ, ЧТО ЗАПРОСЫ ИДУТ ЧЕРЕЗ ОДНУ СЕССИЮ. С ПОМОЩЬЮ ПОЛУЧЕНИЯ ИНФОРМЦИИ О ПОЛЬЗОВАТЕЛЕ
    #     # ПО ИТОГУ Я ПОЛУЧАЛ ПРОСТО 403, т.к. видимо просто указать ADMIN при регистрации недостаточно.
    #     creds = (registered_user["email"], registered_user["password"])
    #     get_token = api_manager.auth_api.authenticate(creds)
    #     user_id = registered_user["id"]
    #     response_get = api_manager.user_api.get_user_info(user_id)



#====================================== ТУТ ТЕСТЫ НА НЕГАТИВНЫЕ СЦЕНАРИИ=========================================

    #
    #
    # def test_negative_login(self, registered_user, requester):
    #
    #     # 1. Попробуйте авторизоваться с несуществующим email:
    #     negative_login_data_email = {
    #         "email": "qwerty@gmail.com",
    #         "password": registered_user["password"]
    #     }
    #
    #     response_login = requester.send_request(
    #         method="POST",
    #         endpoint=LOGIN_ENDPOINT,
    #         data=negative_login_data_email,
    #         expected_status=401
    #     )
    #     assert "message" in response_login.json(), "Отсутствует сообщение об ошибке"
    #
    # def test_negative_password(self, registered_user, requester):
    #
    #     #2. Попробуйте авторизоваться с неверным паролем
    #
    #     negative_login_data_password = {
    #         "email": registered_user["email"],
    #         "password": "123"
    #     }
    #
    #     response_login = requester.send_request(
    #         method="POST",
    #         endpoint=LOGIN_ENDPOINT,
    #         data=negative_login_data_password,
    #         expected_status=401
    #     )
    #     assert "message" in response_login.json(), "Отсутствует сообщение об ошибке"
    #
    # def test_negative_login_empty_body(self, registered_user, requester):
    #
    #     #3. Попробуйте авторизоваться с пустым телом запроса
    #
    #     negative_login_empty_body = {}
    #
    #     response_login = requester.send_request(
    #         method="POST",
    #         endpoint=LOGIN_ENDPOINT,
    #         data=negative_login_empty_body,
    #         expected_status=401
    #     )
    #
    #     assert "message" in response_login.json(), "Отсутствует сообщение об ошибке"
    #
