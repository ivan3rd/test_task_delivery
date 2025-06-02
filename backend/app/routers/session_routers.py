from fastapi import APIRouter, Request
from app.utils import SessionCookieManager

router = APIRouter()


@router.get("/id")
async def get_session_id(request: Request):
    return SessionCookieManager.get_session_cookie(request)
