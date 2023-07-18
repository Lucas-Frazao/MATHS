"""empty message

Revision ID: 99ad96fef46f
Revises: 883fd50b0fbe
Create Date: 2023-07-17 17:04:39.335046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99ad96fef46f'
down_revision = '883fd50b0fbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index('ix_event_date')
        batch_op.drop_index('ix_event_event_name')

    op.drop_table('event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('event_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('description', sa.VARCHAR(length=140), nullable=True),
    sa.Column('date', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index('ix_event_event_name', ['event_name'], unique=False)
        batch_op.create_index('ix_event_date', ['date'], unique=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    # ### end Alembic commands ###
