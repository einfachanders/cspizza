from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Order(BaseModel):
    name: str
    price: int

class GuestLoginReq(BaseModel):
    user_name: str
    user_email: str

class GuestOrderReq(BaseModel):
    orders: list[Order]

class Session(BaseModel):
    session_id: str
    user_name: str
    user_email: str

class StoredOrder(BaseModel):
    order_id: str
    orders: list[Order]
    total_price: int
    ordered: Optional[bool] = False
    payed: Optional[bool] = False
