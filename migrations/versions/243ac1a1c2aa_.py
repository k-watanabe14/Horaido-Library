"""empty message

Revision ID: 243ac1a1c2aa
Revises: 4ca35f594102
Create Date: 2021-02-11 09:37:35.423176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243ac1a1c2aa'
down_revision = '4ca35f594102'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auth_user', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auth_user', 'admin')
    # ### end Alembic commands ###
