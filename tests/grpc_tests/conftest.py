import pytest
import grpc
from grpc import insecure_channel
from internal.pb.grpc.interceptors.logging import LoggingInterceptor
from internal.pb.grpc.interceptors.allure_interceptor import AllureInterceptor
from tests.config import WIREMOCK_HOST, CURRENCY_HOST
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]

def pytest_addoption(parser: pytest.Parser)->None:
    parser.addoption("--mock", action="store_true", default=False)


@pytest.fixture(scope="session")
def grpc_client(request: pytest.FixtureRequest) -> NifflerCurrencyServiceClient:
    channel = insecure_channel(CURRENCY_HOST)
    if request.config.getoption("--mock"):
        channel = insecure_channel(WIREMOCK_HOST)
    intercepted_channel = grpc.intercept_channel(channel, *INTERCEPTORS)
    return NifflerCurrencyServiceClient(intercepted_channel)
