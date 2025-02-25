"""Updating database schema.

Revision ID: 4a224c752697
Revises: 4aa7448fb436
Create Date: 2025-01-03 12:10:55.444935

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4a224c752697'
down_revision = '4aa7448fb436'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registro_egresado', schema=None) as batch_op:
        batch_op.alter_column('ag',
               existing_type=mysql.DECIMAL(precision=10, scale=3),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('aa',
               existing_type=mysql.DECIMAL(precision=10, scale=3),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('pg',
               existing_type=mysql.DECIMAL(precision=10, scale=3),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('pa',
               existing_type=mysql.DECIMAL(precision=10, scale=3),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('rendimiento',
               existing_type=mysql.DECIMAL(precision=10, scale=2),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('fecha_grado',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.alter_column('cod_carrera',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('cod_periodo',
               existing_type=mysql.VARCHAR(length=5),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('num_periodo',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=10),
               existing_nullable=True)
        batch_op.alter_column('cedula',
               existing_type=mysql.VARCHAR(charset='latin1', collation='latin1_swedish_ci', length=10),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.alter_column('nombre',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               existing_nullable=True)

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('clave',
               existing_type=mysql.VARCHAR(length=15),
               type_=sa.String(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('clave',
               existing_type=sa.String(length=128),
               type_=mysql.VARCHAR(length=15),
               existing_nullable=True)

    with op.batch_alter_table('registro_egresado', schema=None) as batch_op:
        batch_op.alter_column('nombre',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.alter_column('cedula',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(charset='latin1', collation='latin1_swedish_ci', length=10),
               existing_nullable=True)
        batch_op.alter_column('num_periodo',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('cod_periodo',
               existing_type=sa.String(length=10),
               type_=mysql.VARCHAR(length=5),
               existing_nullable=True)
        batch_op.alter_column('cod_carrera',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('fecha_grado',
               existing_type=sa.Date(),
               type_=mysql.VARCHAR(length=10),
               existing_nullable=True)
        batch_op.alter_column('rendimiento',
               existing_type=sa.Float(),
               type_=mysql.DECIMAL(precision=10, scale=2),
               existing_nullable=True)
        batch_op.alter_column('pa',
               existing_type=sa.String(length=10),
               type_=mysql.DECIMAL(precision=10, scale=3),
               existing_nullable=True)
        batch_op.alter_column('pg',
               existing_type=sa.String(length=10),
               type_=mysql.DECIMAL(precision=10, scale=3),
               existing_nullable=True)
        batch_op.alter_column('aa',
               existing_type=sa.String(length=10),
               type_=mysql.DECIMAL(precision=10, scale=3),
               existing_nullable=True)
        batch_op.alter_column('ag',
               existing_type=sa.String(length=10),
               type_=mysql.DECIMAL(precision=10, scale=3),
               existing_nullable=True)

    # ### end Alembic commands ###
