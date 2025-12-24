from api.auth_api import AuthApi
from api.user_api import UserApi
from api.movies_api import MoviesApi

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP структурой
    """

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserApi(session)
        self.movies_api = MoviesApi(session)