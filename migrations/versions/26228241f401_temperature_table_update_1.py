"""temperature table update 1

Revision ID: 26228241f401
Revises: 
Create Date: 2018-04-30 23:48:21.651887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26228241f401'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temp')
    # ### end Alembic commands ###
