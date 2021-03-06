"""new init

Revision ID: a864508dd9dd
Revises: 
Create Date: 2018-08-11 10:10:22.250648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a864508dd9dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('job_title', sa.String(length=254), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employes_first_name'), 'employes', ['first_name'], unique=False)
    op.create_index(op.f('ix_employes_last_name'), 'employes', ['last_name'], unique=False)
    op.create_index(op.f('ix_employes_middle_name'), 'employes', ['middle_name'], unique=False)
    op.create_table('holiday',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('holiday_year', sa.Integer(), nullable=True),
    sa.Column('holiday_date', sa.Date(), nullable=True),
    sa.Column('holiday_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_holiday_holiday_date'), 'holiday', ['holiday_date'], unique=True)
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('birth_year', sa.Date(), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patients_first_name'), 'patients', ['first_name'], unique=False)
    op.create_index(op.f('ix_patients_last_name'), 'patients', ['last_name'], unique=False)
    op.create_index(op.f('ix_patients_middle_name'), 'patients', ['middle_name'], unique=False)
    op.create_table('lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sick_list_number', sa.String(length=32), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('first_checkin', sa.Date(), nullable=True),
    sa.Column('second_checkin', sa.Date(), nullable=True),
    sa.Column('vkk', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('status', sa.String(length=32), nullable=True),
    sa.Column('diacrisis', sa.String(length=255), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['employes.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lists_sick_list_number'), 'lists', ['sick_list_number'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('last_visit', sa.DateTime(), nullable=True),
    sa.Column('employe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employe_id'], ['employes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('checkins',
    sa.Column('checkin_id', sa.Integer(), nullable=False),
    sa.Column('checkin_date', sa.Date(), nullable=True),
    sa.Column('checkin_note', sa.String(length=255), nullable=True),
    sa.Column('co_type', sa.Integer(), nullable=True),
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ),
    sa.PrimaryKeyConstraint('checkin_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checkins')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_lists_sick_list_number'), table_name='lists')
    op.drop_table('lists')
    op.drop_index(op.f('ix_patients_middle_name'), table_name='patients')
    op.drop_index(op.f('ix_patients_last_name'), table_name='patients')
    op.drop_index(op.f('ix_patients_first_name'), table_name='patients')
    op.drop_table('patients')
    op.drop_index(op.f('ix_holiday_holiday_date'), table_name='holiday')
    op.drop_table('holiday')
    op.drop_index(op.f('ix_employes_middle_name'), table_name='employes')
    op.drop_index(op.f('ix_employes_last_name'), table_name='employes')
    op.drop_index(op.f('ix_employes_first_name'), table_name='employes')
    op.drop_table('employes')
    # ### end Alembic commands ###
