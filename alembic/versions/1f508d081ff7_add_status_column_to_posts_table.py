"""add status column to posts table

Revision ID: 1f508d081ff7
Revises: 149e273f18ef
Create Date: 2022-11-01 12:34:58.895377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f508d081ff7'
down_revision = '149e273f18ef'
branch_labels = None
depends_on = None


def upgrade() -> None:

    with op.batch_alter_table("posts", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("status", sa.Boolean(), nullable=False, server_default='TRUE'),
            insert_after="published"
        )
    # op.add_column(
    #     'posts',
    #     sa.Column('status', sa.Integer(), nullable=False)
    # )
    # op.execute('')
    pass


def downgrade() -> None:
    op.drop_column('posts', 'status')
    pass
