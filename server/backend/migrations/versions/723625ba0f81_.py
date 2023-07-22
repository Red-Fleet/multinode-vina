"""empty message

Revision ID: 723625ba0f81
Revises: 751eceddef9b
Create Date: 2023-07-23 03:29:45.663068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '723625ba0f81'
down_revision = '751eceddef9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('worker_notification', schema=None) as batch_op:
        batch_op.alter_column('docking_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('worker_notification', schema=None) as batch_op:
        batch_op.alter_column('docking_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)

    # ### end Alembic commands ###
