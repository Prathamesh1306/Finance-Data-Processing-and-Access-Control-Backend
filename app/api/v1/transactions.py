import math
import uuid
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_roles
from app.models.user import User, RoleEnum
from app.models.transaction import TypeEnum, CategoryEnum
from app.schemas.common import PaginatedResponse
from app.schemas.transaction import TransactionResponse, TransactionCreate, TransactionUpdate, TransactionFilter
from app.services.transaction_service import list_transactions, get_transaction_by_id, create_transaction, update_transaction, soft_delete_transaction

router = APIRouter()

@router.get("", response_model=PaginatedResponse[TransactionResponse])
async def get_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: TypeEnum | None = Query(None),
    category: CategoryEnum | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    min_amount: Decimal | None = Query(None),
    max_amount: Decimal | None = Query(None),
    current_user: User = Depends(require_roles(RoleEnum.VIEWER, RoleEnum.ANALYST, RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    filters = TransactionFilter(
        type=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount
    )
    items, total = await list_transactions(db, filters, page, page_size)
    pages = math.ceil(total / page_size) if total > 0 else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(require_roles(RoleEnum.VIEWER, RoleEnum.ANALYST, RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await get_transaction_by_id(db, transaction_id)

@router.post("", response_model=TransactionResponse, status_code=201)
async def create_new_transaction(
    data: TransactionCreate,
    current_user: User = Depends(require_roles(RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await create_transaction(db, data, current_user.id)

@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_existing_transaction(
    transaction_id: uuid.UUID,
    data: TransactionUpdate,
    current_user: User = Depends(require_roles(RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await update_transaction(db, transaction_id, data)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_transaction(
    transaction_id: uuid.UUID,
    current_user: User = Depends(require_roles(RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    await soft_delete_transaction(db, transaction_id)
