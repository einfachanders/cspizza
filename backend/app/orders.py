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

async def mark_ordered(session_id: str) -> StoredOrder:
    orders[session_id].ordered = True
    return orders[session_id]

async def mark_payed(session_id: str) -> StoredOrder:
    orders[session_id].payed = True
    return orders[session_id]

async def get_order(session_id: str) -> StoredOrder:
    if session_id in orders.keys():
        return orders[session_id]
    else:
        return None

async def get_orders() -> dict[str, StoredOrder]:
    order_list = []
    for session_id, order in orders.items():
        order_json = order.model_dump()
        order_json.update(sessions.get_session_data(session_id))
        order_list.append(order_json)
    return order_list
