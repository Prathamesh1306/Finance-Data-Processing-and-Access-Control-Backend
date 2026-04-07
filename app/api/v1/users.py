import math
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_roles
from app.models.user import User, RoleEnum
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.user_service import list_users, get_user_by_id, create_user, update_user, delete_user

router = APIRouter()

@router.get("", response_model=PaginatedResponse[UserResponse], dependencies=[Depends(require_roles(RoleEnum.ADMIN))])
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    items, total = await list_users(db, page, page_size)
    pages = math.ceil(total / page_size) if total > 0 else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_roles(RoleEnum.ADMIN))])
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@router.post("", response_model=UserResponse, status_code=201, dependencies=[Depends(require_roles(RoleEnum.ADMIN))])
async def create_new_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, data)

@router.patch("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_roles(RoleEnum.ADMIN))])
async def update_existing_user(user_id: uuid.UUID, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user(db, user_id, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(
    user_id: uuid.UUID,
    current_user: User = Depends(require_roles(RoleEnum.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    await delete_user(db, user_id, current_user.id)
