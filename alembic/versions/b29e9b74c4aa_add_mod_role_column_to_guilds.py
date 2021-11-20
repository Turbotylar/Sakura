"""add mod role column to guilds

Revision ID: b29e9b74c4aa
Revises: c95e84b48999
Create Date: 2021-11-20 05:22:48.824026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b29e9b74c4aa'
down_revision = 'c95e84b48999'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('guilds', sa.Column('mod_role', sa.Integer, nullable=True))


def downgrade():
    op.drop_column('guilds', 'mod_role')
