import decimal
from typing import TypedDict


class RateDict(TypedDict):
    Cur_ID: int
    Date: str
    Cur_Abbreviation: str
    Cur_Scale: int
    Cur_Name: str
    Cur_OfficialRate: decimal.Decimal
