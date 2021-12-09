from dataclasses import dataclass
from enum import Enum

from django.conf import settings


class TransactionTypes(Enum):
    NOT_DEFINED = 'NOT_DEFINED'

    # System defined types
    FIGHT_VOTING = 'FIGHT_VOTING'

    WELCOME = 'WELCOME'
    BUYING_POWERPOINTS = 'BUYING_POWERPOINTS'
    SYSTEM = 'SYSTEM'

    # With undefined type
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'


class PaymentSystemTransactionStatus(Enum):
    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'


@dataclass
class Currency:
    name: str


@dataclass
class ExchangeRate:
    first_currency: Currency
    second_currency: Currency
    first_second_rate: float

    def reverse_currency(self):
        return 1 / self.first_second_rate


DOLLARS_PER_POWER_POINT = 0.001
USD_VALUE_DECIMAL_PLACES = 2

USD = Currency(name="USD")
PP = Currency(name="PowerMeters")

PP_USD = ExchangeRate(first_currency=PP, second_currency=USD,
                      first_second_rate=DOLLARS_PER_POWER_POINT)
