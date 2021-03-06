"""dismiss

Revision ID: 6d8778f6ddd7
Revises: 4f5e898e8c08
Create Date: 2018-09-22 00:04:59.120514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d8778f6ddd7'
down_revision = '4f5e898e8c08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employes', sa.Column('dismissed', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_employes_dismissed'), 'employes', ['dismissed'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employes_dismissed'), table_name='employes')
    op.drop_column('employes', 'dismissed')
    # ### end Alembic commands ###
