"""create phone number column for user column

Revision ID: a99e131f01d3
Revises: 
Create Date: 2025-06-22 19:54:16.558666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a99e131f01d3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
