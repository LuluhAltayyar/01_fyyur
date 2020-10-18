"""empty message

Revision ID: 5db55e634b0c
Revises: 6ed3d30fec21
Create Date: 2020-10-14 20:48:25.872817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5db55e634b0c'
down_revision = '6ed3d30fec21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_description')
    # ### end Alembic commands ###
