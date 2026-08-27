"""baseline schema

Revision ID: 490d340f402c
Revises: 
Create Date: 2026-08-27 15:30:43.502276
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '490d340f402c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Це baseline ревізія — ми нічого не створюємо,
    # просто фіксуємо поточний стан бази як стартову точку.
    pass


def downgrade():
    # Аналогічно, нічого не видаляємо.
    pass
