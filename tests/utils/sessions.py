from requests import Session, HTTPError
from urllib.parse import urlparse, parse_qs
from tests.utils.allure_helper import allure_attach_request

def raise_for_status(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
        print(response)
        return response
    
    return wrapper

class BaseSession(Session):
    """Сессия с прокидыванием base_url и логированием."""

    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.pop("base_url", "")
        super().__init__(*args, **kwargs)

    @raise_for_status
    @allure_attach_request
    def request(self, method, url, **kwargs):
        if not url.startswith("http"):
            url = self.base_url + url
        return super().request(method, url, **kwargs)

class AuthSession(BaseSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = None

    @allure_attach_request
    def request(self, method, url, **kwargs):
        response = super().request(method, url, **kwargs)

        for r in response.history:
            self.cookies.update(r.cookies.get_dict())

            location = r.headers.get("Location")
            if location:
                query = urlparse(location).query
                code_list = parse_qs(query).get("code")
                if code_list:
                    self.code = code_list[0]

        return response