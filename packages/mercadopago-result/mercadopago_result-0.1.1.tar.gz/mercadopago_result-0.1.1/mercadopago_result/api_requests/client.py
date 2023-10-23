from dataclasses import dataclass
from enum import Enum
from result import Err
from result import Ok
from result import Result
from typing import List
from typing import Union
from typing import Optional

from mercadopago_result.api_requests.common import GetRequestError
from mercadopago_result.api_requests.common import HeaderFromAccessTokenError
from mercadopago_result.api_requests.common import HttpRequestError
from mercadopago_result.api_requests.common import JsonHeader
from mercadopago_result.api_requests.common import send_get_request
from mercadopago_result.api_requests.common import send_post_json_request
from mercadopago_result.api_requests.common import send_put_request
from mercadopago_result.authorization import AccessToken
from mercadopago_result.client import Client

""" Handles all the API endpoints for the Client
API official documentation:
https://www.mercadopago.com.br/developers/en/reference/customers/_customers/post
"""


class ClientCreationHeader(JsonHeader):
    pass


CLIENT_ENDPOINT_URL = "https://api.mercadopago.com/v1/customers"
CLIENT_SEARCH_URL = "https://api.mercadopago.com/v1/customers/search"
CLIENT_PUT_URL = "https://api.mercadopago.com/v1/customers/{id}"


class ClientCreationRequestErrorType(Enum):
    CREDENTIALS_REQUIRED = 100
    COSTUMER_ALREADY_EXISTS = 101
    MISSING_COSTUMER_ID = 102
    PARAMETER_NOT_OBJECT = 103
    PARAMETER_LENGTH_TOO_LONG = 104
    INVALID_COSTUMER = 105
    INVALID_EMAIL = 106  # appears twice, check error message
    INVALID_FIRST_NAME = 107
    INVALID_LAST_NAME = 108
    INVALID_PHONE_AREA_CODE = 109
    INVALID_PHONE_NUMBER = 110
    INVALID_IDENTIFICATION_TYPE = 111
    INVALID_IDENTIFICATION_NUMBER = 112
    INVALID_ADDRESS_ZIP_CODE = 113
    INVALID_STREET_NAME = 114
    INVALID_REGISTER_DATE = 115
    INVALID_DESCRIPTION = 116
    INVALID_METADATA = 117
    BODY_MUST_BE_JSON = 118
    CARD_REQUIRED = 119
    CARD_NOT_FOUND = 120
    INVALID_CARD = 121
    INVALID_CARD_DATA = 122
    PAYMENT_METHOD_REQUIRED = 123
    ISSUER_ID_REQUIRED = 124
    INVALID_PARAMETERS = 125
    CANNOT_UPDATE_EMAIL = 126
    CANNOT_RESOLVE_PAYMENT_METHOD = 127
    INVALID_EMAIL_FORMAT = 128  # appears twice, check error message
    MAXIMUM_CARD_LIMIT = 129
    INVALID_CARD_OWNER = 140
    INVALID_USER_INVOLVED = 150
    INVALID_DATE_RANGE_FORMAT = 200
    RANGE_MUST_BELONG_TO_DATE = 201
    INVALID_PARAMETER_AFTER = 202
    INVALID_PARAMETER_BEFORE = 203
    INVALID_FILTER_FORMAT = 204
    INVALID_QUERY_FORMAT = 205
    ATTRIBUTE_SORT = 206
    FILTER_ORDER = 207
    INVALID_SORT_PARAMETER = 208


@dataclass(frozen=True)
class ClientCreateError:
    class AccessToken(HeaderFromAccessTokenError):
        pass

    class HttpRequest(HttpRequestError):
        pass


@dataclass(frozen=True)
class ClientListError:
    class AccessToken(HeaderFromAccessTokenError):
        pass

    class GetRequest(GetRequestError):
        pass


@dataclass(frozen=True)
class ClientGetError:
    class MissingId:
        pass

    @dataclass(frozen=True)
    class NotFound:
        filter_parameter: Client

    @dataclass(frozen=True)
    class MultipleResults:
        filter_parameter: Client
        results: List[Client]

    class AccessToken(HeaderFromAccessTokenError):
        pass

    class GetRequest(GetRequestError):
        pass


@dataclass(frozen=True)
class ClientPutError:
    class AccessToken(HeaderFromAccessTokenError):
        pass

    class HttpRequest(HttpRequestError):
        pass


