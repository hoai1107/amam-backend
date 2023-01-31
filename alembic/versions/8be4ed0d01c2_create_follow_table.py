"""Create follow table

Revision ID: 8be4ed0d01c2
Revises: 2af421d51153
Create Date: 2023-01-31 10:52:42.910341

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8be4ed0d01c2'
down_revision = '2af421d51153'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('following_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('followed_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('following_id', 'followed_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follow')
    # ### end Alembic commands ###