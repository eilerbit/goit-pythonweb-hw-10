"""Initial migration

Revision ID: 3b7e96bdaf0c
Revises: 
Create Date: 2025-03-29 19:47:57.908957
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '3b7e96bdaf0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), unique=True, nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('birthday', sa.Date(), nullable=True),
        sa.Column('additional_data', sa.Text(), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('contacts')
