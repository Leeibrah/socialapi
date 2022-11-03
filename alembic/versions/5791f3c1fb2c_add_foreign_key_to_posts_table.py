"""add foreign-key to posts table

Revision ID: 5791f3c1fb2c
Revises: 4f37519831a1
Create Date: 2022-11-01 14:20:30.375270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5791f3c1fb2c'
down_revision = '4f37519831a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("posts", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), nullable=False),
            insert_after="status"
        )
    op.create_foreign_key(
        'posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
