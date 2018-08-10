"""table Holiday

Revision ID: ecc6a2c90c95
Revises: 429fd16dd705
Create Date: 2018-08-10 11:40:28.806360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecc6a2c90c95'
down_revision = '429fd16dd705'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('holiday',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('holiday_year', sa.Integer(), nullable=True),
    sa.Column('holiday_date', sa.Date(), nullable=True),
    sa.Column('holiday_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('holiday')
    # ### end Alembic commands ###