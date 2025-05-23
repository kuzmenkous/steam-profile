"""Profile model added invite_link_path column

Revision ID: f77ae239df70
Revises: 496659b6047f
Create Date: 2025-02-28 19:27:07.360545

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f77ae239df70"
down_revision: Union[str, None] = "496659b6047f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("profile", sa.Column("invite_link_path", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profile", "invite_link_path")
    # ### end Alembic commands ###
