import datetime
import decimal

from sqlalchemy import Date, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_class import Base


class Rate(Base):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    currency_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime.date] = mapped_column(Date)
    currency_abbreviation: Mapped[str] = mapped_column(String)
    currency_scale: Mapped[int] = mapped_column(Integer)
    currency_name: Mapped[str] = mapped_column(String)
    currency_rate: Mapped[decimal.Decimal] = mapped_column(Numeric)

    __table_args__ = (UniqueConstraint(currency_id, date),)
