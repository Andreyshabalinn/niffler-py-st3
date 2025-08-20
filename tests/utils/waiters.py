import datetime
import logging
import time

import allure


@allure.step
def wait_until_timeout(function):
    def wrapper(*args, **kwargs):
        default_timeout = 12
        timeout = kwargs.pop("timeout", default_timeout)
        polling_interval = kwargs.pop("polling_interval", 0.1)
        err = kwargs.pop("err", None)
        start_time = datetime.datetime.now().timestamp()
        result = None
        logging.debug(f'{start_time} start waiting')
        while datetime.datetime.now().timestamp() < start_time + timeout + 0.1:
            result = function(*args, **kwargs)
            if result is not None and result != [] and result != '':
                break
            time.sleep(polling_interval)
        if err and result is None:
            raise TimeoutError(
                f"{datetime.datetime.now().isoformat()} "
                f"Результаты функции {function.__name__} не найдены за {timeout}s"
            )
        if result is None:
            logging.error(f"{datetime.datetime.now().timestamp()} result is None")
        return result

    return wrapper