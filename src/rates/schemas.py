import datetime
import decimal
from typing import Optional

from pydantic import BaseModel


class RatePost(BaseModel):
    date: Optional[datetime.date] = None


class RateCreate(BaseModel):
    currency_id: int
    date: datetime.date
    currency_abbreviation: str
    currency_scale: int
    currency_name: str
    currency_rate: decimal.Decimal


class RateReturn(RateCreate):
    id: int
    dynamic: Optional[decimal.Decimal] = None
