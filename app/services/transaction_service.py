import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionFilter
from app.core.exceptions import NotFoundError

async def get_transaction_by_id(db: AsyncSession, transaction_id: uuid.UUID) -> Transaction:
    stmt = select(Transaction).where(Transaction.id == transaction_id, Transaction.is_deleted == False)
    result = await db.execute(stmt)
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise NotFoundError("Transaction not found or deleted")
    return transaction

async def list_transactions(db: AsyncSession, filters: TransactionFilter, page: int, page_size: int) -> tuple[list[Transaction], int]:
    conditions = [Transaction.is_deleted == False]
    
    if filters.type:
        conditions.append(Transaction.type == filters.type)
    if filters.category:
        conditions.append(Transaction.category == filters.category)
    if filters.date_from:
        conditions.append(Transaction.date >= filters.date_from)
    if filters.date_to:
        conditions.append(Transaction.date <= filters.date_to)
    if filters.min_amount is not None:
        conditions.append(Transaction.amount >= filters.min_amount)
    if filters.max_amount is not None:
        conditions.append(Transaction.amount <= filters.max_amount)
        
    count_stmt = select(func.count(Transaction.id)).where(and_(*conditions))
    total = await db.scalar(count_stmt) or 0
    
    stmt = select(Transaction).where(and_(*conditions)).order_by(Transaction.date.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    items = list(result.scalars().all())
    
    return items, total

async def create_transaction(db: AsyncSession, data: TransactionCreate, created_by: uuid.UUID) -> Transaction:
    transaction = Transaction(
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        description=data.description,
        created_by=created_by
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def update_transaction(db: AsyncSession, transaction_id: uuid.UUID, data: TransactionUpdate) -> Transaction:
    transaction = await get_transaction_by_id(db, transaction_id)
    
    if data.amount is not None:
        transaction.amount = data.amount
    if data.type is not None:
        transaction.type = data.type
    if data.category is not None:
        transaction.category = data.category
    if data.date is not None:
        transaction.date = data.date
    if data.description is not None:
        transaction.description = data.description
        
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def soft_delete_transaction(db: AsyncSession, transaction_id: uuid.UUID) -> None:
    transaction = await get_transaction_by_id(db, transaction_id)
    transaction.is_deleted = True
    await db.commit()
