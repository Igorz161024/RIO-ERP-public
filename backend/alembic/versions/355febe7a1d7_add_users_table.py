"""add users table

Revision ID: 355febe7a1d7
Revises: b7f9f9dec21f
Create Date: 2026-09-24 20:30:33.192635
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '355febe7a1d7'
down_revision = 'b7f9f9dec21f'
branch_labels = None
depends_on = None


def upgrade():
    # створення таблиці users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('email', sa.String(length=100), nullable=True, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('refresh_token', sa.String(length=255), nullable=True),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # створення таблиці entry_lines
    op.create_table(
        'entry_lines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('journal_id', sa.Integer(), nullable=False),
        sa.Column('account', sa.String(), nullable=False),
        sa.Column('debit', sa.Float(), nullable=True),
        sa.Column('credit', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['journal_id'], ['journal.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entry_lines_id'), 'entry_lines', ['id'], unique=False)

    # зміни у finance
    op.alter_column('finance', 'account',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # зміни у journal
    op.drop_column('journal', 'comment')


def downgrade():
    # відкат users
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    # відкат entry_lines
    op.drop_index(op.f('ix_entry_lines_id'), table_name='entry_lines')
    op.drop_table('entry_lines')

    # відкат finance
    op.alter_column('finance', 'account',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # відкат journal
    op.add_column('journal', sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=True))
