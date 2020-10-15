"""empty message

Revision ID: 9dde4ea9e59d
Revises: 6ced271d07c0
Create Date: 2020-10-15 22:21:02.733355

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9dde4ea9e59d'
down_revision = '6ced271d07c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('date_registration', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personal_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('patronymic', sa.String(length=100), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('geolocation', sa.String(length=200), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_user'),
    sa.UniqueConstraint('phone_number')
    )
    op.drop_table('user')
    op.drop_constraint('announcement_user_fkey', 'announcement', type_='foreignkey')
    op.create_foreign_key(None, 'announcement', 'users', ['user'], ['id'])
    op.drop_constraint('want_user_fkey', 'want', type_='foreignkey')
    op.create_foreign_key(None, 'want', 'users', ['user'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'want', type_='foreignkey')
    op.create_foreign_key('want_user_fkey', 'want', 'user', ['user'], ['id'])
    op.drop_constraint(None, 'announcement', type_='foreignkey')
    op.create_foreign_key('announcement_user_fkey', 'announcement', 'user', ['user'], ['id'])
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('date_registration', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('token', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.drop_table('personal_area')
    op.drop_table('users')
    # ### end Alembic commands ###
