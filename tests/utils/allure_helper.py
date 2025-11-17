import json
import logging
from json import JSONDecodeError

import allure
import curlify
from allure_commons.types import AttachmentType
from requests import Response
from playwright.sync_api import Page

def allure_logger(config):
    listener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger

def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент и в консоль."""
    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]
        with allure.step(f"{method} {url}"):

            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            logging.debug(curl)
            logging.debug(response.text)

            allure.attach(
                body=curl.encode("utf8"),
                name=f"Request {response.status_code}",
                attachment_type=AttachmentType.TEXT,
                extension=".txt"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )
            except JSONDecodeError:
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt")
            allure.attach(
                body=json.dumps(dict(response.headers), indent=4).encode("utf8"),
                name=f"Response headers {response.status_code}",
                attachment_type=AttachmentType.JSON,
                extension=".json"
            )
        return response

    return wrapper


def attach_sql(conn, cursor, statement, parameters, context, executemany):
    try:
        if parameters:
            if isinstance(parameters, dict):
                param_str = str(parameters)
            else:
                param_str = ", ".join(map(str, parameters))
            sql_full = f"{statement} -- params: {param_str}"
        else:
            sql_full = statement
    except Exception as e:
        sql_full = f"Ошибка формирования SQL: {e}"

    try:
        db_name = context.connection.engine.url.database
    except Exception:
        db_name = "unknown"

    name = f"{statement.split()[0]} {db_name}"
    allure.attach(sql_full, name=name, attachment_type=AttachmentType.TEXT)

_original_goto = Page.goto

def goto_with_allure(self, url, *args, **kwargs):
    with allure.step(f"Переходим по URL: {url}"):
        return _original_goto(self, url, *args, **kwargs)