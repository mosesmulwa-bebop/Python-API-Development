"""add column created at to posts

Revision ID: a733ea13c3fd
Revises: 3a1470f99f61
Create Date: 2022-01-29 21:59:42.338475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a733ea13c3fd'
down_revision = '3a1470f99f61'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', 
    
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    pass
