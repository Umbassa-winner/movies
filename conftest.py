import requests
import pytest
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
# from constants import REGISTER_ENDPOINT, BASE_URL
# from custom_requester.custom_requester import CustomRequester

"""============================================= AUTH API ================================================"""

@pytest.fixture(scope="session")
def session():
    """
    Создание единой для всех тестов сессии, которая закрывается после выполнения теста.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра Api_Manager
    """
    return ApiManager(session)

@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(test_user, api_manager):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя с ID
    """

    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="function")
def login_data (registered_user):
    """
    :return: Возвращает dict email и password для логина
    """

    return {
                "email": registered_user ["email"],
                "password": registered_user ["password"]
            }

@pytest.fixture(scope="function")
def creds_user (test_user):
    """
    :return: возвращает кортеж из кредов для аутентификации в качестве USER
    """
    return (test_user["email"], test_user["password"])

@pytest.fixture(scope="function")
def user_id (registered_user):
    """
    :return: возвращает id зарегистрированного пользователя
    """
    return registered_user["id"]

@pytest.fixture(scope="function")
def clean_up_user_for_other_except_register(api_manager, registered_user, creds):
    """
    Автоматическая очистка тестовых данных зареганых после тестов
    """
    yield None

    api_manager.auth_api.authenticate(creds)
    api_manager.user_api.clean_up_user(registered_user["id"])

# ПОПРОБОВАТЬ С user_id

"""=========================================== MOVIE API =============================================="""

@pytest.fixture(scope="function")
def creds_super_admin():
    """
    Возвращает кортеж из кредов для аутентификации как SUPER_ADMIN
    """
    # return DataGenerator.generate_admin_creds()
    return ("api1@gmail.com", "asdqwe123Q")

@pytest.fixture(scope="function")
def data_for_filter():
    """
    Данные для фильтра
    """
    min_price = DataGenerator.generate_movie_min_price()
    max_price = DataGenerator.generate_movie_max_price()
    return (min_price, max_price)

@pytest.fixture(scope="function")
def test_movie():
    """
    Генератор данных для создания фильма
    """
    random_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_image_url()
    random_price = DataGenerator.generate_movie_price()
    random_description = DataGenerator.generate_movie_description()
    random_location = DataGenerator.generate_movie_location()
    random_published = DataGenerator.generate_movie_published()
    random_genreId = DataGenerator.generate_movie_ganreid()

    return {
        "name": random_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genreId
    }

@pytest.fixture(scope="function")
def created_movie(test_movie, api_manager, creds_super_admin):
    """
    :param test_movie: Тестовые данные фильма
    :param api_manager: Объект класса ApiManager
    """
    login = api_manager.auth_api.authenticate(creds_super_admin)
    response = api_manager.movies_api.create_movie(test_movie)
    response_data = response.json()
    created_movie = test_movie.copy()
    created_movie["id"] = response_data["id"]
    return created_movie

@pytest.fixture()
def check_movie_for_delete(api_manager):
    """
    Проверка на существование фильма для DELETE
    :param api_manager: Объект класса ApiManager
    """
    def check(movie_id):
        response = api_manager.movies_api.get_movie(movie_id, 404)
        return response.status_code == 404
    return check

@pytest.fixture(scope="function")
def test_movie_for_patch():
    """
    Генератор данных для изменения фильма
    """
    random_name = DataGenerator.generate_random_movie_name()
    random_description = DataGenerator.generate_movie_description()

    return {
        "name": random_name,
        "description": random_description,
    }

@pytest.fixture(scope="function")
def clean_movie(api_manager):
    def cleaner (id):
        api_manager.movies_api.delete_movie(id)
    return cleaner

"""=========================================== MOVIE API NEGATIVE =============================================="""

@pytest.fixture(scope="function")
def negative_data_for_filter():
    """
    NEGATIVE данные для фильтра
    """
    neg_min_price = DataGenerator.generate_negative_movie_min_price()
    neg_max_price = DataGenerator.generate_negative_movie_max_price()

    return (neg_min_price, neg_max_price)

@pytest.fixture(scope="function")
def negative_test_movie_without_four_param():
    """
    NEGATIVE Генерация данных без некоторых полей
    """
    random_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_image_url()
    random_price = DataGenerator.generate_movie_price()

    return {
        "name": random_name,
        "imageUrl": random_image_url,
        "price": random_price,
    }

@pytest.fixture(scope="function")
def negative_test_movie_with_wrong_type_data():
    """
    NEGATIVE Генерация данных с некорректным типом данных для полей
    """
    random_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_negative_random_word()
    random_price = DataGenerator.generate_negative_random_word()
    random_description = DataGenerator.generate_movie_description()
    random_location = DataGenerator.generate_negative_random_word()
    random_published = DataGenerator.generate_movie_published()
    random_genreid = DataGenerator.generate_movie_ganreid()

    return {
        "name": random_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genreid
    }

@pytest.fixture(scope="function")
def negative_test_movie_empty_json():
    """
    NEGATIVE Пустой джейсон
    """
    return {}

@pytest.fixture(scope="function")
def negative_id():
    """
    NEGATIVE неверный айди для get теста
    """
    random_id = DataGenerator.generate_negative_random_id()
    return random_id

@pytest.fixture(scope="function")
def login_and_auth(api_manager, creds_super_admin):
    api_manager.auth_api.authenticate(creds_super_admin)

"""============================================LOGIN DATA================================================


@pytest.fixture(scope="session")
def user_login_data (test_user):

    return {
        "email": test_user["email"],
        "password": test_user["password"]
    }


================================================NEGATIVE===================================================


@pytest.fixture(scope="session")
def negative_user_login_data_password(test_user):

    return {
        "email": test_user["email"],
        "password": 123
    }

@pytest.fixture(scope="session")
def negative_user_login_data_email(test_user):

    return {
        "email": test_user["email"] + 'KEK',
        "password": test_user["password"]
    }
@pytest.fixture(scope="session")
def negative_user_login_data_empty_body_request(test_user):

    return {}

"""

"""===================================== НЕАКТУАЛЬНО  ======================================"""


"""

@pytest.fixture(scope='session')
def requester():

    # Фикстура для создания кастомного реквестера

    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

"""