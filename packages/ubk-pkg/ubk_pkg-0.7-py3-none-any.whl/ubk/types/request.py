"""
request body dataclass.
"""
from uuid import uuid4
from dataclasses import dataclass


@dataclass
class RequestBody:
    """
    The request body.
    """
    method: str
    jsonrpc: str = "2.0"
    params: dict = None

    def to_dict(self):
        """
        returns a dict representation of dataclas
        """
        request_dict = {
            "jsonrpc": self.jsonrpc,
            "id": str(uuid4()),
            "method": self.method,
            "params": self.params
        }
        if self.params is not None:
            request_dict["params"] = self.params

        return request_dict


@dataclass
class RequestTransferCreditCreate:
    """
    TransferCreditCreate (create check) params represents.
    """
    number: str
    amount: int
    ext_id: str = str(uuid4())

    def to_dict(self):
        """
        returns a dict representation of dataclas
        """
        return {
            "ext_id": self.ext_id,
            "number": self.number,
            "amount": self.amount
        }


@dataclass
class RequestAccount2Card(RequestTransferCreditCreate):
    """
    Account2Card Processing includes (create check and pay check)
    """


@dataclass
class RequestTransferCreditConfirm:
    """
    TransferCreditConfirm (pay check) params represents.
    """
    ext_id: str

    def to_dict(self):
        """
        returns a dict representation of dataclas
        """
        return {
            "ext_id": self.ext_id
        }


@dataclass
class RequestTransferCreditCancel:
    """
    TransferCreditCancel params represents.
    """
    ext_id: str

    def to_dict(self):
        """
        returns a dict representation of dataclas
        """
        return {
            "ext_id": self.ext_id
        }


@dataclass
class RequestTransferCreditState:
    """
    TransferCreditState params represents.
    """
    ext_id: str

    def to_dict(self):
        """
        returns a dict representation of dataclas
        """
        return {
            "ext_id": self.ext_id
        }
