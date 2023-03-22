from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from pydantic.typing import Union
from decimal import Decimal

from src.utils import reformat_num


class BetBase(BaseModel):
    event_id: Union[int, str]
    amount: Union[Decimal, float, int, str]

    @validator('amount')
    def amount_format(cls, v) -> Decimal:
        num = reformat_num(v, 2)

        if num < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The amount must not be less than 0")

        return num


class BetOut(BetBase):
    id: Union[int, str]
    status: str


class ChangeStatus(BaseModel):
    event_id: Union[int, str]
    state: str
