"""alter column published to have default

Revision ID: 2258b66e38e4
Revises: 8ffcdf9c679b
Create Date: 2022-01-29 22:22:19.377584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2258b66e38e4'
down_revision = '8ffcdf9c679b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts','published',server_default='TRUE')
    pass


def downgrade():
    op.alter_column('posts','published',server_default='')
    pass
