"""create_tables

Revision ID: ca42297a1d70
Revises: 
Create Date: 2025-04-10 22:19:06.736964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca42297a1d70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedbacks',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('feedback_text', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classification',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('sentiment', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('feedbacks_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['feedbacks_id'], ['feedbacks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('classification')
    op.drop_table('feedbacks')
    # ### end Alembic commands ###
