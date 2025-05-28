from uuid import uuid4
from fastapi import Request, Response


def set_session_cookie(response: Response):
    session_id = str(uuid4())
    response.set_cookie(
        key='session_id',
        value=session_id,
        max_age=60 * 60 * 24 * 7,  # 1 week
        httponly=True,
        secure=False,  # True in production with HTTPS
        samesite="lax"
    )


def get_session_cookie(request: Request):
    session_data = request.cookies.get('session_id')
    return session_data if session_data else None


def delete_session_cookie(response: Response):
    response.delete_cookie('session_id')



