from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from app.utils import get_session_cookie

router = APIRouter()


@router.get("/id")
async def get_session_id(request: Request):
    return get_session_cookie(request)
