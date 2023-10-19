"""v0.12.0.

Revision ID: 4ed9482de00d
Revises: 1a2098221d39
Create Date: 2023-09-07 16:07:57.755794

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4ed9482de00d"
down_revision = "1a2098221d39"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_cloud_run_instance_lamin_instance_id_instance",
        "cloud_run_instance",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_cloud_run_instance_lamin_instance_id_instance"),
        "cloud_run_instance",
        "instance",
        ["lamin_instance_id"],
        ["id"],
    )
    op.add_column(
        "db_user",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.add_column("db_user", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.drop_constraint("uq_db_user_instance_id", "db_user", type_="unique")
    op.create_index(
        op.f("ix_db_user_created_at"), "db_user", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_db_user_updated_at"), "db_user", ["updated_at"], unique=False
    )
    op.create_unique_constraint(
        "uq_db_user_instance_id_db_user_name",
        "db_user",
        ["instance_id", "db_user_name"],
    )
    op.create_unique_constraint(
        "uq_db_user_instance_id_name", "db_user", ["instance_id", "name"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_db_user_instance_id_name", "db_user", type_="unique")
    op.drop_constraint("uq_db_user_instance_id_db_user_name", "db_user", type_="unique")
    op.drop_index(op.f("ix_db_user_updated_at"), table_name="db_user")
    op.drop_index(op.f("ix_db_user_created_at"), table_name="db_user")
    op.create_unique_constraint(
        "uq_db_user_instance_id", "db_user", ["instance_id", "db_user_name"]
    )
    op.drop_column("db_user", "updated_at")
    op.drop_column("db_user", "created_at")
    op.drop_constraint(
        op.f("fk_cloud_run_instance_lamin_instance_id_instance"),
        "cloud_run_instance",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_cloud_run_instance_lamin_instance_id_instance",
        "cloud_run_instance",
        "instance",
        ["lamin_instance_id"],
        ["id"],
        ondelete="CASCADE",
    )
