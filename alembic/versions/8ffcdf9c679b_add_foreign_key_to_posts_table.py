"""add foreign key to posts table

Revision ID: 8ffcdf9c679b
Revises: a733ea13c3fd
Create Date: 2022-01-29 22:07:11.595966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ffcdf9c679b'
down_revision = 'a733ea13c3fd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
    sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
