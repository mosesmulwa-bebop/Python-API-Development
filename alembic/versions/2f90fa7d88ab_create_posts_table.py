"""create posts table

Revision ID: 2f90fa7d88ab
Revises: 
Create Date: 2022-01-29 20:58:57.079269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f90fa7d88ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
     sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True),
     sa.Column('title',sa.String(), nullable=False)  
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
