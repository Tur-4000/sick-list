"""diacrisis

Revision ID: 13578a91223f
Revises: 6d8778f6ddd7
Create Date: 2018-09-24 23:30:24.311133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13578a91223f'
down_revision = '6d8778f6ddd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diacrisis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diagnoses', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diacrisis_diagnoses'), 'diacrisis', ['diagnoses'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_diacrisis_diagnoses'), table_name='diacrisis')
    op.drop_table('diacrisis')
    # ### end Alembic commands ###