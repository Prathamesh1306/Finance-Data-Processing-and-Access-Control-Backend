import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum = RoleEnum.VIEWER
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.VIEWER

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)
