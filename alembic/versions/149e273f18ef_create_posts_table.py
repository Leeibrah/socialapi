"""create posts table

Revision ID: 149e273f18ef
Revises: 
Create Date: 2022-11-01 12:20:50.144224

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '149e273f18ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), server_default='FALSE', nullable=False),
        
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint('id'),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
