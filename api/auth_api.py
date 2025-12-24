from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_AUTH, REGISTER_ENDPOINT, LOGIN_ENDPOINT

class AuthApi(CustomRequester):

    """
    Класс для работы с аутентификацией
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_AUTH)

    def register_user(self, user_data, expected_status = 201):
        """
        Регистрация пользователя нового
        :param user_data:
        :param expected_status:
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status = 200):
        """
        Авторизация зарегистрированного пользователя
        :param login_data:
        :param expected_status:
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):

        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("Token is Missing")

        token = response.get("accessToken")
        self._update_session_headers(self.session, **{"Authorization": "Bearer " + token})

