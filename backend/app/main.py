import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from app.routers import main_router
from app.db import session_manager
from app.utils import SessionCookieManager

DATABASE_URL = os.getenv('DATABASE_URL')


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init(DATABASE_URL+'?local_infile=1')
    yield
    await session_manager.close()

app = FastAPI(
    lifespan=lifespan
)
app.include_router(main_router, prefix="")


@app.middleware('http')
async def session_middleware(request: Request, call_next):
    session_id = SessionCookieManager.get_session_cookie(request)
    response = await call_next(request)
    if not session_id:
        SessionCookieManager.set_session_cookie(response)
    return response
