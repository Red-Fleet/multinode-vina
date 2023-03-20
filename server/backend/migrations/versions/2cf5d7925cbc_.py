"""empty message

Revision ID: 2cf5d7925cbc
Revises: 4ad1369f8198
Create Date: 2023-03-20 11:13:55.030137

"""
from alembic import op
import sqlalchemy as sa
from app.models.docking import ListType

# revision identifiers, used by Alembic.
revision = '2cf5d7925cbc'
down_revision = '4ad1369f8198'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ligand', sa.TEXT(), nullable=True))
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.Enum('COMPUTED', 'NOT_COMPUTED', 'COMPUTING', 'ERROR', name='computestate'),
               existing_nullable=True)
        batch_op.drop_column('worker_id')
        batch_op.drop_column('target')
        batch_op.drop_column('master_id')
        batch_op.drop_column('ligands')
        batch_op.drop_column('ligands_name')
        batch_op.drop_column('target_name')

    with op.batch_alter_table('docking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('compute_ids', ListType(), nullable=True))
        batch_op.drop_column('ligand_ids')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('docking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ligand_ids', sa.TEXT(), nullable=True))
        batch_op.drop_column('compute_ids')

    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_name', sa.VARCHAR(length=1000), nullable=True))
        batch_op.add_column(sa.Column('ligands_name', sa.VARCHAR(length=1000), nullable=True))
        batch_op.add_column(sa.Column('ligands', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('master_id', sa.VARCHAR(length=36), nullable=False))
        batch_op.add_column(sa.Column('target', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('worker_id', sa.VARCHAR(length=36), nullable=False))
        batch_op.alter_column('state',
               existing_type=sa.Enum('COMPUTED', 'NOT_COMPUTED', 'COMPUTING', 'ERROR', name='computestate'),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)
        batch_op.drop_column('ligand')

    # ### end Alembic commands ###
