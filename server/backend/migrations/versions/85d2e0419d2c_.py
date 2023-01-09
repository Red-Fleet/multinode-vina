"""empty message

Revision ID: 85d2e0419d2c
Revises: 905af2fda2e4
Create Date: 2023-01-09 17:12:34.008781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d2e0419d2c'
down_revision = '905af2fda2e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target_name', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('ligands_name', sa.String(length=1000), nullable=True))
        batch_op.alter_column('error',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('compute', schema=None) as batch_op:
        batch_op.alter_column('error',
               existing_type=sa.TEXT(),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
        batch_op.drop_column('ligands_name')
        batch_op.drop_column('target_name')

    # ### end Alembic commands ###
