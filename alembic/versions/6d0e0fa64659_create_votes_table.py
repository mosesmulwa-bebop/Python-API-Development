"""create votes table

Revision ID: 6d0e0fa64659
Revises: 2258b66e38e4
Create Date: 2022-01-29 22:24:56.092835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d0e0fa64659'
down_revision = '2258b66e38e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
   
    )
    op.create_foreign_key('votes_posts_fkey', source_table='votes', referent_table='posts', 
    local_cols=['post_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('votes_users_fkey', source_table='votes', referent_table='users', 
    local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('votes_posts_fkey', table_name='votes')
    op.drop_constraint('votes_users_fkey', table_name='votes')
    op.drop_table('votes')
    pass
