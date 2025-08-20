import base64
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
    AuthClient().register(username, password)
    token = AuthClient().auth(username, password)
    allure.attach(token, name="token.txt", attachment_type=allure.attachment_type.TEXT)
    return token

class AuthClient:
    def __init__(self):
        self.session = AuthSession(base_url=auth_url)

        # Переписать с использованием библиотеки
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()

        self._basic_token = base64.b64encode(auth_sercet.encode('utf-8')).decode('utf-8')
        self.authorization_basic = {"Authorization": f"Basic {self._basic_token}"}
        self.token = None

    def auth(self, username, password):
        self.session.get(
                    url="/oauth2/authorize",
                    params=OAuthRequest(
                        redirect_uri=f"{frontend_url}authorized",
                        code=self.session.code,
                        code_challenge=self.code_challenge
                    ).model_dump(),
                    allow_redirects=True
                )

        self.session.post(
            url="login",
            data={
                "username": username,
                "password": password,
                "_csrf": self.session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )

        token_response = self.session.post(
            url="oauth2/token",
            data={
                "code": self.session.code,
                "redirect_uri": f"{frontend_url}authorized",
                "code_verifier": self.code_verifier,
                "grant_type": "authorization_code",
                "client_id": "client"
            },
        )

        self.token = token_response.json().get("access_token", None)
        return self.token
    
    def register(self, username, password):
        self.session.get(
            url=f"{auth_url}/register",
            params={
                "redirect_uri": "http://auth.niffler.dc:9000/register",
            },
            allow_redirects=True
        )

        result = self.session.post(
            url=f"{auth_url}/register",
            data={
                "username": username,
                "password": password,
                "passwordSubmit": password,
                "_csrf": self.session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )
        return result