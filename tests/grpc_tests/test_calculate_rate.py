from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from tests.grpc_tests.internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues
import grpc
import pytest


def test_calculate_rate(grpc_client: NifflerCurrencyServiceClient) -> None:
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=CurrencyValues.EUR,
            desiredCurrency=CurrencyValues.RUB,
            amount=100.0
        )
    )
    assert response.calculatedAmount == 7200, "Expected 7200"


def test_calculate_rate_without_desired_currency(grpc_client: NifflerCurrencyServiceClient) -> None:
    try:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                amount=100.0
            )
        )
    except grpc.RpcError as e:
        assert e.code() == grpc.StatusCode.UNKNOWN
        assert e.details() == "Application error processing RPC"
