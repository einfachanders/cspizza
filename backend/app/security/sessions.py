from cachetools import TTLCache
from fastapi import Request, HTTPException
from jose import jws
from typing import Annotated
import uuid
from app.core.config import settings
from app.schemas import Session

session_cache = TTLCache(
    maxsize=100,
    ttl=settings.FASTAPI_SESSION_TIMEOUT
)

def _create_session(user_name: str, user_email: str, is_admin: bool = False) -> str:
    for session_id, session in session_cache.items():
        if session.user_email == user_email:
            raise HTTPException(
                status_code=400,
                detail="E-Mail already in use."
            )
    while True:
        session_id = str(uuid.uuid4())  # Store session_id as a string
        if session_id not in session_cache:
            break
    session = Session(
        session_id=session_id,
        user_name=user_name,
        user_email=user_email,
        is_admin=is_admin
    )
    session_cache[session_id] = session
    return session_id

def get_session_data(session_id: str) -> Session | None:
    return session_cache.get(session_id)

def create_cookie(user_name: str, user_email: str, is_admin: bool = False) -> str:
    """Creates a signed new session cookie

    Args:
        user_name (str): Name of the user
        user_email (str): EMail of the user

    Returns:
        str: signed cookie value
    """
    session_id = _create_session(user_name, user_email, is_admin)
    cookie_value = jws.sign(
        payload=str(session_id).encode(),
        key=settings.FASTAPI_JWS_SECRET,
        algorithm="HS256"
    )
    return cookie_value


def _validate_session(session_id: str) -> Session | None:
    return session_cache.get(session_id)


def validate_cookie(request: Request) -> Session | None:
    cookie_value = request.cookies.get("pizza_session")
    if cookie_value is None:
        raise HTTPException(
            status_code=401,
            detail="Session cookie missing"
        )
    try:
        session_id = jws.verify(
            token=cookie_value,
            key=settings.FASTAPI_JWS_SECRET,
            algorithms=["HS256"]
        ).decode()
        session = _validate_session(session_id)
        if session is None:
            raise HTTPException(
                status_code=401,
                detail="Session expired or invalid"
            )
        return session
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid session cookie"
        )

async def check_admin(request: Request) -> bool:
    session = validate_cookie(request)
    if not session.is_admin:
        raise HTTPException(
            status_code=403,
            detail="User does not have the required access rights"
        )
    return session