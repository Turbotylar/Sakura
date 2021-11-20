"""change roles to bigint

Revision ID: e8f8a6f873cc
Revises: b4aa3960dc91
Create Date: 2021-11-20 17:28:27.710033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f8a6f873cc'
down_revision = 'b4aa3960dc91'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('guilds', 'jail_role', type_= sa.BigInteger)
    op.alter_column('guilds', 'mute_role', type_= sa.BigInteger)
    op.alter_column('guilds', 'mod_role', type_= sa.BigInteger)


def downgrade():
    op.alter_column('guilds', 'jail_role', type_= sa.Integer)
    op.alter_column('guilds', 'mute_role', type_= sa.Integer)
    op.alter_column('guilds', 'mod_role', type_= sa.Integer)
