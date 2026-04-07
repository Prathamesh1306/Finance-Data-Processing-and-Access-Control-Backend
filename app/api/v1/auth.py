from fastapi import APIRouter, Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedError, ForbiddenError

router = APIRouter()

# Define the security scheme for OpenAPI/Swagger documentation
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user_data = UserCreate(
        email=request.email,
        full_name=request.full_name,
        password=request.password
    )
    user = await create_user(db, user_data)
    return user

@router.post("/login", response_model=TokenResponse, summary="Get API Key for Authentication")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Login to get an API key for authentication.
    
    Use the returned access_token in the Authorization header as:
    - Authorization: Bearer <access_token>
    - Or just: Authorization: <access_token>
    
    Then use this token in Swagger UI by clicking "Authorize" button and entering the token.
    """
    user = await get_user_by_email(db, request.email)
    if not user:
        raise UnauthorizedError(message="Wrong credentials")
    
    if not verify_password(request.password, user.hashed_password):
        raise UnauthorizedError(message="Wrong credentials")
        
    if not user.is_active:
        raise ForbiddenError(message="Inactive user")
        
    token = create_access_token(subject=str(user.id), role=user.role.value)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=3600
    )
