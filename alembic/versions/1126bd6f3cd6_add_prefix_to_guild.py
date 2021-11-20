"""add prefix to guild

Revision ID: 1126bd6f3cd6
Revises: b29e9b74c4aa
Create Date: 2021-11-20 14:59:25.875686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1126bd6f3cd6'
down_revision = 'b29e9b74c4aa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('guilds', sa.Column('custom_prefix', sa.String, nullable=True))


def downgrade():
    op.drop_column('guilds', 'custom_prefix')
