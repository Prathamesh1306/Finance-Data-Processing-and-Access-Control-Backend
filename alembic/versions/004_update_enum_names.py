"""Update enum names in model definitions

Revision ID: 004_update_enum_names
Revises: 003_fix_enum_name
Create Date: 2026-04-07 11:58:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '004_update_enum_names'
down_revision: Union[str, Sequence[str], None] = '003_fix_enum_name'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop columns first, then enums, then recreate everything
    op.execute("ALTER TABLE transactions DROP COLUMN IF EXISTS type")
    op.execute("ALTER TABLE transactions DROP COLUMN IF EXISTS category")
    
    # Drop and recreate enums
    op.execute("DROP TYPE IF EXISTS typeofenum CASCADE")
    op.execute("DROP TYPE IF EXISTS typeenum CASCADE")
    op.execute("DROP TYPE IF EXISTS categoryenum CASCADE")
    
    op.execute("CREATE TYPE typeofenum AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("CREATE TYPE categoryenum AS ENUM ('SALARY', 'FREELANCE', 'FOOD', 'TRANSPORT', 'UTILITIES', 'ENTERTAINMENT', 'HEALTH', 'EDUCATION', 'RENT', 'OTHER')")
    
    # Recreate columns
    op.execute("ALTER TABLE transactions ADD COLUMN type typeofenum NOT NULL DEFAULT 'INCOME'::typeofenum")
    op.execute("ALTER TABLE transactions ADD COLUMN category categoryenum NOT NULL DEFAULT 'OTHER'::categoryenum")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE IF EXISTS typeofenum")
    op.execute("DROP TYPE IF EXISTS categoryenum")
    op.execute("CREATE TYPE typeenum AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("CREATE TYPE categoryenum AS ENUM ('SALARY', 'FREELANCE', 'FOOD', 'TRANSPORT', 'UTILITIES', 'ENTERTAINMENT', 'HEALTH', 'EDUCATION', 'RENT', 'OTHER')")
