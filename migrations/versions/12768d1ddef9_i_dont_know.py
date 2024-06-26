"""I dont know

Revision ID: 12768d1ddef9
Revises: dc97e6153938
Create Date: 2024-04-11 11:45:33.380811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12768d1ddef9'
down_revision = 'dc97e6153938'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('docker_id', sa.String(length=255), nullable=False))
        batch_op.drop_index('ix_image_name')
        batch_op.create_index(batch_op.f('ix_image_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_image_docker_id'), ['docker_id'], unique=False)

    with op.batch_alter_table('vorlage', schema=None) as batch_op:
        batch_op.drop_index('ix_vorlage_name')
        batch_op.create_index(batch_op.f('ix_vorlage_name'), ['name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vorlage', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_vorlage_name'))
        batch_op.create_index('ix_vorlage_name', ['name'], unique=1)

    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_image_docker_id'))
        batch_op.drop_index(batch_op.f('ix_image_name'))
        batch_op.create_index('ix_image_name', ['name'], unique=1)
        batch_op.drop_column('docker_id')

    # ### end Alembic commands ###
