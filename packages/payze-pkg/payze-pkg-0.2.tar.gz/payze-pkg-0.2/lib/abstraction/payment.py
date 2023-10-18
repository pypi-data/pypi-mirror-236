"""
payment abctraction.
"""
from abc import ABC
from abc import abstractmethod

from typing import Any


class Account2CardABC(ABC):
    """
    Account2CardABC implementation.
    """
    @abstractmethod
    def account2card(self, params: Any) -> Any:
        """
        abstractclassmethod method that's must implement in subclass.
        """
        raise NotImplementedError("account2card method is not implemented")

    @abstractmethod
    def status_check(self, params: Any) -> Any:
        """
        abstractclassmethod method that's must implement in subclass.
        """
        raise NotImplementedError("pay check method is not implemented")
