from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class Wallet(Base):
    uuid: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(scale=2), default=0.0)
