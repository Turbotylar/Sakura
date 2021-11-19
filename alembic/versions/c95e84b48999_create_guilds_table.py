"""create guilds table

Revision ID: c95e84b48999
Revises: ef06cfa141e6
Create Date: 2021-11-20 04:26:59.840379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c95e84b48999'
down_revision = 'ef06cfa141e6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'guilds',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('discord_id', sa.Integer),
        sa.Column('jail_role', sa.Integer, nullable=True),
        sa.Column('mute_role', sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_table('guilds')
