"""nome colocado

Revision ID: 161d4ece1069
Revises: 4a2cf598d5b5
Create Date: 2020-07-27 18:51:54.726926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '161d4ece1069'
down_revision = '4a2cf598d5b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usuario', 'nome',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usuario', 'nome',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###