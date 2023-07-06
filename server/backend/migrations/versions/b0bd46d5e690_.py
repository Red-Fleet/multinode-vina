"""empty message

Revision ID: b0bd46d5e690
Revises: 862c488d1521
Create Date: 2023-06-13 15:34:08.475489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0bd46d5e690'
down_revision = '862c488d1521'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('compute',
    sa.Column('compute_id', sa.String(length=36), nullable=False),
    sa.Column('docking_id', sa.String(length=36), nullable=True),
    sa.Column('result', sa.TEXT(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Enum('COMPUTED', 'NOT_COMPUTED', 'COMPUTING', 'ERROR', name='computestate'), nullable=True),
    sa.Column('error', sa.TEXT(), nullable=True),
    sa.Column('ligand', sa.TEXT(), nullable=True),
    sa.Column('ligand_name', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('compute_id')
    )
    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_compute_docking_id'), ['docking_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_compute_docking_id'))

    op.drop_table('compute')
    # ### end Alembic commands ###