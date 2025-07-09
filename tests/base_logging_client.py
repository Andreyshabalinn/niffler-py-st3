import logging
import time
import requests

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url
        self.headers = {
            "Accept": "*/*"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _log_request(self, method, url, **kwargs):
        logger.info(f"REQUEST: {method} {url}")
        logger.debug(f"Headers: {kwargs.get('headers')}")
        logger.debug(f"Params: {kwargs.get('params')}")
        logger.debug(f"Data: {kwargs.get('data')}")
        logger.debug(f"JSON: {kwargs.get('json')}")

    def _log_response(self, response: requests.Response):
        logger.info(f"RESPONSE: {response.status_code} {response.url}")
        logger.debug(f"Response body: {response.text}")

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("headers", self.headers)

        self._log_request(method, url, **kwargs)

        response = requests.request(method, url, **kwargs)

        self._log_response(response)

        return response
