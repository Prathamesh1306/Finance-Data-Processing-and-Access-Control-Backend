"""Fix enum typo

Revision ID: 002_fix_enum
Revises: 001_initial
Create Date: 2026-04-03 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_fix_enum'
down_revision: Union[str, Sequence[str], None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the column first, then the enum, then recreate both
    op.execute("ALTER TABLE transactions DROP COLUMN type")
    op.execute("DROP TYPE IF EXISTS typeofenum")
    op.execute("CREATE TYPE typeofenum AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("ALTER TABLE transactions ADD COLUMN type typeofenum NOT NULL DEFAULT 'INCOME'::typeofenum")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE transactions DROP COLUMN type")
    op.execute("DROP TYPE IF EXISTS typeofenum")
    op.execute("CREATE TYPE typeofenum AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("ALTER TABLE transactions ADD COLUMN type typeofenum NOT NULL DEFAULT 'INCOME'::typeofenum")
