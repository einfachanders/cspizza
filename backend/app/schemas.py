from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Order(BaseModel):
    name: str
    price: int

class GuestLoginReq(BaseModel):
    user_name: str
    user_email: str
    order_code: str

class AdminLoginReq(BaseModel):
    user_name: str
    user_email: str
    admin_token: str

class GuestOrderReq(BaseModel):
    orders: list[Order]

class Session(BaseModel):
    session_id: str
    user_name: str
    user_email: str
    is_admin: bool = False

class StoredOrder(BaseModel):
    order_id: str
    orders: list[Order]
    total_price: int
    ordered: Optional[bool] = True
    payed: Optional[bool] = False

class StoredOrderPatchReq(BaseModel):
    ordered: Optional[bool] = None
    payed: Optional[bool] = None