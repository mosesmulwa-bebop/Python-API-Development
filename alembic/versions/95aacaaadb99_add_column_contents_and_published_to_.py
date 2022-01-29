"""add column contents and published to posts

Revision ID: 95aacaaadb99
Revises: 2f90fa7d88ab
Create Date: 2022-01-29 21:34:23.402073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95aacaaadb99'
down_revision = '2f90fa7d88ab'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
    sa.Column('content',sa.String(), nullable=False)
    )
    op.add_column('posts',
    sa.Column('published',sa.Boolean(), nullable=False)
    )  
    pass


def downgrade():
    op.drop_column('posts', 'title')
    op.drop_column('posts', 'published')
    pass