ClientCreateRequestError = Union[
    ClientCreateError,
    ClientCreateError.AccessToken,
    ClientCreateError.AccessToken.MissingPrivateKey,
    ClientCreateError.HttpRequest,
]
ClientCreationRequestResult = Result[Client, ClientCreateRequestError]
ClientListRequestError = Union[
    ClientListError,
    ClientListError.GetRequest,
    ClientListError.GetRequest.HttpRequest,
    ClientListError.GetRequest.UnexpectedJsonFormat,
    ClientListError.AccessToken,
    ClientListError.AccessToken.MissingPrivateKey,
]
ClientGetListRequestResult = Result[List[Client],
                                    ClientListRequestError]
ClientGetRequestError = Union[
    ClientGetError,
    ClientGetError.GetRequest,
    ClientGetError.GetRequest.HttpRequest,
    ClientGetError.GetRequest.UnexpectedJsonFormat,
    ClientGetError.MultipleResults,
    ClientGetError.NotFound,
    ClientGetError.MissingId,
    ClientGetError.AccessToken,
    ClientGetError.AccessToken.MissingPrivateKey,
]
ClientGetRequestResult = Result[List[Client],
                                ClientGetRequestError]
ClientPutRequestError = Union[
    ClientPutError,
    ClientPutError.AccessToken,
    ClientPutError.AccessToken.MissingPrivateKey,
    ClientPutError.HttpRequest,
]
ClientPutRequestResult = Result[List[Client],
                                ClientPutRequestError]


def send_client_creation_request(
        client: Client,
        access_token: AccessToken) -> ClientCreationRequestResult:
    headers: Optional[ClientCreationHeader] = None
    match ClientCreationHeader.from_access_token(access_token):
        case Ok(headers):
            pass  # can send the request
        case Err(ClientCreateError.AccessToken.MissingPrivateKey(
        )):
            return Err(
                ClientCreateError.AccessToken.MissingPrivateKey())
    match send_post_json_request(CLIENT_ENDPOINT_URL,
                                 client,
                                 headers,
                                 Client):
        case Ok(response_client):
            return Ok(response_client)
        case Err(problem):
            # convert to a client error
            return Err(ClientCreateError.HttpRequest(
                problem.code, problem.name, problem.message))


def send_client_get_list_request(
        client_filter: Client,
        access_token: AccessToken) -> ClientGetListRequestResult:
    headers: Optional[ClientCreationHeader] = None
    match ClientCreationHeader.from_access_token(access_token):
        case Ok(headers):
            pass
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(
                ClientListError.AccessToken.MissingPrivateKey())
    match send_get_request(CLIENT_SEARCH_URL, client_filter, headers, Client):
        case Ok(client_list):
            return Ok(client_list)
        case Err(GetRequestError.HttpRequest(code, name, message)):
            return Err(ClientListError.GetRequest.HttpRequest(
                code, name, message))
        case Err(GetRequestError.UnexpectedJsonFormat(endpoint, json_obj)):
            return Err(
                ClientListError.GetRequest.UnexpectedJsonFormat(
                    endpoint, json_obj))


def send_client_get_request(
        client_filter: Client,
        access_token: AccessToken) -> ClientGetRequestResult:
    client_list: Optional[list[Client]] = None
    match send_client_get_list_request(client_filter, access_token):
        case Ok(client_list):
            pass
        case Err(ClientListError.GetRequest.HttpRequest(code,
                                                        name,
                                                        msg)):
            return Err(ClientGetError.GetRequest.HttpRequest(code,
                                                             name,
                                                             msg))
        case Err(ClientListError.GetRequest.UnexpectedJsonFormat(
                endpoint, json_obj)):
            return Err(
                ClientGetError.GetRequest.UnexpectedJsonFormat(
                    endpoint, json_obj))
    if not client_filter.id:
        return Err(ClientGetError.MissingId())
    match client_list:
        case []:
            return Err(ClientGetError.NotFound(client_filter))
        case [single_result]:
            return Ok(single_result)
        case _:
            return Err(ClientGetError.MultipleResults(
                client_filter, client_list))


def send_client_put_request(
        client_updated: Client,
        access_token: AccessToken) -> ClientPutRequestResult:
    headers: Optional[ClientCreationHeader] = None
    match ClientCreationHeader.from_access_token(access_token):
        case Ok(headers):
            pass
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(
                ClientPutError.AccessToken.MissingPrivateKey())
    put_url = CLIENT_PUT_URL.format(id=client_updated.id)
    match send_put_request(put_url, client_updated, headers, Client):
        case Ok(client):
            return Ok(client)
        case Err(problem):
            return Err(ClientPutError.HttpRequest(
                problem.code, problem.name, problem.message))
