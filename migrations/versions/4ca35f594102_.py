"""empty message

Revision ID: 4ca35f594102
Revises: ff72b90028ed
Create Date: 2021-02-10 23:27:48.097921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ca35f594102'
down_revision = 'ff72b90028ed'
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