from fastapi import FastAPI, Response, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
import app.orders as orders
from app.schemas import AdminLoginReq, GuestLoginReq, GuestOrderReq, Session, StoredOrder, StoredOrderPatchReq
from app.security import sessions

# init FastAPI application
app = FastAPI(
    title=settings.FASTAPI_PROJECT_NAME,
    openapi_url=f"{settings.FASTAPI_BASE_URI}/openapi.json",
    docs_url=f"{settings.FASTAPI_BASE_URI}/docs"
)

# Set all CORS enabled origins
if settings.FASTAPI_BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.FASTAPI_BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["GET", "PATCH", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

@app.post(f"{settings.FASTAPI_BASE_URI}/v1/guest-login")
async def guest_login(guest_login_req: GuestLoginReq):
    if not guest_login_req.order_code == settings.FASTAPI_ORDER_CODE:
        raise HTTPException(
            status_code=401,
            detail="Incorrect login code"
        )
    cookie_value = sessions.create_cookie(
        user_name=guest_login_req.user_name,
        user_email=guest_login_req.user_email
    )
    response = Response(status_code=200)
    response.set_cookie(
        key="pizza_session",
        value=cookie_value,
        max_age=settings.FASTAPI_SESSION_TIMEOUT,
        expires=settings.FASTAPI_SESSION_TIMEOUT,
        path="/",
        domain=settings.FASTAPI_DOMAIN,
        secure=True if settings.FASTAPI_PROTOCOL == "https" else False,
        httponly=True,
        samesite="lax"
    )
    return response

@app.post(f"{settings.FASTAPI_BASE_URI}/v1/admin-login")
async def admin_login(guest_login_req: AdminLoginReq):
    if not guest_login_req.admin_token == settings.FASTAPI_ADMIN_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Incorrect admin token"
        )
    cookie_value = sessions.create_cookie(
        user_name=guest_login_req.user_name,
        user_email=guest_login_req.user_email,
        is_admin=True
    )
    response = Response(status_code=200)
    response.set_cookie(
        key="pizza_session",
        value=cookie_value,
        max_age=settings.FASTAPI_SESSION_TIMEOUT,
        expires=settings.FASTAPI_SESSION_TIMEOUT,
        path="/",
        domain=settings.FASTAPI_DOMAIN,
        secure=True if settings.FASTAPI_PROTOCOL == "https" else False,
        httponly=True,
        samesite="lax"
    )
    return response

@app.post(f"{settings.FASTAPI_BASE_URI}/v1/guest-order")
async def guest_order(guest_order_req: GuestOrderReq, session: Session = Depends(sessions.validate_cookie)):
    order_id = await orders.generate_order_id()
    order = StoredOrder(
        order_id=order_id,
        session=session,
        orders=guest_order_req.orders,
        total_price=sum(order.price for order in guest_order_req.orders)
    )
    order = await orders.add_order(order_id, order, session.session_id)
    return order

@app.get(f"{settings.FASTAPI_BASE_URI}/v1/guest-order")
async def get_order(session: Session = Depends(sessions.validate_cookie)):
    order = await orders.get_order(session.session_id)
    return order

@app.get(f"{settings.FASTAPI_BASE_URI}/v1/orders")
async def get_orders(session: Session = Depends(sessions.check_admin)):
    all_orders = await orders.get_orders()
    return all_orders

@app.patch("/api/v1/orders/{order_id}")
async def patch_order(order_id: str, patch_req: StoredOrderPatchReq,
                      session: Session = Depends(sessions.check_admin)):
    order = await orders.get_order_by_id(order_id)
    if order is None:
        return HTTPException(
            status_code=404,
            detail="Order not found"
        )
    order = await orders.update_order(order.order_id, **patch_req.model_dump())
    return order
