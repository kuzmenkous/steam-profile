"""Trade model

Revision ID: 8e1bd8293a2b
Revises: f77ae239df70
Create Date: 2025-03-02 19:34:53.242034

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e1bd8293a2b"
down_revision: Union[str, None] = "f77ae239df70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "trade",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("partner", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trade_partner"), "trade", ["partner"], unique=False)
    op.create_index(op.f("ix_trade_token"), "trade", ["token"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_trade_token"), table_name="trade")
    op.drop_index(op.f("ix_trade_partner"), table_name="trade")
    op.drop_table("trade")
    # ### end Alembic commands ###
