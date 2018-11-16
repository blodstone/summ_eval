"""empty message

Revision ID: c1ddc179f7d1
Revises: 
Create Date: 2018-11-16 18:24:47.405165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1ddc179f7d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('document',
    sa.Column('doc_id', sa.String(length=25), nullable=False),
    sa.Column('doc_json', sa.Text(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('doc_id')
    )
    op.create_table('doc_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('pro_id', sa.Integer(), nullable=False),
    sa.Column('numberOfAnnotations', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doc_id'], ['document.doc_id'], ),
    sa.ForeignKeyConstraint(['pro_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('finished_at', sa.DateTime(), nullable=True),
    sa.Column('result_json', sa.Text(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['status_id'], ['doc_status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_table('doc_status')
    op.drop_table('document')
    op.drop_table('user')
    op.drop_table('project')
    op.drop_table('dataset')
    # ### end Alembic commands ###
