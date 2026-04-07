"""Fix enum name from typeenum to typeofenum

Revision ID: 003_fix_enum_name
Revises: 002_fix_enum
Create Date: 2026-04-07 11:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003_fix_enum_name'
down_revision: Union[str, Sequence[str], None] = '002_fix_enum'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if old enum exists and fix it
    op.execute("ALTER TABLE transactions DROP COLUMN IF EXISTS type")
    op.execute("DROP TYPE IF EXISTS typeofenum")
    op.execute("DROP TYPE IF EXISTS typeenum")
    
    # Create the correct enum with the right name
    op.execute("CREATE TYPE typeofenum AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("ALTER TABLE transactions ADD COLUMN type typeofenum NOT NULL DEFAULT 'INCOME'::typeofenum")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE transactions DROP COLUMN type")
    op.execute("DROP TYPE IF EXISTS typeofenum")
    op.execute("CREATE TYPE typeenum AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("ALTER TABLE transactions ADD COLUMN type typeenum NOT NULL DEFAULT 'INCOME'::typeenum")
