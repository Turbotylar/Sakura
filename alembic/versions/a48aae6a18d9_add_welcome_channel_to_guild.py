"""add welcome_channel to guild

Revision ID: a48aae6a18d9
Revises: d9f1d82cd84c
Create Date: 2021-11-28 01:48:56.221074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a48aae6a18d9'
down_revision = 'd9f1d82cd84c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('guilds', sa.Column('welcome_channel', sa.Integer, nullable=True))


def downgrade():
    op.drop_column('guilds', 'welcome_channel')
