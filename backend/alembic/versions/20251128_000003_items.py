"""
items tables

Create Date: 2025-11-28
"""

import sqlalchemy as sa

from alembic import op

revision = "20251128_000003"
down_revision = "20251128_000002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "seller_id",
            sa.String(length=36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("brand", sa.String(length=100), nullable=True),
        sa.Column("size", sa.String(length=50), nullable=True),
        sa.Column("condition", sa.String(length=32), nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("location_city", sa.String(length=100), nullable=True),
        sa.Column("location_country", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("price_cents >= 0", name="ck_items_price_nonnegative"),
    )
    op.create_index("ix_items_seller_id", "items", ["seller_id"])
    op.create_index("ix_items_status", "items", ["status"])
    op.create_index("ix_items_created_at", "items", ["created_at"])

    op.create_table(
        "item_images",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "item_id",
            sa.String(length=36),
            sa.ForeignKey("items.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("original_key", sa.Text(), nullable=False),
        sa.Column("thumb_key", sa.Text(), nullable=True),
        sa.Column("medium_key", sa.Text(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_item_images_item_id", "item_images", ["item_id"])


def downgrade() -> None:
    op.drop_index("ix_item_images_item_id", table_name="item_images")
    op.drop_table("item_images")
    op.drop_index("ix_items_created_at", table_name="items")
    op.drop_index("ix_items_status", table_name="items")
    op.drop_index("ix_items_seller_id", table_name="items")
    op.drop_table("items")
