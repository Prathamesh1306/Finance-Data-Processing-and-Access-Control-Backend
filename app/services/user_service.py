import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundError, ConflictError, ForbiddenError
from app.core.security import hash_password

async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError(message="User not found")
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def list_users(db: AsyncSession, page: int, page_size: int) -> tuple[list[User], int]:
    count_stmt = select(func.count(User.id))
    total = await db.scalar(count_stmt) or 0
    
    stmt = select(User).order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    items = list(result.scalars().all())
    
    return items, total

async def create_user(db: AsyncSession, data: UserCreate) -> User:
    existing_user = await get_user_by_email(db, data.email)
    if existing_user:
        raise ConflictError(message="Email already registered")
        
    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(db: AsyncSession, user_id: uuid.UUID, data: UserUpdate) -> User:
    user = await get_user_by_id(db, user_id)
    
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active
        
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: uuid.UUID, requesting_user_id: uuid.UUID) -> None:
    if str(user_id) == str(requesting_user_id):
        raise ForbiddenError(message="Admin cannot delete themselves")
        
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()

async def set_user_active(db: AsyncSession, user_id: uuid.UUID, is_active: bool) -> User:
    user = await get_user_by_id(db, user_id)
    user.is_active = is_active
    await db.commit()
    await db.refresh(user)
    return user
