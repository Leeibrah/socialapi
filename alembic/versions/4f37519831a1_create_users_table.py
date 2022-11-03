"""create users table

Revision ID: 4f37519831a1
Revises: 1f508d081ff7
Create Date: 2022-11-01 14:05:38.377523

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '4f37519831a1'
down_revision = '1f508d081ff7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
