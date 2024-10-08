"""Adding Tag to QUIZ

Revision ID: 964b05113e1a
Revises: da822d43349f
Create Date: 2021-01-07 16:43:02.130218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '964b05113e1a'
down_revision = 'da822d43349f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('python_quiz', sa.Column('tag', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('python_quiz', 'tag')
    # ### end Alembic commands ###
