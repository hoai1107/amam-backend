"""Change primary key in vote model

Revision ID: 0e3ce5459b9c
Revises: 9692d2b9c78c
Create Date: 2023-01-25 20:59:11.304297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0e3ce5459b9c'
down_revision = '9692d2b9c78c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment_votes', 'comment_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('comment_votes', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('comment_votes', 'id')
    op.alter_column('post_votes', 'post_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('post_votes', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('post_votes', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_votes', sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.alter_column('post_votes', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('post_votes', 'post_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.add_column('comment_votes', sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.alter_column('comment_votes', 'user_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('comment_votes', 'comment_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###
