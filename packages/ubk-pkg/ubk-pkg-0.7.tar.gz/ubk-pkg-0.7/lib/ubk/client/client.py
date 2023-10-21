"""
the base client for UniPostApi
"""
import logging

from requests import request

from ubk.types.error import ErrorResponse
from ubk.types.request import RequestBody
from ubk.types.request import RequestAccount2Card
from ubk.types.response import ResponseCheckStatus
from ubk.types.response import ResponseCreateCheck
from ubk.types.response import ResponseConfirmCheck
from ubk.types.response import ResponseAccount2Card
from ubk.exceptions.service import UBKServiceException
from ubk.types.request import RequestTransferCreditState
from ubk.types.request import RequestTransferCreditCreate
from ubk.types.request import RequestTransferCreditCancel
from ubk.types.request import RequestTransferCreditConfirm


logger = logging.getLogger(__name__)


class UniPosAPI:
    """
    the default UniPoApi
    """
    def __init__(
        self,
        url: str,
        token: str,
    ):
        self.url = url
        self.access_token = token
        self.timeout = 20
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        self.methods = {
            "create_check": "transfer.credit.create",
            "pay_check": "transfer.credit.confirm",
            "status_check": "transfer.credit.state",
            "cancel_check": "transfer.credit.cancel"
        }

    def __send_request(self, method, params=None):
        """
        do request.
        """
        data = RequestBody(
            method=method,
            params=params
        ).to_dict()

        response = request(
            method="POST",
            url=self.url,
            json=data,
            headers=self.headers,
            timeout=self.timeout
        )

        try:
            response = response.json()

        except Exception as exc:
            msg = "error ubk service - %s", exc
            logger.error(msg)
            raise UBKServiceException(msg) from exc

        # handle errors
        error = ErrorResponse(**response)

        if error.error is not None:
            msg = str(error)
            logger.error(msg)
            raise UBKServiceException(msg)

        return response

    def _create_check(self, params: RequestTransferCreditCreate) -> ResponseCreateCheck: # noqa
        """
        Implementation of create_check.
        """
        method = self.methods.get("create_check")
        params = params.to_dict()

        resp: dict = self.__send_request(method, params)

        return ResponseCreateCheck(**resp)

    def _pay_check(self, params: RequestTransferCreditConfirm) -> ResponseConfirmCheck: # noqa
        """
        Implementation of pay_check.
        """
        method = self.methods.get("pay_check")
        params = params.to_dict()

        resp: dict = self.__send_request(method, params)

        return ResponseConfirmCheck(**resp)

    def account2card(self, params: RequestAccount2Card) -> ResponseAccount2Card: # noqa
        """
        implementation of account2card.
        """
        params = params.to_dict()

        # create check
        resp_create_check: ResponseCreateCheck = self._create_check(
            params=RequestTransferCreditCreate(**params)
        )

        # pay check
        resp_pay_check: ResponseConfirmCheck = self._pay_check(
            params=RequestTransferCreditConfirm(
                ext_id=resp_create_check.result.get("ext_id")
            )
        )

        kwargs = resp_pay_check.to_dict()

        return ResponseAccount2Card(**kwargs)

    def status_check(self, params: RequestTransferCreditState) -> ResponseCheckStatus: # noqa
        """
        Implementation of status_check.
        """
        method = self.methods.get("status_check")
        params = params.to_dict()

        resp: dict = self.__send_request(method, params)

        return ResponseCheckStatus(**resp)

    def cancel_check(self, params: RequestTransferCreditCancel) -> ResponseCheckStatus: # noqa
        """
        Implementation of status_check.
        """
        method = self.methods.get("cancel_check")
        params = params.to_dict()

        resp: dict = self.__send_request(method, params)

        return ResponseCheckStatus(**resp)

