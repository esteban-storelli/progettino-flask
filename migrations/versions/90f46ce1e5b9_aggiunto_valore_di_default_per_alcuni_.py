"""Aggiunto valore di default per alcuni campi

Revision ID: 90f46ce1e5b9
Revises: eda076ab915b
Create Date: 2025-10-10 19:42:25.149134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90f46ce1e5b9'
down_revision = 'eda076ab915b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column('high_score', server_default=sa.text("0"))
        batch_op.alter_column('number_of_plays', server_default=sa.text("0"))
        batch_op.alter_column('total_points', server_default=sa.text("0"))


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column('high_score', server_default=None)
        batch_op.alter_column('number_of_plays', server_default=None)
        batch_op.alter_column('total_points', server_default=None)
