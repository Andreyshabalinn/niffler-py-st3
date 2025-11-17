from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from tests.grpc_tests.internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues
import grpc
import pytest
#
#   Эти тесты запускаем только с параметром --mock
#


@pytest.mark.parametrize("spend, spendCurrency, desiredCurrency, expected_result", [
    (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
    (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
    (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0),
]
)
def test_currency_conversion(
    grpc_client: NifflerCurrencyServiceClient,
    spend: float,
    spendCurrency: CurrencyValues,
    desiredCurrency: CurrencyValues,
    expected_result: float,
):
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spendCurrency,
            desiredCurrency=desiredCurrency,
            amount=spend
        )
    )
    assert response.calculatedAmount == expected_result, f"Expected {expected_result}"




def test_missing_desired_currency_returns_error(grpc_client: NifflerCurrencyServiceClient):
    """Тест на отсутствие desiredCurrency"""
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.USD,
                amount=100.0,
            )
        )
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND


def test_missing_spend_currency_returns_error(grpc_client: NifflerCurrencyServiceClient):
    """Тест на отсутствие spendCurrency"""
    with pytest.raises(grpc.RpcError) as exc_info:
        request = CalculateRequest(
            desiredCurrency=CurrencyValues.RUB,
            amount=100.0
        )
        grpc_client.calculate_rate(request=request)

    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND


def test_missing_amount_returns_error(grpc_client: NifflerCurrencyServiceClient):
    """Тест на отсутствие amount"""
    with pytest.raises(grpc.RpcError) as exc_info:
        request = CalculateRequest(
            spendCurrency=CurrencyValues.USD,
            desiredCurrency=CurrencyValues.RUB,
        )
        grpc_client.calculate_rate(request=request)

    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND


def test_empty_request(grpc_client: NifflerCurrencyServiceClient):
    """Тест на пустой запрос"""
    with pytest.raises(grpc.RpcError) as exc_info:
        request = CalculateRequest()
        grpc_client.calculate_rate(request=request)
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND
