"""empty message

Revision ID: b7d6afce8e37
Revises: 2a3e9d09363f
Create Date: 2025-02-05 22:12:12.588703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7d6afce8e37'
down_revision = '2a3e9d09363f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.String(length=50),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
