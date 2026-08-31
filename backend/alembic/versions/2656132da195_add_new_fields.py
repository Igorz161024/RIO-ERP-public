"""add new fields

Revision ID: 2656132da195
Revises: 490d340f402c
Create Date: 2026-08-27 15:33:35.694527

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2656132da195'
down_revision = '490d340f402c'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'purchases',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('supplier', sa.String, nullable=False),
        sa.Column('country', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
    )

def downgrade():
    op.drop_table('purchases')
