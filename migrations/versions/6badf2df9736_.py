"""empty message

Revision ID: 6badf2df9736
Revises: 51db54ce93bd
Create Date: 2018-12-09 17:03:32.506809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6badf2df9736'
down_revision = '51db54ce93bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('sanity_answer_2', sa.Boolean(), nullable=True))
    op.add_column('document', sa.Column('sanity_statement_2', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'sanity_statement_2')
    op.drop_column('document', 'sanity_answer_2')
    # ### end Alembic commands ###