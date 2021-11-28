"""add is_debug_guild to guild

Revision ID: 168f8521afde
Revises: 29514eb25e3c
Create Date: 2021-11-28 23:35:51.420215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '168f8521afde'
down_revision = '29514eb25e3c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('guilds', sa.Column('is_debug_guild', sa.Boolean, default=False))


def downgrade():
    op.drop_column('guilds', 'is_debug_guild')
