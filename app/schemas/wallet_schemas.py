from decimal import Decimal
from pydantic import BaseModel
from enum import Enum


class OperationType(str, Enum):
    """
    Enum для определения типа операции с кошельком.

    Доступные типы операций:
    - DEPOSIT: Пополнение кошелька.
    - WITHDRAW: Снятие средств с кошелька.
    """

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Operation(BaseModel):
    """
    Модель для представления операции с кошельком.

    Attributes:
        operation_type (OperationType): Тип операции (пополнение или снятие).
        amount (Decimal): Сумма операции.
    """

    operation_type: OperationType
    amount: Decimal


class WalletResponse(BaseModel):
    """
    Модель для представления ответа о состоянии кошелька.

    Attributes:
        uuid (str): Уникальный идентификатор кошелька.
        balance (float): Текущий баланс кошелька.
    """

    uuid: str
    balance: float
