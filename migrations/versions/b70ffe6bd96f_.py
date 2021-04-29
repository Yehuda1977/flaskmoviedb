"""empty message

Revision ID: b70ffe6bd96f
Revises: a195e09ced9d
Create Date: 2021-04-28 12:53:07.725087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70ffe6bd96f'
down_revision = 'a195e09ced9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'movie_id')
    op.alter_column('movie', 'title',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movie', 'title',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.add_column('comment', sa.Column('movie_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'comment', 'movie', ['movie_id'], ['id'])
    # ### end Alembic commands ###