"""Add validation status column to preview files

Revision ID: 398150912a3f
Revises: 3b0d1321079e
Create Date: 2021-11-09 00:07:04.543076

"""
from zou.app.models.preview_file import VALIDATION_STATUSES
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "398150912a3f"
down_revision = "3b0d1321079e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "preview_file",
        sa.Column(
            "validation_status",
            sqlalchemy_utils.types.choice.ChoiceType(VALIDATION_STATUSES),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("preview_file", "validation_status")
    # ### end Alembic commands ###
