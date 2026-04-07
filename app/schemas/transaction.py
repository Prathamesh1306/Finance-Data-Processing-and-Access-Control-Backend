import uuid
from datetime import date
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

from app.models.transaction import TypeEnum, CategoryEnum

class TransactionBase(BaseModel):
    amount: Decimal = Field(gt=0)
    type: TypeEnum
    category: CategoryEnum
    date: date
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[TypeEnum] = None
    category: Optional[CategoryEnum] = None
    date: Optional[date] = None
    description: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: uuid.UUID
    is_deleted: bool
    created_by: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

class TransactionFilter(BaseModel):
    type: Optional[TypeEnum] = None
    category: Optional[CategoryEnum] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None

class DashboardSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    record_count: int
    period_from: Optional[date] = None
    period_to: Optional[date] = None
    
    model_config = ConfigDict(from_attributes=True)

class CategoryTotal(BaseModel):
    category: CategoryEnum
    total: Decimal
    count: int
    percentage: Decimal
    
    model_config = ConfigDict(from_attributes=True)

class TrendPoint(BaseModel):
    period_label: str
    income: Decimal
    expenses: Decimal
    net: Decimal
    
    model_config = ConfigDict(from_attributes=True)
