import logging
import requests

from tests.utils.sessions import BaseSession

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, base_url: str, token: str = None):
        self.session = BaseSession(base_url=base_url)
        self.base_url = base_url

        self.headers = {"Accept": "*/*"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(self.headers)

    def _mask(self, headers: dict) -> dict:
        h = headers.copy()
        if "Authorization" in h:
            h["Authorization"] = "***"
        return h

    def _log_request(self, method, url, **kwargs):
        masked_headers = self._mask(kwargs.get("headers", {}))
        logger.info(f"REQUEST: {method} {url}")
        logger.debug(f"Headers: {masked_headers}")
        logger.debug(f"Params: {kwargs.get('params')}")
        logger.debug(f"Data: {kwargs.get('data')}")
        logger.debug(f"JSON: {kwargs.get('json')}")

    def _log_response(self, response: requests.Response):
        logger.info(f"RESPONSE: {response.status_code} {response.url}")
        logger.debug(f"Response body: {response.text}")

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        self._log_request(method, self.base_url + path, **kwargs)

        response = self.session.request(method, path, **kwargs)

        self._log_response(response)
        return response
