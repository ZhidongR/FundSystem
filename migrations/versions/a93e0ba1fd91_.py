"""empty message

Revision ID: a93e0ba1fd91
Revises: ac8d4c749857
Create Date: 2022-04-16 12:28:25.301371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a93e0ba1fd91'
down_revision = 'ac8d4c749857'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_fund_hold',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('fund_id', sa.Integer(), nullable=True),
    sa.Column('fund_code', sa.String(length=64), nullable=True),
    sa.Column('fund_name', sa.String(length=64), nullable=True),
    sa.Column('hold_num', sa.Float(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('last_price', sa.Float(), nullable=True),
    sa.Column('last_time', sa.DateTime(), nullable=True),
    sa.Column('current_price', sa.Float(), nullable=True),
    sa.Column('price_time', sa.DateTime(), nullable=True),
    sa.Column('current_amount', sa.Float(), nullable=True),
    sa.Column('current_profit', sa.Float(), nullable=True),
    sa.Column('lastday_profit', sa.Float(), nullable=True),
    sa.Column('buy_price', sa.Float(), nullable=True),
    sa.Column('buy_price_time', sa.DateTime(), nullable=True),
    sa.Column('buy_amount', sa.Float(), nullable=True),
    sa.Column('buy_time', sa.DateTime(), nullable=True),
    sa.Column('sale_flag', sa.Integer(), nullable=True),
    sa.Column('deal_flag', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fund_id'], ['fund.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_fund_hold_fund_id'), 'user_fund_hold', ['fund_id'], unique=False)
    op.create_index(op.f('ix_user_fund_hold_user_id'), 'user_fund_hold', ['user_id'], unique=False)
    op.create_table('user_fund_trace',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('fund_id', sa.Integer(), nullable=True),
    sa.Column('fund_code', sa.String(length=64), nullable=True),
    sa.Column('fund_name', sa.String(length=64), nullable=True),
    sa.Column('buy_or_sale', sa.String(length=64), nullable=True),
    sa.Column('buy_money', sa.Float(), nullable=True),
    sa.Column('sale_number', sa.Float(), nullable=True),
    sa.Column('application_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('trace_price', sa.Float(), nullable=True),
    sa.Column('price_time', sa.DateTime(), nullable=True),
    sa.Column('trace_num', sa.Float(), nullable=True),
    sa.Column('trace_total', sa.Float(), nullable=True),
    sa.Column('trace_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fund_id'], ['fund.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_fund_trace_fund_id'), 'user_fund_trace', ['fund_id'], unique=False)
    op.create_index(op.f('ix_user_fund_trace_user_id'), 'user_fund_trace', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_fund_trace_user_id'), table_name='user_fund_trace')
    op.drop_index(op.f('ix_user_fund_trace_fund_id'), table_name='user_fund_trace')
    op.drop_table('user_fund_trace')
    op.drop_index(op.f('ix_user_fund_hold_user_id'), table_name='user_fund_hold')
    op.drop_index(op.f('ix_user_fund_hold_fund_id'), table_name='user_fund_hold')
    op.drop_table('user_fund_hold')
    # ### end Alembic commands ###
