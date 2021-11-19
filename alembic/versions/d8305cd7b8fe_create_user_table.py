"""create user table

Revision ID: d8305cd7b8fe
Revises: 
Create Date: 2021-11-20 03:32:15.274526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8305cd7b8fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('discord_id', sa.Integer),
        sa.Column('is_bot_dev', sa.Boolean, default=False),
    )


def downgrade():
    op.drop_table('users')
