"""add auto increment to primary keys with identity

Revision ID: c5c9a50f757c
Revises: 6bb017fd9a5c
Create Date: 2021-11-28 02:12:20.412387

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.sql as sas


# revision identifiers, used by Alembic.
revision = 'c5c9a50f757c'
down_revision = '6bb017fd9a5c'
branch_labels = None
depends_on = None

guilds = sas.table('guilds',
    sa.Column('id', sa.Integer, sa.Identity(), primary_key=True),
    sa.Column('id_old', sa.Integer, primary_key=True)
)

users = sas.table('users',
    sa.Column('id', sa.Integer, sa.Identity(), primary_key=True),
    sa.Column('id_old', sa.Integer, primary_key=True)
)

def upgrade():
    op.alter_column('guilds', 'id', new_column_name='id_old')
    op.add_column('guilds',
        sa.Column('id', sa.Integer, sa.Identity(), primary_key=True)
    )
    op.execute(
        guilds.update().
            values({"id": guilds.c.id_old})
    )
    op.drop_column('guilds', 'id_old')


    op.alter_column('users', 'id', new_column_name='id_old')
    op.add_column('users',
        sa.Column('id', sa.Integer, sa.Identity(), primary_key=True)
    )
    op.execute(
        users.update().
            values({"id": users.c.id_old})
    )
    op.drop_column('users', 'id_old')


def downgrade():
    op.alter_column('guilds', 'id', new_column_name='id_old')
    op.add_column('guilds',
        sa.Column('id', sa.Integer, primary_key=True)
    )
    op.execute(
        guilds.update().
            values({"id": guilds.c.id_old})
    )
    op.drop_column('guilds', 'id_old')


    op.alter_column('users', 'id', new_column_name='id_old')
    op.add_column('users',
        sa.Column('id', sa.Integer, primary_key=True)
    )
    op.execute(
        users.update().
            values({"id": users.c.id_old})
    )
    op.drop_column('users', 'id_old')
