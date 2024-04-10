"""Added all the tables

Revision ID: f49e146a50c5
Revises: 5bdab5824295
Create Date: 2024-04-08 16:21:22.349792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f49e146a50c5'
down_revision = '5bdab5824295'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vorlage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('vscodeextension', sa.String(length=255), nullable=False),
    sa.Column('installcommands', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('vorlage', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_vorlage_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_vorlage_version'), ['version'], unique=False)

    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=False),
    sa.Column('id_vorlage', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_vorlage'], ['vorlage.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_image_id_vorlage'), ['id_vorlage'], unique=False)
        batch_op.create_index(batch_op.f('ix_image_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_image_path'), ['path'], unique=True)
        batch_op.create_index(batch_op.f('ix_image_version'), ['version'], unique=False)

    op.create_table('container',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('id_volume', sa.Integer(), nullable=False),
    sa.Column('id_image', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_image'], ['image.id'], ),
    sa.ForeignKeyConstraint(['id_volume'], ['volume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('container', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_container_id_image'), ['id_image'], unique=False)
        batch_op.create_index(batch_op.f('ix_container_id_volume'), ['id_volume'], unique=False)
        batch_op.create_index(batch_op.f('ix_container_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('container', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_container_name'))
        batch_op.drop_index(batch_op.f('ix_container_id_volume'))
        batch_op.drop_index(batch_op.f('ix_container_id_image'))

    op.drop_table('container')
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_image_version'))
        batch_op.drop_index(batch_op.f('ix_image_path'))
        batch_op.drop_index(batch_op.f('ix_image_name'))
        batch_op.drop_index(batch_op.f('ix_image_id_vorlage'))

    op.drop_table('image')
    with op.batch_alter_table('vorlage', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_vorlage_version'))
        batch_op.drop_index(batch_op.f('ix_vorlage_name'))

    op.drop_table('vorlage')
    # ### end Alembic commands ###