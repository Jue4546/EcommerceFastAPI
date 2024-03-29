"""update address table

Revision ID: 357772061a7d
Revises: b6cdbb072979
Create Date: 2024-01-12 09:31:07.835901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '357772061a7d'
down_revision: Union[str, None] = 'b6cdbb072979'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('district', sa.String(length=100), nullable=True, comment='区'))
    op.add_column('address', sa.Column('detail', sa.String(length=255), nullable=True, comment='详细地址'))
    op.create_index(op.f('ix_address_city'), 'address', ['city'], unique=False)
    op.create_index(op.f('ix_address_detail'), 'address', ['detail'], unique=False)
    op.create_index(op.f('ix_address_district'), 'address', ['district'], unique=False)
    op.create_index(op.f('ix_address_postal_code'), 'address', ['postal_code'], unique=False)
    op.create_index(op.f('ix_address_province_or_state'), 'address', ['province_or_state'], unique=False)
    op.create_index(op.f('ix_address_street'), 'address', ['street'], unique=False)
    op.create_index(op.f('ix_address_user_id'), 'address', ['user_id'], unique=False)
    op.drop_column('address', 'country')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('country', sa.VARCHAR(length=100), autoincrement=False, nullable=True, comment='国家'))
    op.drop_index(op.f('ix_address_user_id'), table_name='address')
    op.drop_index(op.f('ix_address_street'), table_name='address')
    op.drop_index(op.f('ix_address_province_or_state'), table_name='address')
    op.drop_index(op.f('ix_address_postal_code'), table_name='address')
    op.drop_index(op.f('ix_address_district'), table_name='address')
    op.drop_index(op.f('ix_address_detail'), table_name='address')
    op.drop_index(op.f('ix_address_city'), table_name='address')
    op.drop_column('address', 'detail')
    op.drop_column('address', 'district')
    # ### end Alembic commands ###
