"""Tool for signing/verifying json documents"""
import string
import json

from typing import Any, Dict, List, Tuple, Union, Optional, Final
from base64 import b64encode
from hashlib import blake2b
from json import JSONDecoder
from pydantic.json import pydantic_encoder


# Default signature generator
_SIGNATURE_DIGEST_LEN: Final[int] = 32

_SKIP_CHARS = string.whitespace + ":,"


def _skip_chars(s: str, idx: int = 0) -> int:       # pylint: disable=C0103
    """Skips all unimportant characters until the beginning of the next token"""
    while idx < len(s) and s[idx] in _SKIP_CHARS:
        idx += 1

    return idx


class TTDecoder(JSONDecoder):
    """JSONDecoder with built-in signature checking functionality."""

    def __init__(
            self,
            hash_dict: Dict[str, Any],
            hash_name: str,
            hash_list: List[str],
            *args, **kwargs):
        """Initialize decoder"""
        self.hash_dict = hash_dict
        self.hash_name = hash_name
        self.hash_list = hash_list

        super().__init__(*args, **kwargs)

    def raw_decode(self, s: str, idx: int) -> Any:  # pylint: disable=C0103,W0222
        assert s[0] == "{", "ASSERT c8e74621-b641-4480-a767-f626c52ee7ed"

        _start = _skip_chars(s, 1)

        _result: Dict[str, Any] = {}
        _tokens: Dict[str, str] = {}

        while _start < len(s):
            if s[_start] == '}':
                _start += 1
                break

            _key, _end = super().raw_decode(s, _start)
            _start = _skip_chars(s, _end + 1)
            _value, _end = super().raw_decode(s, _start)

            if _key in self.hash_list:
                _tokens[_key] = s[_start:_end]

            if _key == self.hash_name:
                self.hash_dict["hash_digest"] = _value
            else:
                _result[_key] = _value

            _start = _skip_chars(s, _end + 1)

        for _key in self.hash_list:
            self.hash_dict["hash_func"].update(_tokens.get(_key, '').encode("utf-8"))

        return _result, _start


class TTSignatureChecker:
    """Signature checker for TTDecoder"""

    def __init__(
            self,
            digest_length: int,
            hash_name: str,
            hash_list: List[str],
            hash_seed: bytes
    ):
        self.hash_dict = {
            "hash_func": blake2b(digest_size=digest_length, key=hash_seed),
            "hash_digest": None
        }

        self.hash_name = hash_name
        self.hash_list = hash_list

    def __call__(self, *args, **kwargs) -> JSONDecoder:
        """Creates new JSONDecoder with signature checker"""
        return TTDecoder(self.hash_dict, self.hash_name, self.hash_list, *args, **kwargs)

    def get_signatures(self) -> Tuple[Optional[str], Optional[str]]:
        """Returns actual and expected signatures of last loaded JSON str"""
        return b64encode(self.hash_dict["hash_func"].digest()).decode('utf-8'), self.hash_dict["hash_digest"]

    def is_signature_valid(self) -> bool:
        """Returns validation result of last performed JSON load operation"""
        _actual, _expected = self.get_signatures()

        return _actual == _expected


class TTSignedJson:
    """Generates and checks signed JSON strings"""
    _digest_length: int = _SIGNATURE_DIGEST_LEN

    def __init__(self, hash_name: str, hash_list: List[str], hash_seed: bytes) -> None:
        """Initialize the object"""
        self.hash_name = hash_name
        self.hash_list = hash_list
        self.hash_seed = hash_seed

        self._checker = None

        assert hash_name not in hash_list, "ASSERT f7c19f43-14b5-41ee-b583-7554f4108894: hash_name=[{}]".format(
            hash_name)

    def dumps(self, obj_dict: Dict[str, Any]) -> str:
        """Creates a signed JSON for the given object"""

        assert self.hash_name not in obj_dict, "ASSERT bcedf11e-cbde-4143-89b7-b05061d984f0"
        assert not (set(self.hash_list) - set(obj_dict.keys())),\
            "ASSERT 5bce26d4-3023-4285-91bb-06768f92af59: missing=[{}]".format(
                set(self.hash_list) - set(obj_dict.keys())
        )

        _tokens = {key: json.dumps(value, default=pydantic_encoder) for key, value in obj_dict.items()}
        _hash = blake2b(digest_size=self._digest_length, key=self.hash_seed)

        for _key in self.hash_list:
            _hash.update(_tokens.get(_key, '').encode("utf-8"))

        _tokens[self.hash_name] = json.dumps(b64encode(_hash.digest()).decode('utf-8'))

        return "{{{}}}".format(
            ", ".join(("{}: {}".format(json.dumps(key), value) for key, value in _tokens.items()))
        )

    def loads(self, obj_json: Union[str, bytes]) -> Dict[str, Any]:
        """Verifies signed JSON string and returns dict"""

        self._checker = TTSignatureChecker(
            self._digest_length, self.hash_name, self.hash_list, self.hash_seed
        )

        return json.loads(obj_json, cls=self._checker)

    def get_signatures(self) -> Tuple[Optional[str], Optional[str]]:
        """Returns actual and expected signatures of last loaded JSON str"""
        if not self._checker:
            return None, None

        return self._checker.get_signatures()

    def is_signature_valid(self) -> bool:
        """Returns validation result of last performed JSON load operation"""
        return self._checker is not None and self._checker.is_signature_valid()
