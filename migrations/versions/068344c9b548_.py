"""empty message

Revision ID: 068344c9b548
Revises: 786fde9117e2
Create Date: 2021-01-31 13:02:46.356066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '068344c9b548'
down_revision = '786fde9117e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.String(length=128), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('author', sa.String(length=128), nullable=True),
    sa.Column('publisher_name', sa.String(length=128), nullable=True),
    sa.Column('sales_date', sa.String(length=128), nullable=True),
    sa.Column('image_url', sa.String(length=128), nullable=True),
    sa.Column('borrower_id', sa.Integer(), nullable=True),
    sa.Column('checkout_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['borrower_id'], ['auth_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rental_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('checkout_date', sa.DateTime(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['auth_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_maps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_maps')
    op.drop_table('rental_history')
    op.drop_table('book')
    # ### end Alembic commands ###
