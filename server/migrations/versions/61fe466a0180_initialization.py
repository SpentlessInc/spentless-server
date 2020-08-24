"""Initialization

Revision ID: 61fe466a0180
Revises: 
Create Date: 2020-08-24 07:30:30.991063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61fe466a0180'
down_revision = None
branch_labels = None
depends_on = None

create_budget_trigger = """
    CREATE OR REPLACE FUNCTION create_budget() RETURNS TRIGGER AS
        $BODY$
            BEGIN
                INSERT INTO "budget" (user_id, year, month)
                     VALUES (
                        NEW.id,
                        EXTRACT(YEAR FROM CURRENT_TIMESTAMP),
                        EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
                     );
                RETURN NEW;
            END
        $BODY$
    LANGUAGE plpgsql;
    
    CREATE TRIGGER create_budget_trigger
        AFTER INSERT
        ON "user"
        FOR EACH ROW
    EXECUTE PROCEDURE create_budget();
"""
drop_budget_trigger = """
    DROP TRIGGER create_budget_trigger ON "user";
    DROP FUNCTION create_budget();
"""



def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mcc',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('info', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('notifications_enabled', sa.Boolean(), nullable=False),
    sa.Column('monobank_token', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('budget',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('income', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('savings', sa.SmallInteger(), nullable=True),
    sa.Column('year', sa.SmallInteger(), nullable=False),
    sa.Column('month', sa.SmallInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('budget_user_idx', 'budget', ['user_id', 'month', 'year'], unique=False)
    op.create_table('transaction',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('balance', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('cashback', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('mcc', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('info', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['mcc'], ['mcc.code'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('transaction_user_timestamp_idx', 'transaction', ['user_id', 'timestamp'], unique=False)
    op.execute(create_budget_trigger)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_budget_trigger)
    op.drop_index('transaction_user_timestamp_idx', table_name='transaction')
    op.drop_table('transaction')
    op.drop_index('budget_user_idx', table_name='budget')
    op.drop_table('budget')
    op.drop_table('user')
    op.drop_table('mcc')
    # ### end Alembic commands ###