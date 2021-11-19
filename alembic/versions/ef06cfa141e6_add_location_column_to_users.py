"""add location column to users

Revision ID: ef06cfa141e6
Revises: d8305cd7b8fe
Create Date: 2021-11-20 03:35:29.731637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef06cfa141e6'
down_revision = 'd8305cd7b8fe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('location', sa.String, nullable=True))


def downgrade():
    op.drop_column('users', 'location')
