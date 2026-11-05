"""create_clients_and_orders_tables

Revision ID: f5ff01a1db29
Revises: 
Create Date: 2026-11-05 16:17:35.115951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5ff01a1db29'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        );
    ''')
    
    op.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            id SERIAL PRIMARY KEY,
            item TEXT NOT NULL,
            price INTEGER NOT NULL,
            client_id INTEGER NOT NULL REFERENCES clients(id)
        );
    ''')
    
    op.execute('''
        CREATE INDEX IF NOT EXISTS idx_orders_client_id ON orders (client_id);
    ''')



def downgrade() -> None:
    op.execute('DROP INDEX IF EXISTS idx_orders_client_id;' )
    op.execute('DROP TABLE IF EXISTS orders;')
    op.execute("DROP TABLE IF EXISTS clients;")

