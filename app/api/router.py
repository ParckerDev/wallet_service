from fastapi import APIRouter, HTTPException, Depends
from schemas.wallet_schemas import WalletResponse, Operation
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import db_helper
from .crud import (
    create_wallet,
    get_wallet,
    get_wallets,
    deposit_operation,
    withdraw_operation,
    format_money,
)

sess = Annotated[AsyncSession, Depends(db_helper.get_db)]

router = APIRouter(prefix="/api/v1/wallets", tags=["WALLETS"])


@router.get("", response_model=list[WalletResponse])
async def get_all_wallets(session: sess):
    """
    Получает список всех кошельков.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        list[WalletResponse]: Список всех кошельков.
    """
    wallets = await get_wallets(session=session)
    return wallets


@router.get("/new", response_model=WalletResponse, status_code=201)
async def create_new_wallet(session: sess):
    """
    Создает новый кошелек.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        WalletResponse: Созданный кошелек.

    Raises:
        HTTPException: Если кошелек не был создан.
    """
    wallet = await create_wallet(session=session)
    if not wallet:
        raise HTTPException(status_code=500, detail="wallet don't create")
    return wallet


@router.get("/{wallet_uuid}", response_model=WalletResponse, status_code=200)
async def get_balance(session: sess, wallet_uuid: str):
    """
    Получает информацию о кошельке по его UUID.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        wallet_uuid (str): UUID кошелька.

    Returns:
        WalletResponse: Информация о кошельке.

    Raises:
        HTTPException: Если кошелек не найден.
    """
    wallet = await get_wallet(session=session, wallet_uuid=wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="wallet not found")
    return wallet


@router.post(
    "/{wallet_uuid}/operation",
    status_code=200,
    description="Test",
)
async def perf_operations(
    session: sess,
    wallet_uuid: str,
    operation: Operation,
):
    """
    Выполняет операцию (депозит или вывод) с указанным кошельком.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        wallet_uuid (str): UUID кошелька.
        operation (Operation): Операция, которую нужно выполнить.

    Returns:
        dict: Сообщение о результате операции и текущий баланс.

    Raises:
        HTTPException: Если кошелек не найден или недостаточно средств
        для вывода.
    """
    wallet = await get_wallet(session=session, wallet_uuid=wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if operation.operation_type == "DEPOSIT":
        await deposit_operation(
            session=session,
            wallet=wallet,
            amount=operation.amount,
        )
        return {
            "message": f"wallet deposit successful!",
            "balance": f"{format_money(wallet.balance)}$",
        }
    if operation.operation_type == "WITHDRAW":
        if wallet.balance < operation.amount:
            raise HTTPException(
                status_code=400,
                detail="The balance is less than the withdrawal amount!",
            )
        await withdraw_operation(
            session=session, wallet=wallet, amount=operation.amount
        )
        return {
            "message": f"The withdrawal was successful.",
            "balance": f"{format_money(wallet.balance)}$",
        }
