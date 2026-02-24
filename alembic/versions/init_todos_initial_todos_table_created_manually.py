"""Initial todos table (created manually)

Revision ID: init_todos
Revises: init_todos
Create Date: 2026-02-24 10:18:16.815510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'init_todos'
down_revision: Union[str, Sequence[str], None] = 'init_todos'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
