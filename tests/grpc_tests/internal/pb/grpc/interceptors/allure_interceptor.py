from typing import Callable
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson
import grpc
import allure


class AllureInterceptor(grpc.UnaryUnaryClientInterceptor):

    def intercept_unary_unary(self, continuation: Callable, client_call_details: grpc.ClientCallDetails, request: Message) -> Callable:
        with allure.step(client_call_details.method):
            allure.attach(MessageToJson(request), "request",
                          attachment_type=allure.attachment_type.JSON)
            response = continuation(client_call_details, request)
            allure.attach(MessageToJson(response.result()), "response",
                          attachment_type=allure.attachment_type.JSON)
            return response
