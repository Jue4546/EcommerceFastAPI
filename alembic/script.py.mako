"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.services.auth_service import get_password_hash
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
    admin_password_hash = get_password_hash("Pa$sW0rd")
    op.execute(
        f"""
        INSERT INTO users (username, email, password, is_admin, is_disabled, registration_time)
        VALUES ('admin', 'admin@dbcd.oky.wiki', '{admin_password_hash}', true, false, now())
        """
    )


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
