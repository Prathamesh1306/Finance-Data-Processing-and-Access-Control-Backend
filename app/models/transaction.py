import enum
import uuid
from datetime import date
from sqlalchemy import String, Boolean, Numeric, Date, Text, ForeignKey, CheckConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database import Base
from app.models.base import TimestampMixin

class TypeEnum(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class CategoryEnum(str, enum.Enum):
    SALARY = "SALARY"
    FREELANCE = "FREELANCE"
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    UTILITIES = "UTILITIES"
    ENTERTAINMENT = "ENTERTAINMENT"
    HEALTH = "HEALTH"
    EDUCATION = "EDUCATION"
    RENT = "RENT"
    OTHER = "OTHER"

class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"
    
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    type: Mapped[TypeEnum] = mapped_column(Enum(TypeEnum, name='typeofenum'), nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum, name='categoryenum'), nullable=False)
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
