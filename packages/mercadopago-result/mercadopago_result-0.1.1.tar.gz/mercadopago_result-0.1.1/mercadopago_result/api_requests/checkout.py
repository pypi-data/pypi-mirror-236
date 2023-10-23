from dataclasses import dataclass
from enum import Enum
from result import Err
from result import Ok
from result import Result
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
from mercadopago_result.checkout import Checkout
from mercadopago_result.checkout import CheckoutShorten


class CheckoutHeader(JsonHeader):
    pass


CHECKOUT_CREATE_URL = "https://api.mercadopago.com/checkout/preferences"
CHECKOUT_LIST_URL = "https://api.mercadopago.com/checkout/preferences/search"
CHECKOUT_GET_URL = "https://api.mercadopago.com/checkout/preferences/{id}"
CHECKOUT_PUT_URL = "https://api.mercadopago.com/checkout/preferences/{id}"


class CheckoutRequestErrorType(str, Enum):
    INVALID_COLLECTOR_ID = "invalid_collector_id"
    INVALID_SPONSOR_ID = "invalid_sponsor_id"
    INVALID_COLLECTOR_EMAIL = "invalid_collector_email"
    INVALID_OPERATION_TYPE = "invalid_operation_type"
    INVALID_EXPIRATION_DATE_TO = "invalid_expiration_date_to"
    INVALID_EXPIRATION_DATE_FROM = "invalid_expiration_date_from"
    INVALID_ITEMS = "invalid_items"
    INVALID_BACK_URLS = "invalid_back_urls"
    INVALID_PAYMENT_METHODS = "invalid_payment_methods"
    INVALID_INSTALLMENTS = "invalid_installments"
    INVALID_MARKETPLACE_FEE = "invalid_marketplace_fee"
    INVALID_ID = "invalid_id"
    INVALID_ACCESS_TOKEN = "invalid_access_token"
    INVALID_SHIPMENTS = "invalid_shipments"
    INVALID_BINARY_MODE = "invalid_binary_mode"


@dataclass(frozen=True)
class CheckoutCreateError:
    class AccessToken(HeaderFromAccessTokenError):
        pass

    class HttpRequest(HttpRequestError):
        pass


@dataclass(frozen=True)
class CheckoutGetListError:
    class AccessToken(HeaderFromAccessTokenError):
        pass

    class GetRequest(GetRequestError):
        pass


@dataclass(frozen=True)
class CheckoutGetError:
    class MissingId:
        pass

    class AccessToken(HeaderFromAccessTokenError):
        pass

    class GetRequest(GetRequestError):
        pass


@dataclass(frozen=True)
class CheckoutPutError:
    class MissingId:
        pass

    class AccessToken(HeaderFromAccessTokenError):
        pass

    class PutRequest(HttpRequestError):
        pass


CheckoutCreateErrors = Union[
    CheckoutCreateError,
    CheckoutCreateError.AccessToken,
    CheckoutCreateError.AccessToken.MissingPrivateKey,
    CheckoutCreateError.HttpRequest,
]
CheckoutCreateResult = Result[Checkout, CheckoutCreateErrors]
CheckoutGetListErrors = Union[
    CheckoutGetListError,
    CheckoutGetListError.GetRequest,
    CheckoutGetListError.GetRequest.HttpRequest,
    CheckoutGetListError.GetRequest.UnexpectedJsonFormat,
    CheckoutGetListError.AccessToken,
    CheckoutGetListError.AccessToken.MissingPrivateKey,
]
CheckoutGetListResult = Result[CheckoutShorten, CheckoutGetListErrors]
CheckoutGetErrors = Union[
    CheckoutGetError,
    CheckoutGetError.GetRequest,
    CheckoutGetError.GetRequest.HttpRequest,
    CheckoutGetError.GetRequest.UnexpectedJsonFormat,
    CheckoutGetError.MissingId,
    CheckoutGetError.AccessToken,
    CheckoutGetError.AccessToken.MissingPrivateKey,
]
CHECKOUT_GET_RESULT = Result[Checkout, CheckoutGetErrors]
CheckoutPutErrors = Union[
    CheckoutPutError,
    CheckoutPutError.PutRequest,
    CheckoutPutError.AccessToken,
    CheckoutPutError.AccessToken.MissingPrivateKey,
    CheckoutPutError.MissingId,
]
CheckoutPutResult = Result[Checkout, CheckoutPutErrors]


