"""create users table with role and refresh_token

Revision ID: b7f9f9dec21f
Revises: 60a3f0ed5bba
Create Date: 2026-09-17 11:54:21.755513
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b7f9f9dec21f'
down_revision = '60a3f0ed5bba'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(length=100), nullable=False, unique=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=True),
        sa.Column("refresh_token", sa.String(length=255), nullable=True),
    )

def downgrade():
    op.drop_table("users")
