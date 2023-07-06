"""empty message

Revision ID: e2d974039cdd
Revises: b0bd46d5e690
Create Date: 2023-07-06 15:37:00.005024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d974039cdd'
down_revision = 'b0bd46d5e690'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('docking', schema=None) as batch_op:
        batch_op.drop_column('compute_ids')

    with op.batch_alter_table('request', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_request_master_id'), ['master_id'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
        batch_op.alter_column('client_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)
        batch_op.drop_index('ix_user_username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('ix_user_username', ['username'], unique=False)
        batch_op.alter_column('client_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)

    with op.batch_alter_table('request', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_request_master_id'))

    with op.batch_alter_table('docking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('compute_ids', sa.TEXT(), nullable=True))

    # ### end Alembic commands ###