from abc import ABC
from importlib import import_module
from typing import Literal, Unpack

from services.email.base import EmailServiceBaseClass


class EmailServiceStrategy(ABC):
    STRATEGIES = {"django": "services.email.django", "fake": "services.email.fake"}

    @staticmethod
    def resolve(strategy: Literal["django"]) -> EmailServiceBaseClass:
        if strategy not in EmailServiceStrategy.STRATEGIES:
            raise ValueError(f"Invalid email service strategy: {strategy}")

        module_path = EmailServiceStrategy.STRATEGIES[strategy]
        module = import_module(module_path)
        return module.EmailService
