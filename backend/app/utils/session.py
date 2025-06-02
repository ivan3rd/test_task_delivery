from uuid import uuid4, UUID
from fastapi import Request, Response



class SessionCookieManager():

    @classmethod
    def set_session_cookie(cls, response: Response):
        session_id = str(uuid4())
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age=60 * 60 * 24 * 7,  # 1 week
            httponly=True,
            secure=False,  # True in production with HTTPS
            samesite="lax"
        )

    @classmethod
    def get_session_cookie(cls, request: Request) -> UUID | str | None:
        session_data = request.cookies.get('session_id')
        return session_data if session_data else None

    @classmethod
    def delete_session_cookie(cls, response: Response):
        response.delete_cookie('session_id')
