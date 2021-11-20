"""change discord_id to bigint

Revision ID: b4aa3960dc91
Revises: 1126bd6f3cd6
Create Date: 2021-11-20 17:07:33.656927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4aa3960dc91'
down_revision = '1126bd6f3cd6'
branch_labels = None
depends_on = None


def upgrade():
    op.altar_column('guilds', 'discord_id', type_= sa.BigInteger)
    op.altar_column('users', 'discord_id', type_= sa.BigInteger)


def downgrade():
    op.altar_column('guilds', 'discord_id', type_= sa.Integer)
    op.altar_column('users', 'discord_id', type_= sa.Integer)
