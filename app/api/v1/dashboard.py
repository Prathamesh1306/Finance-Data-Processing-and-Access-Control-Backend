from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_roles
from app.models.user import User, RoleEnum
from app.models.transaction import TypeEnum
from app.schemas.transaction import DashboardSummary, CategoryTotal, TrendPoint
from app.services.dashboard_service import get_summary, get_category_totals, get_trends

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary(
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    current_user: User = Depends(require_roles(RoleEnum.VIEWER, RoleEnum.ANALYST, RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await get_summary(db, date_from, date_to)

@router.get("/category-totals", response_model=list[CategoryTotal])
async def dashboard_category_totals(
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    type: TypeEnum | None = Query(None),
    current_user: User = Depends(require_roles(RoleEnum.ANALYST, RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await get_category_totals(db, date_from, date_to, type)

@router.get("/trends", response_model=list[TrendPoint])
async def dashboard_trends(
    period: str = Query("MONTHLY"),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    current_user: User = Depends(require_roles(RoleEnum.ANALYST, RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await get_trends(db, period, date_from, date_to)
