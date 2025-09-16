"""add indexes for task filters

Revision ID: CHANGE_ME
Revises: <put previous revision id here>
Create Date: 2025-09-08 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "914790be166b"
down_revision: str | None = "b4171658857d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_tasks_project_status", "tasks", ["project_id", "status"])
    op.create_index("ix_tasks_project_priority", "tasks", ["project_id", "priority"])
    op.create_index("ix_tasks_project_due_at", "tasks", ["project_id", "due_at"])
    op.create_index("ix_tasks_assignee_status", "tasks", ["assignee_id", "status"])


def downgrade() -> None:
    op.drop_index("ix_tasks_assignee_status", table_name="tasks")
    op.drop_index("ix_tasks_project_due_at", table_name="tasks")
    op.drop_index("ix_tasks_project_priority", table_name="tasks")
    op.drop_index("ix_tasks_project_status", table_name="tasks")
