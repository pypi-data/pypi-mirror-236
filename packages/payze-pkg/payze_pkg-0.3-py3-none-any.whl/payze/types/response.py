"""
response types.
"""
from typing import Optional

from dataclasses import dataclass


@dataclass
class CardPayment:
    """
    CardPayment represents.
    """
    token: str
    preauthorize: bool
    google_pay: bool
    apple_pay: bool
    card_mask: bool
    card_expiration: Optional[str]
    merchant_id: Optional[str]
    terminal_id: Optional[str]
    rrn: Optional[str]
    processing_vendor_id: Optional[str]
    processing_vendor: Optional[str]

    def to_dict(self):
        """
        dict representation.
        """
        return {
            "preauthorize": self.preauthorize,
            "googlePay": self.google_pay,
            "applePay": self.apple_pay,
            "cardMask": self.card_mask,
            "card_expiration": self.card_expiration,
            "merchantId": self.merchant_id,
            "terminalId": self.terminal_id,
            "token": self.token,
            "rrn": self.rrn,
            "processingVendorId": self.processing_vendor_id,
            "processingVendor": self.processing_vendor
        }


@dataclass
class WalletPayment:
    """
    WalletPayment represents.
    """
    flow: str
    token: str
    tokenize_card: bool

    def to_dict(self):
        """
        Convert WalletPayment data class to a dictionary.
        """
        return {
            "flow": self.flow,
            "token": self.token,
            "tokenizeCard": self.tokenize_card
        }


@dataclass
class Hooks:
    """
    Hooks represents.
    """
    webhook_gateway: str
    success_redirect_gateway: str
    error_redirect_gateway: str

    def to_dict(self):
        """
        Convert Hooks data class to a dictionary.
        """
        return {
            "webhookGateway": self.webhook_gateway,
            "successRedirectGateway": self.success_redirect_gateway,
            "errorRedirectGateway": self.error_redirect_gateway
        }


@dataclass
class Payment:
    """
    Payment represents.
    """
    id: int
    requester_id: int
    transaction_id: str
    type: str
    source: str
    amount: float
    currency: str
    status: str
    card_payment: CardPayment
    wallet_payment: WalletPayment
    hooks: Hooks
    language: str
    idempotency_key: str
    metadata: Optional[dict]
    share_link: Optional[str]
    network: Optional[str]
    blocked_amount: Optional[float]
    captured_amount: Optional[float]
    refunded_amount: Optional[float]
    reversed_amount: Optional[float]
    settled_balance_amount: Optional[float]
    cross_currency_settlement: Optional[dict]
    settled: Optional[dict]
    reject_reason: Optional[str]
    fee: Optional[dict]
    channel: Optional[dict]
    payer: Optional[dict]
    receipt: Optional[dict]
    sand_box: bool
    captured_date: Optional[str]
    blocked_date: Optional[str]
    settled_date: Optional[str]
    refunded_date: Optional[str]
    reverse_date: Optional[str]
    rejected_date: Optional[str]
    created_date: str
    payment_url: Optional[str]
    version: int
    last_modified_date: str

    def to_dict(self):
        """
        Convert Payment data class to a dictionary.
        """
        return {
            "id": self.id,
            "requesterId": self.requester_id,
            "transactionId": self.transaction_id,
            "type": self.type,
            "source": self.source,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "cardPayment": self.card_payment.to_dict(),
            "walletPayment": self.wallet_payment.to_dict(),
            "hooks": self.hooks.to_dict(),
            "language": self.language,
            "idempotencyKey": self.idempotency_key,
            "metadata": self.metadata,
            "shareLink": self.share_link,
            "network": self.network,
            "blockedAmount": self.blocked_amount,
            "capturedAmount": self.captured_amount,
            "refundedAmount": self.refunded_amount,
            "reversedAmount": self.reversed_amount,
            "settledBalanceAmount": self.settled_balance_amount,
            "crossCurrencySettlement": self.cross_currency_settlement,
            "settled": self.settled,
            "rejectReason": self.reject_reason,
            "fee": self.fee,
            "channel": self.channel,
            "payer": self.payer,
            "receipt": self.receipt,
            "sandBox": self.sand_box,
            "capturedDate": self.captured_date,
            "blockedDate": self.blocked_date,
            "settledDate": self.settled_date,
            "refundedDate": self.refunded_date,
            "reverseDate": self.reverse_date,
            "rejectedDate": self.rejected_date,
            "createdDate": self.created_date,
            "paymentUrl": self.payment_url,
            "version": self.version,
            "lastModifiedDate": self.last_modified_date
        }


@dataclass
class Data:
    """
    Data Payment represents.
    """
    payment: Payment

    def to_dict(self):
        """
        Convert Data data class to a dictionary.
        """
        return {
            "payment": self.payment.to_dict()
        }


@dataclass
class ValueData:
    """
    Data Payment represents.
    """
    payment: Payment

    def to_dict(self):
        """
        Convert Data data class to a dictionary.
        """
        return {
            "payment": self.payment.to_dict()
        }


@dataclass
class Status:
    """
    Status Payment represents.
    """
    message: Optional[str]
    errors: Optional[dict]
    type: Optional[str]

    def to_dict(self):
        """
        Convert Status data class to a dictionary.
        """
        return {
            "message": self.message,
            "errors": self.errors,
            "type": self.type
        }


@dataclass
class ResponseAddCard:
    """
    Add card response representation.
    """
    data: Data
    status: Status

    def to_dict(self):
        """
        Convert ResponseAddCard data class to a dictionary.
        """
        return {
            "data": self.data.to_dict(),
            "status": self.status.to_dict()
        }


@dataclass
class ResponseVerifyCard:
    """
    Verify card response representation.
    """
    success: bool

    def to_dict(self):
        """
        Convert ResponseVerifyCard data class to a dictionary.
        """
        return {
            "success": self.success
        }


@dataclass
class ResponseRefund:
    """
    ResponseRefund response representation.
    """
    data: Data
    status: Status

    def to_dict(self):
        """
        Convert ResponseAddCard data class to a dictionary.
        """
        return {
            "data": self.data.to_dict(),
            "status": self.status.to_dict()
        }


@dataclass
class ResponseStatusCheck:
    """
    ResponseStatusCheck response representation.
    """
    value: Data
    status: Status

    def to_dict(self):
        """
        Convert ResponseStatucCheck data class to a dictionary.
        """
        return {
            "data": self.data.to_dict(),
            "status": self.value.to_dict()
        }
