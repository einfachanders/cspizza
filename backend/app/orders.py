import uuid
from app.schemas import StoredOrder
from app.security import sessions

orders: dict[str, StoredOrder] = {}

async def generate_order_id() -> uuid.UUID:
    while True:
        order_id = str(uuid.uuid4())  # Store session_id as a string
        if order_id not in orders:
            break
    return order_id

async def add_order(order_id: str, order: StoredOrder, session_id: str) -> StoredOrder:
    orders[session_id] = order
    return orders[session_id]

async def get_order(session_id: str) -> StoredOrder:
    if session_id in orders.keys():
        return orders[session_id]
    else:
        return None

async def get_order_by_id(order_id: str) -> StoredOrder:
    order = None
    for session_id, order in orders.items():
        if order.order_id == order_id:
            return order
    return order

async def get_session_for_order(order_id: str) -> str:
    session_id = None
    for session_id, order in orders.items():
        if order.order_id == order_id:
            return session_id
    return session_id

async def get_orders() -> dict[str, StoredOrder]:
    order_list = []
    if len(orders) > 0:
        for session_id, order in orders.items():
            order_json = order.model_dump()
            order_json.update(sessions.get_session_data(session_id))
            order_list.append(order_json)
    return order_list

async def update_order(order_id: str, **kwargs) -> StoredOrder:
    session_id = await get_session_for_order(order_id)
    if orders[session_id] is not None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(orders[session_id], key, value)
    return orders[session_id]
