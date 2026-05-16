"""001 - rename users.parent_id to users.distributor_id

Revision ID: 77e46c9242de
Revises: 
Create Date: 2026-05-16 14:20:57.896409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77e46c9242de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('distributor_id', sa.Integer(), nullable=True))

    op.execute('UPDATE users SET distributor_id = parent_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['distributor_id'], ['id'])
        batch_op.drop_column('parent_id')


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.INTEGER(), nullable=True))

    op.execute('UPDATE users SET parent_id = distributor_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['parent_id'], ['id'])
        batch_op.drop_column('distributor_id')
