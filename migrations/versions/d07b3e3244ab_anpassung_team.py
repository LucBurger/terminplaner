"""ANpassung TEAM

Revision ID: d07b3e3244ab
Revises: a0bf7b2fc5e5
Create Date: 2023-03-23 10:24:54.024609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd07b3e3244ab'
down_revision = 'a0bf7b2fc5e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('beschreibung', sa.String(length=140), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_column('beschreibung')

    # ### end Alembic commands ###
