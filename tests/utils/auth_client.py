import base64
import logging
import pkce
import allure
from tests.config import USERNAME, PASSWORD, AUTH_URL, AUTH_SECRET, BASE_URL
from tests.models.oauth import OAuthRequest
from tests.utils.sessions import AuthSession

username = USERNAME
password = PASSWORD
auth_url = AUTH_URL
auth_sercet = AUTH_SECRET
frontend_url = BASE_URL


def auth_with_token():
    try:
        print("СТАТУС РЕГИСТРАЦИИ")
        print(username)
        print(password)
        AuthClient().register(username, password)
    except Exception as e:
        print("НЕ УДАЛОСЬ ЗАРЕГИСТРИРОВАТЬСЯ")

    token = AuthClient().auth(username, password)
    allure.attach(token, name="token.txt", attachment_type=allure.attachment_type.TEXT)
    return token

class AuthClient:
    def __init__(self):
        self.session = AuthSession(base_url=auth_url)
        self.redirect_uri = frontend_url + "authorized"

        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()

        self._basic_token = base64.b64encode(auth_sercet.encode('utf-8')).decode('utf-8')
        self.authorization_basic = {"Authorization": f"Basic {self._basic_token}"}
        self.token = None

        

    def auth(self, username: str, password: str):
        # Шаг 1: Получаем страницу авторизации с параметрами и Basic Auth
            self.session.get(
                url="oauth2/authorize",
                params=OAuthRequest(
                    response_type="code",
                    client_id="client",
                    redirect_uri=self.redirect_uri,
                    scope="openid",
                    code_challenge=self.code_challenge,
                    code_challenge_method="S256"
                ).model_dump(),
                headers=self.authorization_basic,
                allow_redirects=True
            )

            # Извлекаем CSRF токен из cookies для формы логина
            csrf_token = self.session.cookies.get("XSRF-TOKEN")
            if not csrf_token:
                raise RuntimeError("CSRF token not found in cookies")

            # Шаг 2: Логинимся, передавая username, password и csrf
            result = self.session.post(
                url="login",
                data={
                    "username": username,
                    "password": password,
                    "_csrf": csrf_token,
                    "redirect_uri": self.redirect_uri,
                },
                allow_redirects=True
            )

            # После логина сервер должен перенаправить с кодом авторизации
            # Предполагаем, что code доступен в self.session.code (или нужно его вытянуть из URL)

            if not hasattr(self.session, 'code') or not self.session.code:
                # Если код не сохранен, пробуем извлечь из последнего URL редиректа
                last_url = result.url
                from urllib.parse import urlparse, parse_qs
                parsed_url = urlparse(last_url)
                query_params = parse_qs(parsed_url.query)
                code_list = query_params.get("code")
                if not code_list:
                    raise RuntimeError("Authorization code not found after login")
                self.session.code = code_list[0]

            # Шаг 3: Запрашиваем access token по полученному authorization code
            token_response = self.session.post(
                url="oauth2/token",
                #headers=self.authorization_basic,
                data={
                    "code": self.session.code,
                    "redirect_uri": self.redirect_uri,
                    "code_verifier": self.code_verifier,
                    "grant_type": "authorization_code",
                    "client_id": "client",
                },
            )

            # Проверяем, что получили JSON с токеном
            if token_response.headers.get("Content-Type", "").startswith("application/json"):
                self.token = token_response.json().get("access_token")
                if not self.token:
                    logging.error("Access token not found in response")
                    logging.error(token_response.text)
                    raise RuntimeError("Access token missing")
            else:
                logging.error("Non-JSON response from /oauth2/token")
                logging.error(f"Status code: {token_response.status_code}")
                logging.error(f"Response body:\n{token_response.text}")
                raise RuntimeError("OAuth token response was not JSON")

            return self.token
    
    def register(self, username, password):
        self.session.get(
            url="register",
            params={
                "redirect_uri": "http://auth.niffler.dc:9000/register",
            },
            allow_redirects=True
        )


        result = self.session.post(
            url=f"register",
            data={
                "username": username,
                "password": password,
                "passwordSubmit": password,
                "_csrf": self.session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )
        return result