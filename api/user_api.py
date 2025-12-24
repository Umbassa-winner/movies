from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_AUTH

class UserApi(CustomRequester):

    """
    Класс для работы с Юзером
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_AUTH)

    def get_user_info(self, user_id, expected_status=200):
        """
        :param user_id: ID пользователя
        :param expected_status: ожидаемый статус-код
        """
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        """
        :param user_id: ID пользователя, которое хотим удалить
        :param expected_status: ожидаемый статус-код
        """

        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def clean_up_user(self, user_id, expected_status=200):
        """
        :param user_id: ID пользователя, которое хотим ОЧИСТИТЬ ПОСЛЕ ТЕСТОВ
        :param expected_status: ожидаемый статус-код
        """

#         1. Создать генератор отдельный от регистеред юзер, который будет использоваться фикстурой подчистки
#         2. Сделать условие, что если не было авторизации (нет access токена у пользователя), то мы берем
        #    его данные для авторизации и аутентификации соотв. Если есть, то берем этот токен для удаления.

        return self.send_request(
            method="DELETE",
            endpoint= f"/user/{user_id}",
            expected_status=expected_status
        )

