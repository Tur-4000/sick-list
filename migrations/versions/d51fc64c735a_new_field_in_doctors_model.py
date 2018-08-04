"""new field in Doctors model

Revision ID: d51fc64c735a
Revises: b8a96c93d55d
Create Date: 2018-08-05 00:09:48.449028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd51fc64c735a'
down_revision = 'b8a96c93d55d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctors', sa.Column('last_visit', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('doctors', 'last_visit')
    # ### end Alembic commands ###
