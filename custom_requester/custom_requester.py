import json
import logging
import os

class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "SUKA": "BLYAD"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(self, method, endpoint, data=None, expected_status=200, need_logging=True):
        """
        :param method: HTTP метод (напр., POST, PUT)
        :param endpoint: Эндпоинт (напр, /login)
        :param data: Тело запроса (JSON данные)
        :param expected_status: Ожидаемый статус-код (напр., 200)
        :param need_logging: Ожидается ли логирование запроса/ответа
        :return: Объект ответа requests.Response
        """
        url = f"{self.base_url}{endpoint}"

        # print(f"🔍 DEBUG send_request:")
        # print(f"   self.headers = {self.headers}")
        # print(f"   session.headers = {dict(self.session.headers)}")

        response = self.session.request(method, url, json=data, headers=self.headers)
        if need_logging:
            self.log_request_and_response(response)
        if response.status_code != expected_status:
            raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")
        return response


    def _update_session_headers(self, session, **kwargs):
        """
        :param session: Объект requests.Session, предоставленный API классом
        :param kwargs: Хедеры, которые мы получаем и ими обновляем
        """
        self.headers.update(kwargs) #Обновляем базовые заголовки
        session.headers.update(self.headers) #Обновляем заголовки в текущей сессии

    def log_request_and_response(self, response):
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response.status_code}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response.status_code}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")
