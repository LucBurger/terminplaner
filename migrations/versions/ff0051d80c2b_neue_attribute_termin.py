"""Neue Attribute Termin

Revision ID: ff0051d80c2b
Revises: 623a0a7e2c22
Create Date: 2023-03-23 08:31:13.246489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff0051d80c2b'
down_revision = '623a0a7e2c22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('termin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('zeit', sa.DateTime(), nullable=True))
        batch_op.alter_column('datum',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('termin', schema=None) as batch_op:
        batch_op.alter_column('datum',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.drop_column('zeit')

    # ### end Alembic commands ###