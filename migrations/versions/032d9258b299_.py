"""empty message

Revision ID: 032d9258b299
Revises: 818bb5547a46
Create Date: 2025-02-05 16:48:59.936854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '032d9258b299'
down_revision = '818bb5547a46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'planet', ['home_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('home_id')

    # ### end Alembic commands ###
