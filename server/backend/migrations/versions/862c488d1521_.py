"""empty message

Revision ID: 862c488d1521
Revises: 3d34e7b1b679
Create Date: 2023-06-13 14:52:35.095732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '862c488d1521'
down_revision = '3d34e7b1b679'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ligand_name', sa.TEXT(), nullable=True))

    with op.batch_alter_table('docking', schema=None) as batch_op:
        batch_op.drop_column('ligands_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('docking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ligands_name', sa.VARCHAR(length=1000), nullable=True))

    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.drop_column('ligand_name')

    # ### end Alembic commands ###
