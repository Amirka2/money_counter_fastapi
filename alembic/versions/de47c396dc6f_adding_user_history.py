"""adding user history

Revision ID: de47c396dc6f
Revises: 9ec7ca62909f
Create Date: 2023-07-06 01:00:47.960506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de47c396dc6f'
down_revision = '9ec7ca62909f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('histories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('sum', sa.Float(), nullable=False),
    sa.Column('messages', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_histories_id'), 'histories', ['id'], unique=False)
    op.alter_column('users', 'tokens_value',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'tokens_value',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index(op.f('ix_histories_id'), table_name='histories')
    op.drop_table('histories')
    # ### end Alembic commands ###