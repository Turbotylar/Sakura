"""add auto_increment to primary keys

Revision ID: 6bb017fd9a5c
Revises: a48aae6a18d9
Create Date: 2021-11-28 02:00:59.037080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb017fd9a5c'
down_revision = 'a48aae6a18d9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('guilds', 'id', autoincrement=True)



def downgrade():
    op.alter_column('guilds', 'id', autoincrement=False)

