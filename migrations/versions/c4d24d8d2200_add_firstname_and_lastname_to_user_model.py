"""Add firstName and lastName to User model

Revision ID: c4d24d8d2200
Revises: 040a4dcdf222
Create Date: 2025-06-12 18:21:31.359600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4d24d8d2200'
down_revision = '040a4dcdf222'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstName', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('lastName', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('lastName')
        batch_op.drop_column('firstName')

    # ### end Alembic commands ###
