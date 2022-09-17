"""connect db

Revision ID: ffc124390ce9
Revises: 
Create Date: 2021-07-22 18:05:03.176222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffc124390ce9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    op.create_index(op.f('ix_admin_username'), 'admin', ['username'], unique=False)
    op.create_table('newlead',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('fullname', sa.String(length=64), nullable=True),
    sa.Column('mobile', sa.String(length=64), nullable=True),
    sa.Column('leadfrom', sa.String(length=64), nullable=True),
    sa.Column('handleby', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_newlead_email'), 'newlead', ['email'], unique=True)
    op.create_index(op.f('ix_newlead_fullname'), 'newlead', ['fullname'], unique=False)
    op.create_index(op.f('ix_newlead_mobile'), 'newlead', ['mobile'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_newlead_mobile'), table_name='newlead')
    op.drop_index(op.f('ix_newlead_fullname'), table_name='newlead')
    op.drop_index(op.f('ix_newlead_email'), table_name='newlead')
    op.drop_table('newlead')
    op.drop_index(op.f('ix_admin_username'), table_name='admin')
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###