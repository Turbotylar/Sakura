"""change welcome_channel to biginteger on guild

Revision ID: 29514eb25e3c
Revises: c5c9a50f757c
Create Date: 2021-11-28 04:58:13.640195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29514eb25e3c'
down_revision = 'c5c9a50f757c'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('guilds', 'welcome_channel', type_= sa.BigInteger)

def downgrade():
    op.alter_column('guilds', 'welcome_channel', type_= sa.Integer)
 
