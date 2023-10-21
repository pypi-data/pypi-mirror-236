"""
response body dataclass.
"""
from typing import List
from typing import Optional

from dataclasses import dataclass


@dataclass
class LoginResponse:
    """
    the login method response
    """
    jsonrpc: str
    result: dict
    id: int
    status: bool
    origin: str
    host: dict


@dataclass
class Title:
    """
    response title representation
    """
    ru: str
    en: str
    uz: str


@dataclass
class AccountInfo:
    """
    response account info representation
    """
    name: str
    title: Title
    mask: str
    number: str


@dataclass
class Payment:
    """
    response payment representation
    """
    ref_num: str
    id: Optional[int]


@dataclass
class Epos:
    """
    response epos representation
    """
    merchant: str
    terminal: str


@dataclass
class MerchantType:
    """
    response merchant type representation
    """
    ru: str
    en: str
    uz: str


@dataclass
class Merchant:
    """
    response merchant representation
    """
    organization: str
    epos: Epos
    type: MerchantType


@dataclass
class Host:
    """
    response host representation
    """
    host: str
    timestamp: str


@dataclass
class Result:
    """
    response result representation
    """
    ext_id: str
    state: int
    number: str
    description: str
    amount: int
    currency: str
    commission: float
    account: List[AccountInfo]
    payment: Payment
    merchant: Merchant


@dataclass
class BaseResponse:
    """
    the parent dataclass for the response
    """
    jsonrpc: str
    result: Result
    id: str
    status: bool
    origin: str
    host: Host

    def to_dict(self):
        """
        for dict representation.
        """
        return {
            "jsonrpc": self.jsonrpc,
            "result": self.result,
            "id": self.id,
            "status": self.status,
            "origin": self.origin,
            "host": self.host
        }


@dataclass
class ResponseCreateCheck(BaseResponse):
    """
    response (transfer.credit.create) data representation
    """


@dataclass
class ResponseConfirmCheck(BaseResponse):
    """
    response (transfer.credit.confirm) data representation
    """


@dataclass
class ResponseCheckStatus(BaseResponse):
    """
    response (transfer.credit.confirm) data representation
    """


@dataclass
class ResponseAccount2Card(BaseResponse):
    """
    response account2card data representation.
    """
