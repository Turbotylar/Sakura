"""add verified_role to guild

Revision ID: d9f1d82cd84c
Revises: e8f8a6f873cc
Create Date: 2021-11-28 00:26:29.641089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9f1d82cd84c'
down_revision = 'e8f8a6f873cc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('guilds', sa.Column('verified_role', sa.BigInteger, nullable=True))


def downgrade():
    op.drop_column('guilds', 'verified_role')
