import json

from dataclasses import dataclass
from result import Err
from result import Ok
from result import Result
from typing import Optional
from typing import Union


@dataclass(frozen=True)
class AccessTokenError:
    @dataclass(frozen=True)
    class LoadingFile:
        @dataclass(frozen=True)
        class FileDoesNotExist:
            path: str

    @dataclass(frozen=True)
    class Parsing:
        message: str


AccessTokenLoadErrors = Union[
    AccessTokenError,
    AccessTokenError.LoadingFile,
    AccessTokenError.LoadingFile.FileDoesNotExist,
    AccessTokenError.Parsing,
]
AccessTokenLoadFileResult = Result["AccessToken", AccessTokenLoadErrors]
AccessTokenLoadResult = Result["AccessToken", AccessTokenLoadErrors]


@dataclass(frozen=True)
class AccessToken:
    private: Optional[str] = None
    public: Optional[str] = None

    @classmethod
    def load_from_json_file(cls,
                            json_path: str) -> AccessTokenLoadFileResult:
        try:
            with open(json_path, "r") as json_file:
                json_object = json.loads(json_file.read())
            match AccessToken.load_from_json(json_object):
                case Ok(access_token):
                    return Ok(access_token)
                case Err(err):
                    return Err(err)
        except FileNotFoundError:
            return Err(AccessTokenError.LoadingFile.FileDoesNotExist(
                json_path))

    @classmethod
    def load_from_json(cls, json_object: dict) -> AccessTokenLoadResult:
        try:
            return Ok(cls(**json_object))
        except (TypeError, json.decoder.JSONDecodeError) as e:
            return Err(AccessTokenError.Parsing(str(e)))
