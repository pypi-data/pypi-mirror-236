"""
Payze Account2Card implementation.
"""
import requests

from payze.types.request import Hooks
from payze.types.request import WalletPayment
from payze.types.request import RequestRefund
from payze.types.request import RequestStatusCheck
from payze.types.request import RequestAddCardCreate
from payze.types.request import RequestVerifyCardData

from payze.types.response import Data
from payze.types.response import Status
from payze.types.response import Payment
from payze.types.response import ResponseRefund
from payze.types.response import ResponseAddCard
from payze.types.response import ResponseVerifyCard

from payze.types.params import RefundParam
from payze.types.params import StatusCheckParam
from payze.types.params import AddCardDataParam
from payze.types.params import VerifyCardDataParam
from payze.utils.cases import to_snake_case
from payze.utils.decorator import send_request_decorator

from payze.exceptions.service import NotImplementException


class PayzeAccount2CardAPI:
    """
    PayzeAccount2CardAPI provides account2card API functionality.
    """
    def __init__(
        self,
        url: str,
        key: str,
        secret: str,
        url_mobile_cards: str,
        web_hook_gateway: str,
        error_redirect_gateway: str,
        success_redirect_gateway: str,
    ):
        self.url = url
        self.url_mobile_cards = url_mobile_cards
        self.web_hook_gateway = web_hook_gateway
        self.error_redirect_gateway = error_redirect_gateway
        self.success_redirect_gateway = success_redirect_gateway

        self.headers: dict = {
            "Authorization": f"{key}:{secret}",
            # for verify card
            "Content-Type": "application/x-www-form-urlencoded"
        }

    @send_request_decorator
    def __send_request(self, method, data=None, json_data=None, url=None, params=None): # noqa

        if url is None:
            url = self.url
            self.headers["Content-Type"] = "application/json"

        return requests.request(
            method=method,
            url=url,
            data=data,
            json=json_data,
            headers=self.headers,
            params=params,
            timeout=20
        )

    def add_card(self, params: AddCardDataParam) -> ResponseAddCard:
        """
        that's used for getting the transaction id of adding card.
        """
        json_data = RequestAddCardCreate(
            source=params.source,
            amount=params.amount,
            currency=params.currency,
            language=params.language,
            wallet_payment=WalletPayment(
                tokenize_card=params.tokenize_card
            ),
            hooks=Hooks(
                web_hook_gateway=self.web_hook_gateway,
                success_redirect_gateway=self.success_redirect_gateway,
                error_redirect_gateway=self.error_redirect_gateway
            )
        ).to_dict()

        resp = self.__send_request(
            method="PUT",
            json_data=json_data
        )

        return ResponseAddCard(
            data=Data(
                payment=Payment(
                    **to_snake_case(d=resp.get("data").get("payment"))
                )
            ),
            status=Status(
                **to_snake_case(d=resp.get("status"))
            )
        )

    def verify_card(self, params: VerifyCardDataParam) -> ResponseVerifyCard:
        """
        that's used for verify card token.
        """
        json_data = RequestVerifyCardData(
            number=params.number,
            card_holder=params.card_holder,
            expire_date=params.expire_date,
            transaction_id=params.transaction_id
        ).to_form()

        resp = self.__send_request(
            method="POST",
            url=self.url_mobile_cards,
            data=json_data
        )

        return ResponseVerifyCard(
            success=resp.get("success")
        )

    def account2card(self, params: RefundParam):
        """
        that's used accound2card method (refund)
        """
        json_data = RequestRefund(
            source=params.source,
            amount=params.amount,
            language=params.language,
            currency=params.currency,
            token=params.token,
            hooks=Hooks(
                web_hook_gateway=self.web_hook_gateway,
                success_redirect_gateway=self.success_redirect_gateway,
                error_redirect_gateway=self.error_redirect_gateway
            )
        ).to_dict()

        resp = self.__send_request(
            method="PUT",
            json_data=json_data
        )

        return ResponseRefund(
            data=Data(
                payment=Payment(
                    **to_snake_case(d=resp.get("data").get("payment"))
                )
            ),
            status=Status(
                **to_snake_case(d=resp.get("status"))
            )
        )

    def status_check(self, params: StatusCheckParam) -> str:
        """
        check transition status.
        """
        self.url = self.url + "/query/token-based"

        params = RequestStatusCheck(
            check_id=params.check_id
        ).to_query_param()

        resp = self.__send_request(
            method="GET",
            params=params
        )

        # TODO: need implement with dataclasses in future

        if resp.get("data").get("value")[0].get("status") and resp.get("data").get("count") == 1: # noqa
            return resp.get("data").get("value")[0].get("status")

        raise NotImplementException(
            message="status_check is not implemented with dataclasses"
        )
