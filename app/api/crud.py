from decimal import Decimal
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.wallet_model import Wallet


async def create_wallet(session: AsyncSession):
    """
    Создает новый кошелек и сохраняет его в базе данных.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        Wallet: Созданный кошелек с уникальным UUID.
    """
    wallet_uuid = str(uuid.uuid4())
    new_wallet = Wallet(uuid=wallet_uuid)
    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)
    return new_wallet


async def get_wallets(session: AsyncSession):
    """
    Получает список всех кошельков из базы данных.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        list[Wallet]: Список всех кошельков.
    """
    wallets = await session.scalars(select(Wallet))
    return wallets


async def get_wallet(session: AsyncSession, wallet_uuid: str) -> Wallet | None:
    """
    Получает кошелек по его UUID.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        wallet_uuid (str): UUID кошелька.

    Returns:
        Wallet | None: Найденный кошелек или None, если кошелек не найден.
    """
    stmt = select(Wallet).where(Wallet.uuid == wallet_uuid)
    wallet = await session.scalar(stmt)
    return wallet


def format_money(money):
    """
    Форматирует сумму денег до двух знаков после запятой.

    Args:
        money (Decimal): Сумма денег.

    Returns:
        str: Форматированная строка с суммой денег.
    """
    return str(Decimal(money).quantize(Decimal("0.00")))


async def deposit_operation(
    session: AsyncSession,
    wallet: Wallet,
    amount: Decimal,
):
    """
    Выполняет операцию депозита на указанный кошелек.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        wallet (Wallet): Кошелек, на который будет выполнен депозит.
        amount (Decimal): Сумма депозита.

    Returns:
        Wallet: Обновленный кошелек с новым балансом.
    """
    wallet.balance += amount
    await session.commit()
    await session.refresh(wallet)
    return wallet


async def withdraw_operation(
    session: AsyncSession,
    wallet: Wallet,
    amount: Decimal,
):
    """
    Выполняет операцию вывода средств с указанного кошелька.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        wallet (Wallet): Кошелек, с которого будет выполнен вывод.
        amount (Decimal): Сумма вывода.

    Returns:
        Wallet: Обновленный кошелек с новым балансом.
    """
    wallet.balance -= amount
    await session.commit()
    await session.refresh(wallet)
    return wallet
