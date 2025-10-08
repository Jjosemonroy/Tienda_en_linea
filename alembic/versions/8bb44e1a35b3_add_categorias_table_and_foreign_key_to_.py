"""Add categorias table and foreign key to productos

Revision ID: 8bb44e1a35b3
Revises: d8e35fa3dd6a
Create Date: 2025-10-02 20:56:49.757979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bb44e1a35b3'
down_revision: Union[str, Sequence[str], None] = 'd8e35fa3dd6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
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
    
    # Agregar foreign key a la tabla productos
    op.add_column('productos', sa.Column('categoria_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_productos_categoria', 'productos', 'categorias', ['categoria_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar foreign key de productos
    op.drop_constraint('fk_productos_categoria', 'productos', type_='foreignkey')
    op.drop_column('productos', 'categoria_id')
    
    # Eliminar tabla categorias
    op.drop_index(op.f('ix_categorias_nombre'), table_name='categorias')
    op.drop_index(op.f('ix_categorias_id'), table_name='categorias')
    op.drop_table('categorias')
