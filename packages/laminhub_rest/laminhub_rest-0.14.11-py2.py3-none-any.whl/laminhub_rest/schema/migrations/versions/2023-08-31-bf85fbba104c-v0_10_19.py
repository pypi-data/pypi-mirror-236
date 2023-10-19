"""v0.10.19.

Revision ID: bf85fbba104c
Revises: 65ba7fa72764
Create Date: 2023-08-31 12:10:43.941449

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

from laminhub_rest.schema.migrations.function._2023_08_31_bf85fbba104c_v0_10_19 import (
    sql_function_is_laminapp_admin,
)
from laminhub_rest.schema.migrations.rls._2023_08_31_bf85fbba104c_v0_10_19 import (
    sql_drop_rls_laminapp_admin_instance,
    sql_rls_laminapp_admin_instance,
)

# revision identifiers, used by Alembic.
revision = "bf85fbba104c"
down_revision = "65ba7fa72764"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sql_function_is_laminapp_admin)
    op.execute(sql_rls_laminapp_admin_instance)


def downgrade() -> None:
    op.execute(sql_drop_rls_laminapp_admin_instance)
