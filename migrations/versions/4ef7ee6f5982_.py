"""empty message

Revision ID: 4ef7ee6f5982
Revises: 940660f45efa
Create Date: 2018-12-08 11:24:20.764480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef7ee6f5982'
down_revision = '940660f45efa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'deleted')
    op.add_column('thirdparty', sa.Column('phone', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.drop_column('thirdparty', 'phone')
    # ### end Alembic commands ###