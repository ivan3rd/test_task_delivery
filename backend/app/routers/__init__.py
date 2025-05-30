from fastapi import APIRouter
from .package_routers import router as package_router
from .session_routers import router as session_router


main_router = APIRouter()
main_router.include_router(session_router, prefix="/session")
main_router.include_router(package_router, prefix="/package")