def send_checkout_create_request(
        checkout: Checkout,
        access_token: AccessToken) -> CheckoutCreateResult:
    headers: Optional[CheckoutHeader] = None
    # convert access_token to header
    match CheckoutHeader.from_access_token(access_token):
        case Ok(headers):
            pass  # can send the request
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(
                CheckoutCreateError.AccessToken.MissingPrivateKey())
    # send request and return the result
    match send_post_json_request(CHECKOUT_CREATE_URL,
                                 checkout,
                                 headers,
                                 Checkout):
        case Ok(response_checkout):
            return Ok(response_checkout)
        case Err(problem):
            # let the code above decide what to do
            return Err(CheckoutCreateError.HttpRequest(
                problem.code, problem.name, problem.message))


def send_checkout_get_list_request(
        checkout_filter: Checkout,
        access_token: AccessToken) -> CheckoutGetListResult:
    headers: Optional[CheckoutHeader] = None
    match CheckoutHeader.from_access_token(access_token):
        case Ok(headers):
            pass
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(
                CheckoutGetListError.AccessToken.MissingPrivateKey())
    match send_get_request(CHECKOUT_LIST_URL,
                           checkout_filter,
                           headers,
                           CheckoutShorten):
        case Ok(checkout_list):
            return Ok(checkout_list)
        case Err(GetRequestError.HttpRequest(code, name, message)):
            return Err(CheckoutGetListError.GetRequest.HttpRequest(
                code,
                name,
                message))
        case Err(GetRequestError.UnexpectedJsonFormat(endpoint, json_obj)):
            return Err(
                CheckoutGetListError.GetRequest.UnexpectedJsonFormat(
                    endpoint, json_obj))


def send_checkout_get_request(
        checkout_filter: Checkout,
        access_token: AccessToken) -> CHECKOUT_GET_RESULT:
    headers: Optional[CheckoutHeader] = None
    match CheckoutHeader.from_access_token(access_token):
        case Ok(headers):
            pass
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(
                CheckoutGetError.AccessToken.MissingPrivateKey())
    if not checkout_filter.id:
        return Err(CheckoutGetError.MissingId())
    checkout_url = CHECKOUT_GET_URL.format(id=checkout_filter.id)
    match send_get_request(checkout_url,
                           checkout_filter,
                           headers,
                           Checkout):
        case Ok(checkout):
            return Ok(checkout)
        case Err(GetRequestError.HttpRequest(code, name, message)):
            return Err(CheckoutGetError.GetRequest.HttpRequest(
                code,
                name,
                message))
        case Err(GetRequestError.UnexpectedJsonFormat(endpoint, json_obj)):
            return Err(
                CheckoutGetError.GetRequest.UnexpectedJsonFormat(
                    endpoint, json_obj))


def send_checkout_put_request(
        checkout_updated: Checkout,
        access_token: AccessToken) -> CheckoutPutResult:
    headers: Optional[CheckoutHeader] = None
    match CheckoutHeader.from_access_token(access_token):
        case Ok(headers):
            pass
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(CheckoutPutError.AccessToken.MissingPrivateKey())
    if not checkout_updated.id:
        return Err(CheckoutPutError.MissingId())
    put_url = CHECKOUT_PUT_URL.format(id=checkout_updated.id)
    match send_put_request(put_url,
                           checkout_updated,
                           headers,
                           Checkout):
        case Ok(checkout):
            return Ok(checkout)
        case Err(HttpRequestError(code, name, message)):
            return Err(CheckoutPutError.PutRequest(code, name, message))
