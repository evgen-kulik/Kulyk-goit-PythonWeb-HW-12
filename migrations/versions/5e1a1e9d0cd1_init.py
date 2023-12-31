"""Init

Revision ID: 5e1a1e9d0cd1
Revises: b9dcb93948be
Create Date: 2023-09-11 17:11:49.132546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e1a1e9d0cd1"
down_revision: Union[str, None] = "b9dcb93948be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users_info", sa.Column("avatar", sa.String(length=255), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users_info", "avatar")
    # ### end Alembic commands ###
