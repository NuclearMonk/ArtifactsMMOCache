

from enum import Enum
from pydantic import BaseModel, EmailStr


class AccountStatus(Enum):
    standard = 'standard'
    founder = 'founder'
    gold_founder = 'gold_founder'
    vip_founder = 'vip_founder'


class AccountDetails(BaseModel):
    username: str
    subscribed: bool
    status: AccountStatus
    badges: list | None
    achievements_points: int
    banned: bool
    ban_reason: str | None


class MyAccountDetails(AccountDetails):
    email: EmailStr


class AccountDetailsSchema(BaseModel):
    data: AccountDetails


class MyAccountDetailsSchema(BaseModel):
    data: MyAccountDetails
