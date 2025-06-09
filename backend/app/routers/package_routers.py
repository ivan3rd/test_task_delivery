from uuid import UUID
from math import ceil
import logging
import sqlalchemy as sa

from fastapi import APIRouter, HTTPException, Request
from app.db import db_session
from app.utils import SessionCookieManager, get_dollar_exchange_rate
from app.schemas import (
    PackageInSchema, PackageOutSchema, PackageTypeSchema, PaginationResponse
)
from app.models import PackageModel, PackageTypeModel


logger = logging.getLogger('uvicorn.error')

router = APIRouter()

@router.get("/types")
async def get_package_types(request: Request) -> list[PackageTypeSchema]:
    """
    GET method\n
    List of all available package types \n
    """
    types = await PackageTypeModel.get_all()
    return [PackageTypeSchema.model_validate(_) for _ in types]


@router.get("/")
async def get_packages(
    request: Request,
    package_type: str = None,
    page: int = 1,
    page_size: int = 10,
) -> PaginationResponse:
    """
    GET method\n
    Returns paginated list of all items for whole session.\n
    parameter 'package_type' for filtering by name of package type\n
    if not provided, default 'page'=1 and 'page_size'=10\n
    """
    if page < 1:
        raise HTTPException(status_code=422, detail="page can't be less than 1")
    session_id = SessionCookieManager.get_session_cookie(request)
    packages = await PackageModel.get_all(
        page, page_size, package_type=package_type, session_id=session_id
    )
    packages_total = await PackageModel.get_total_count(
        package_type=package_type,
        session_id=session_id
    )
    total_pages = ceil(packages_total/page_size)
    return PaginationResponse(
        current_page=page,
        page_size=page_size,
        total_pages=total_pages,
        total_items=packages_total,
        results=[PackageOutSchema.model_validate(_) for _ in packages]
    )


@router.get("/{package_id}")
async def get_package(
    request: Request,
    package_id: UUID
) -> PackageOutSchema:
    """
    GET method\n
    Returns a single instance of packages by provided package_id\n
    """
    session_id = SessionCookieManager.get_session_cookie(request)
    package = await PackageModel.get_by_id(package_id, session_id)
    if not package:
        raise HTTPException(status_code=404, detail="package by given id was not found or does not belong to this session")
    return PackageOutSchema.model_validate(package)


@router.post("/", status_code=201)
async def post_package(
    request: Request,
    data: PackageInSchema,
) -> PackageOutSchema:
    """
    POST method\n
    Registration of package. Returns package information with id\n
    """
    session_id = SessionCookieManager.get_session_cookie(request)
    package_type = await PackageTypeModel.get_by_id(data.type_id)
    if not package_type:
        raise HTTPException(status_code=422, detail="package type by given type_id was not found")
    package = PackageModel(
        name=data.name,
        weight=data.weight,
        type_id=data.type_id,
        content_cost=data.content_cost,
        session_id=session_id,
    )
    async with db_session() as session:
        session.add(package)
        await session.commit()
    return PackageOutSchema.model_validate(package)


@router.put('/set-delivery-cost')
async def set_delivery_cost(request: Request):
    logger.info('set_delivery_cost(). Starting recounting delivery cost of a packages')
    der = await get_dollar_exchange_rate()
    if der is None:
        raise HTTPException(status_code=422, detail="Couldn't get der data from service. Can't proceed to recalculate delivery cost")
    async with db_session() as session:
        # Because data on packages could be extremly large,
        # async streaming will be used in order to not overload ram of container
        query = sa.select(PackageModel).where(
            PackageModel.delivery_cost.is_(None)
        )
        data = await session.stream_scalars(query)

        packages_cost_recounted = 0
        async for package in data:
            package.count_delivery_cost(der)
            packages_cost_recounted += 1
        logger.info(f'set_delivery_cost(). Delivery cost was recounted for {packages_cost_recounted} packages.')
        await session.commit()
    return True
