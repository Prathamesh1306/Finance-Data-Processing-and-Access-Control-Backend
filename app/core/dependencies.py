import uuid
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import AsyncSessionLocal
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.models.user import User, RoleEnum
from app.services.user_service import get_user_by_id

api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    authorization: Optional[str] = Depends(api_key_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not authorization:
        raise UnauthorizedError(message="Authorization header missing")
    
    # Remove "Bearer " prefix if present
    if authorization.startswith("Bearer "):
        token = authorization[7:]  # Remove "Bearer " prefix
    else:
        token = authorization
    
    payload = decode_access_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedError(message="Invalid token payload")
        
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedError(message="Invalid user ID in token")
        
    user = await get_user_by_id(db, user_uuid)
    if not user:
        raise UnauthorizedError(message="User not found")
        
    if not user.is_active:
        raise ForbiddenError(message="Inactive user")
        
    return user

def require_roles(*roles: RoleEnum):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise ForbiddenError(message="Insufficient permissions")
        return current_user
    return role_checker
