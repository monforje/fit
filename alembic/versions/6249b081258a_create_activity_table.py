"""create activity table

Revision ID: 6249b081258a
Revises: 
Create Date: 2026-01-15 17:00:47.031807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6249b081258a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "activity",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("steps", sa.Integer(), nullable=False),
        sa.Column("calories", sa.Integer(), nullable=False),
        sa.Column("activity_type", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("activity")
