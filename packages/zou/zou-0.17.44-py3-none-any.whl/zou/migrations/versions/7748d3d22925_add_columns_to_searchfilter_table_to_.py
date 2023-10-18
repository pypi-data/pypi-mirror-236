"""Add columns to searchFilter table to create search filters groups

Revision ID: 7748d3d22925
Revises: ae0127f2fc56
Create Date: 2023-09-14 17:50:53.903284

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "7748d3d22925"
down_revision = "ae0127f2fc56"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "search_filter_group",
        sa.Column("list_type", sa.String(length=80), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("color", sa.String(length=8), nullable=False),
        sa.Column(
            "person_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=True,
        ),
        sa.Column(
            "project_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=True,
        ),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["person.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("search_filter_group", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_search_filter_group_list_type"),
            ["list_type"],
            unique=False,
        )

    with op.batch_alter_table("search_filter", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "search_filter_group_id",
                sqlalchemy_utils.types.uuid.UUIDType(binary=False),
                default=uuid.uuid4,
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            None, "search_filter_group", ["search_filter_group_id"], ["id"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("search_filter", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("search_filter_group_id")

    with op.batch_alter_table("search_filter_group", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_search_filter_group_list_type"))

    op.drop_table("search_filter_group")
    # ### end Alembic commands ###
