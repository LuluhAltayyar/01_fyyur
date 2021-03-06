"""empty message

Revision ID: 01ca5329b39f
Revises: 
Create Date: 2020-10-14 14:08:04.183018

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '01ca5329b39f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'website')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.create_table('show',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='show_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='show_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='show_pkey')
    )
    # ### end Alembic commands ###
