"""Create users, projects, tasks and notifications."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("role", sa.String(20), nullable=False, server_default="user"), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("projects", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("description", sa.Text()), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_projects_owner_id", "projects", ["owner_id"])
    op.create_table("tasks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(160), nullable=False), sa.Column("description", sa.Text()), sa.Column("status", sa.String(20), nullable=False, server_default="todo"), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_tasks_project_id", "tasks", ["project_id"])
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("message", sa.String(500), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])

def downgrade():
    op.drop_index("ix_notifications_user_id", table_name="notifications"); op.drop_table("notifications")
    op.drop_index("ix_tasks_project_id", table_name="tasks"); op.drop_table("tasks")
    op.drop_index("ix_projects_owner_id", table_name="projects"); op.drop_table("projects")
    op.drop_index("ix_users_email", table_name="users"); op.drop_table("users")
