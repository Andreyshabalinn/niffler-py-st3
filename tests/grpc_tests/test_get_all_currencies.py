from tests.grpc_tests.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from google.protobuf import empty_pb2

def test_get_all_currencies(grpc_client: NifflerCurrencyServiceClient)-> None:
    response = grpc_client.get_all_currencies(empty_pb2.Empty())
    assert len(response.allCurrencies) == 4