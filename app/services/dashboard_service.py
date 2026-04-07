from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from decimal import Decimal

from app.models.transaction import Transaction, TypeEnum
from app.schemas.transaction import DashboardSummary, CategoryTotal, TrendPoint

async def get_summary(db: AsyncSession, date_from: date | None, date_to: date | None) -> DashboardSummary:
    conditions = [Transaction.is_deleted == False]
    if date_from:
        conditions.append(Transaction.date >= date_from)
    if date_to:
        conditions.append(Transaction.date <= date_to)

    income_stmt = select(func.sum(Transaction.amount)).where(and_(Transaction.type == TypeEnum.INCOME, *conditions))
    expense_stmt = select(func.sum(Transaction.amount)).where(and_(Transaction.type == TypeEnum.EXPENSE, *conditions))
    count_stmt = select(func.count(Transaction.id)).where(and_(*conditions))

    total_income = await db.scalar(income_stmt) or Decimal('0.00')
    total_expenses = await db.scalar(expense_stmt) or Decimal('0.00')
    record_count = await db.scalar(count_stmt) or 0
    net_balance = Decimal(str(total_income)) - Decimal(str(total_expenses))

    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        record_count=record_count,
        period_from=date_from,
        period_to=date_to
    )

async def get_category_totals(db: AsyncSession, date_from: date | None, date_to: date | None, type_filter: TypeEnum | None) -> list[CategoryTotal]:
    conditions = [Transaction.is_deleted == False]
    if date_from:
        conditions.append(Transaction.date >= date_from)
    if date_to:
        conditions.append(Transaction.date <= date_to)
    if type_filter:
        conditions.append(Transaction.type == type_filter)

    total_stmt = select(func.sum(Transaction.amount)).where(and_(*conditions))
    overall_total = await db.scalar(total_stmt) or Decimal('0.00')
    overall_total = Decimal(str(overall_total))

    stmt = select(
        Transaction.category,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count")
    ).where(and_(*conditions)).group_by(Transaction.category).order_by(func.sum(Transaction.amount).desc())
    
    result = await db.execute(stmt)
    rows = result.all()

    category_totals = []
    for row in rows:
        cat_total = Decimal(str(row.total))
        percentage = (cat_total / overall_total * Decimal('100')).quantize(Decimal('0.01')) if overall_total > 0 else Decimal('0.00')
        category_totals.append(CategoryTotal(
            category=row.category,
            total=cat_total,
            count=row.count,
            percentage=percentage
        ))
    return category_totals

async def get_trends(db: AsyncSession, period: str, date_from: date | None, date_to: date | None) -> list[TrendPoint]:
    conditions = [Transaction.is_deleted == False]
    if date_from:
        conditions.append(Transaction.date >= date_from)
    if date_to:
        conditions.append(Transaction.date <= date_to)

    # Check database dialect and use appropriate function
    if 'postgresql' in str(db.bind.dialect):
        if period.upper() == "WEEKLY":
            period_expr = func.to_char(Transaction.date, 'IYYY-IW')
        else:
            period_expr = func.to_char(Transaction.date, 'YYYY-MM')
    else:
        # SQLite for testing
        if period.upper() == "WEEKLY":
            period_expr = func.strftime('%Y-%W', Transaction.date)
        else:
            period_expr = func.strftime('%Y-%m', Transaction.date)

    stmt = select(
        period_expr.label("period_label"),
        func.sum(Transaction.amount).filter(Transaction.type == TypeEnum.INCOME).label("income"),
        func.sum(Transaction.amount).filter(Transaction.type == TypeEnum.EXPENSE).label("expenses")
    ).where(and_(*conditions)).group_by(period_expr).order_by(period_expr.asc())

    result = await db.execute(stmt)
    rows = result.all()
    
    trends = []
    for row in rows:
        inc = Decimal(str(row.income)) if row.income else Decimal('0.00')
        exp = Decimal(str(row.expenses)) if row.expenses else Decimal('0.00')
        net = inc - exp
        trends.append(TrendPoint(
            period_label=row.period_label,
            income=inc,
            expenses=exp,
            net=net
        ))
    return trends
