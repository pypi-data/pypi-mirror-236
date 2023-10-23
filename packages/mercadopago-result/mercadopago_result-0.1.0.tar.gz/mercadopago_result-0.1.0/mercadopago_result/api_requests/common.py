import httpx

from dataclasses import dataclass
from pydantic import BaseModel
from result import Err
from result import Ok
from result import Result
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Type
from typing import Union

from mercadopago_result.authorization import AccessToken


AUTH_TOKEN = str
""" The application authorization token """


class HeaderFromAccessTokenError:
    @dataclass(frozen=True)
    class MissingPrivateKey:
        pass


HeaderFromAccessTokenErrors = Union[
    HeaderFromAccessTokenError.MissingPrivateKey,
]
HEADER_FROM_ACCESS_TOKEN_RESULT = Result[
    "CheckoutHeader",
    HeaderFromAccessTokenErrors]


class JsonHeader(BaseModel):
    authorization: AUTH_TOKEN
    content_type: Literal["application/json"] = "application/json"

    def as_header(self) -> dict[str, str]:
        """ Returns a dict with the keys "Content-Type" and "Authorization"
        this is meant to be used as the headers for the http request """
        return {
            'Content-Type': self.content_type,
            'Authorization': f'Bearer {self.authorization}'
        }

    @classmethod
    def from_access_token(
            cls, access_token: AccessToken) -> HEADER_FROM_ACCESS_TOKEN_RESULT:
        match access_token.private:
            case None:
                return Err(
                    HeaderFromAccessTokenError.MissingPrivateKey())
            case "":
                return Err(
                    HeaderFromAccessTokenError.MissingPrivateKey())
            case key:
                return Ok(cls(authorization=key))


@dataclass(frozen=True)
class HttpRequestError:
    """ Holds the http request error information """
    code: httpx.codes
    name: str
    message: str


POST_REQUEST_RESULT = Result[BaseModel, HttpRequestError]


def send_post_json_request(endpoint_url: str,
                           parameter_data: BaseModel,
                           header: JsonHeader,
                           model: Type[BaseModel]) -> POST_REQUEST_RESULT:
    """ Sends the request to the MercadoPago API endpoint and return a
    validated model object """
    response = httpx.post(endpoint_url,
                          json=parameter_data.model_dump(exclude_unset=True),
                          headers=header.as_header())
    response_json = response.json()
    match response.status_code:
        case httpx.codes.CREATED:
            return Ok(model(**response_json))
        case code:
            return Err(HttpRequestError(code,
                                        response_json.get("error", None),
                                        response_json.get("message", None)))


@dataclass(frozen=True)
class GetRequestError:
    @dataclass
    class UnexpectedJsonFormat:
        endpoint_url: str
        json_object: dict

    class HttpRequest(HttpRequestError):
        pass


ModelResponse = Union[BaseModel, List[BaseModel]]
GetRequestErrors = Union[
    GetRequestError,
    GetRequestError.HttpRequest,
    GetRequestError.UnexpectedJsonFormat,
]
GetRequestResult = Result[ModelResponse, GetRequestErrors]
GET_REQUEST_EXPECTED_KEYS = {"results", "elements"}
''' These are the keys that are expected from a successful get request '''


def check_if_response_is_valid(json_response: Dict[str, Any],
                               model: Type[BaseModel]) -> bool:
    """ True - if there are no extra fields """
    model_fields = set(model.model_fields.keys())
    json_keys = set(json_response.keys())
    return not (json_keys - model_fields)


def send_get_request(endpoint_url: str,
                     parameter_data: BaseModel,
                     header: JsonHeader,
                     model: Type[BaseModel]) -> GetRequestResult:
    response = httpx.get(endpoint_url,
                         params=parameter_data.model_dump(exclude_unset=True),
                         headers=header.as_header())
    response_json = response.json()
    match response.status_code:
        case httpx.codes.OK:
            if not response_json:
                return Err(GetRequestError.UnexpectedJsonFormat(
                    endpoint_url, response_json))
            if check_if_response_is_valid(response_json, model):
                return Ok(model(**response_json))
            if not GET_REQUEST_EXPECTED_KEYS.intersection(
                    response_json.keys()):
                return Err(GetRequestError.UnexpectedJsonFormat(
                    endpoint_url, response_json))
            existing_key = GET_REQUEST_EXPECTED_KEYS.intersection(
                response_json.keys())
            existing_key = list(existing_key)[0]
            items = response_json.get(existing_key, [])
            return Ok([model(**r) for r in items])
        case code:
            return Err(GetRequestError.HttpRequest(
                code,
                response_json.get("error", None),
                response_json.get("message", None)))


PUT_REQUEST_RESULT = Result[BaseModel, HttpRequestError]


def send_put_request(endpoint_url: str,
                     update_data: BaseModel,
                     header: JsonHeader,
                     model: Type[BaseModel]) -> PUT_REQUEST_RESULT:
    response = httpx.put(endpoint_url,
                         json=update_data.model_dump(exclude_unset=True),
                         headers=header.as_header())
    response_json = response.json()
    match response.status_code:
        case httpx.codes.OK:
            return Ok(model(**response_json))
        case code:
            return Err(HttpRequestError(code,
                                        response_json.get("error", None),
                                        response_json.get("message", None)))
