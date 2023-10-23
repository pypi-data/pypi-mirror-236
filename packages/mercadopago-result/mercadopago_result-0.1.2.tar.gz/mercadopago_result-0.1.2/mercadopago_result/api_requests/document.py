from dataclasses import dataclass
from typing import Union
from typing import Optional
from result import Result
from result import Ok
from result import Err

from mercadopago_result.document import Document
from mercadopago_result.authorization import AccessToken
from mercadopago_result.api_requests.common import JsonHeader
from mercadopago_result.api_requests.common import HeaderFromAccessTokenError
from mercadopago_result.api_requests.common import send_get_request
from mercadopago_result.api_requests.common import GetRequestError


class DocumentRequestHeader(JsonHeader):
    pass


DOCUMENT_GET_URL = "https://api.mercadopago.com/v1/identification_types"


@dataclass(frozen=True)
class DocumentGetRequestError:
    class AccessToken(HeaderFromAccessTokenError):
        pass

    class GetRequest(GetRequestError):
        pass


DocumentGetRequestErrors = Union[
    DocumentGetRequestError,
    DocumentGetRequestError.AccessToken,
    DocumentGetRequestError.AccessToken.MissingPrivateKey,
    DocumentGetRequestError.GetRequest,
    DocumentGetRequestError.GetRequest.HttpRequest,
    DocumentGetRequestError.GetRequest.UnexpectedJsonFormat,
]
DocumentGetRequestResult = Result[Document, DocumentGetRequestErrors]


def send_document_get_request(
        access_token: AccessToken) -> DocumentGetRequestResult:
    headers: Optional[DocumentRequestHeader] = None
    match DocumentRequestHeader.from_access_token(access_token):
        case Ok(headers):
            pass
        case Err(HeaderFromAccessTokenError.MissingPrivateKey()):
            return Err(DocumentGetRequestError.AccessToken.MissingPrivateKey())
    match send_get_request(DOCUMENT_GET_URL, Document(), headers, Document):
        case Ok(document):
            return Ok(document)
        case Err(GetRequestError.HttpRequest(code, name, message)):
            return Err(DocumentGetRequestError.GetRequest.HttpRequest(
                code, name, message))
        case Err(GetRequestError.UnexpectedJsonFormat(endpoint, json_object)):
            return Err(DocumentGetRequestError.GetRequest.UnexpectedJsonFormat(
                endpoint, json_object))
