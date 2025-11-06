from typing import Callable
from google.protobuf.message import Message
import grpc


class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):

    def intercept_unary_unary(self, continuation: Callable, client_call_details: grpc.ClientCallDetails, request: Message) -> Callable:
        print(client_call_details.method)
        print(request)
        response = continuation(client_call_details, request)
        print(response.result())
        return response
