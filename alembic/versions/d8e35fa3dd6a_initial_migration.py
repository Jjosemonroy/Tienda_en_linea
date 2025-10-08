"""Initial migration

Revision ID: d8e35fa3dd6a
Revises: 
Create Date: 2025-10-02 20:56:24.400251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8e35fa3dd6a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Crear tabla usuarios
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=True),
        sa.Column('correo', sa.String(length=100), nullable=True),
        sa.Column('contraseña', sa.String(length=255), nullable=True),
        sa.Column('rol', sa.Enum('cliente', 'admin', name='rol'), nullable=True),
        sa.Column('estado', sa.Enum('activo', 'inactivo', name='estado'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)
    op.create_index(op.f('ix_usuarios_correo'), 'usuarios', ['correo'], unique=True)

    # Crear tabla categorias
    op.create_table('categorias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=True),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=True),
        sa.Column('fecha_creacion', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorias_id'), 'categorias', ['id'], unique=False)
    op.create_index(op.f('ix_categorias_nombre'), 'categorias', ['nombre'], unique=True)

    # Crear tabla productos
    op.create_table('productos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=True),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('precio', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('stock', sa.Integer(), nullable=True),
        sa.Column('imagen', sa.String(length=255), nullable=True),
        sa.Column('categoria_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_productos_id'), 'productos', ['id'], unique=False)

    # Crear tabla carrito
    op.create_table('carrito',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=True),
        sa.Column('producto_id', sa.Integer(), nullable=True),
        sa.Column('cantidad', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_carrito_id'), 'carrito', ['id'], unique=False)

    # Crear tabla ventas
    op.create_table('ventas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=True),
        sa.Column('fecha', sa.TIMESTAMP(), nullable=True),
        sa.Column('total', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ventas_id'), 'ventas', ['id'], unique=False)

    # Crear tabla detalle_venta
    op.create_table('detalle_venta',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('venta_id', sa.Integer(), nullable=True),
        sa.Column('producto_id', sa.Integer(), nullable=True),
        sa.Column('cantidad', sa.Integer(), nullable=True),
        sa.Column('precio_unitario', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
        sa.ForeignKeyConstraint(['venta_id'], ['ventas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_detalle_venta_id'), 'detalle_venta', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar tablas en orden inverso
    op.drop_index(op.f('ix_detalle_venta_id'), table_name='detalle_venta')
    op.drop_table('detalle_venta')
    
    op.drop_index(op.f('ix_ventas_id'), table_name='ventas')
    op.drop_table('ventas')
    
    op.drop_index(op.f('ix_carrito_id'), table_name='carrito')
    op.drop_table('carrito')
    
    op.drop_index(op.f('ix_productos_id'), table_name='productos')
    op.drop_table('productos')
    
    op.drop_index(op.f('ix_categorias_nombre'), table_name='categorias')
    op.drop_index(op.f('ix_categorias_id'), table_name='categorias')
    op.drop_table('categorias')
    
    op.drop_index(op.f('ix_usuarios_correo'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_table('usuarios')
