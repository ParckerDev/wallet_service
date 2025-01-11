from decimal import Decimal
from pydantic import BaseModel
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Operation(BaseModel):
    operation_type: OperationType
    amount: Decimal


class WalletResponse(BaseModel):
    uuid: str
    balance: float
