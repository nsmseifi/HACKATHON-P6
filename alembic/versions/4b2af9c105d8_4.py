"""4

Revision ID: 4b2af9c105d8
Revises: 6bcc5e7c46a6
Create Date: 2020-06-30 17:45:01.707064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b2af9c105d8'
down_revision = '6bcc5e7c46a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_foreign_key(op.f('fk_tb_receipts_col_payee_id'), 'receipts', 'stores', ['payee_id'], ['id'])
    op.create_foreign_key(op.f('fk_tb_receipts_col_payer_id'), 'receipts', 'persons', ['payer_id'], ['id'])
        # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_tb_receipts_col_payer_id'), 'receipts', type_='foreignkey')
    op.drop_constraint(op.f('fk_tb_receipts_col_payee_id'), 'receipts', type_='foreignkey')
    # ### end Alembic commands ###