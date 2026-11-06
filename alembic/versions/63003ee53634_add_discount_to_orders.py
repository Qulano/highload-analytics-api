"""add_discount_to_orders

Revision ID: 63003ee53634
Revises: f5ff01a1db29
Create Date: 2026-11-06 16:38:34.437455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63003ee53634'
down_revision: Union[str, Sequence[str], None] = 'f5ff01a1db29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        ALTER TABLE orders
        ADD COLUMN discount INTEGER NOT NULL DEFAULT 0;
    ''')


def downgrade() -> None:
   op.execute('''
    ALTER TABLE orders
    DROP COLUMN IF EXISTS discount;
    ''') 
