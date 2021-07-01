"""Students and courses

Revision ID: 946c3ed59f31
Revises: 7ff5c096eb46
Create Date: 2021-06-30 20:29:00.507628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '946c3ed59f31'
down_revision = '7ff5c096eb46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    # ### end Alembic commands ###