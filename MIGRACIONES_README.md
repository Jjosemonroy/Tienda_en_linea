# Guía de Migraciones con Alembic

## Configuración Completada

He configurado Alembic para tu proyecto de tienda en línea. Aquí está lo que se ha creado:

### Archivos de Configuración
- `alembic.ini` - Configuración principal de Alembic
- `alembic/env.py` - Configuración del entorno de migraciones
- `alembic/versions/` - Directorio con las migraciones

### Migraciones Creadas

1. **Migración Inicial** (`d8e35fa3dd6a_initial_migration.py`)
   - Crea todas las tablas: usuarios, categorias, productos, carrito, ventas, detalle_venta
   - Incluye todas las foreign keys y índices

2. **Migración de Categorías** (`8bb44e1a35b3_add_categorias_table_and_foreign_key_to_.py`)
   - Agrega la tabla categorias
   - Agrega la foreign key categoria_id a la tabla productos

## Configuración de Base de Datos

**IMPORTANTE**: Necesitas crear un archivo `.env` en la raíz del proyecto con las credenciales correctas de tu base de datos:

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tienda_online
```

## Comandos de Migración

### 1. Aplicar Migraciones
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una migración específica
alembic upgrade d8e35fa3dd6a
```

### 2. Revertir Migraciones
```bash
# Revertir a la migración anterior
alembic downgrade -1

# Revertir a una migración específica
alembic downgrade d8e35fa3dd6a

# Revertir todas las migraciones
alembic downgrade base
```

### 3. Ver Estado de Migraciones
```bash
# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current

# Ver migraciones pendientes
alembic show head
```

### 4. Crear Nuevas Migraciones
```bash
# Crear migración automática (detecta cambios en modelos)
alembic revision --autogenerate -m "Descripción del cambio"

# Crear migración vacía (para cambios manuales)
alembic revision -m "Descripción del cambio"
```

## Estructura de las Tablas

### Tabla `usuarios`
- id (PK)
- nombre
- correo (único)
- contraseña
- rol (enum: cliente, admin)
- estado (enum: activo, inactivo)

### Tabla `categorias`
- id (PK)
- nombre (único)
- descripcion
- activo (boolean)
- fecha_creacion

### Tabla `productos`
- id (PK)
- nombre
- descripcion
- precio (decimal 10,2)
- stock
- imagen
- categoria_id (FK a categorias)

### Tabla `carrito`
- id (PK)
- usuario_id (FK a usuarios)
- producto_id (FK a productos)
- cantidad

### Tabla `ventas`
- id (PK)
- usuario_id (FK a usuarios)
- fecha
- total (decimal 10,2)

### Tabla `detalle_venta`
- id (PK)
- venta_id (FK a ventas)
- producto_id (FK a productos)
- cantidad
- precio_unitario (decimal 10,2)

## Próximos Pasos

1. **Configura las credenciales** en el archivo `.env`
2. **Aplica las migraciones** con `alembic upgrade head`
3. **Verifica** que las tablas se crearon correctamente
4. **Usa las migraciones** para futuros cambios en la base de datos

## Notas Importantes

- Siempre revisa las migraciones antes de aplicarlas
- Haz backup de tu base de datos antes de aplicar migraciones en producción
- Las migraciones se aplican en orden secuencial
- Puedes editar las migraciones manualmente si es necesario
