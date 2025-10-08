from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

# Schemas para Categorías
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas para Productos (actualizados)
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int
    imagen: Optional[str] = None
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    categoria: Optional[CategoriaResponse] = None

    class Config:
        from_attributes = True

# Schemas para Usuarios
class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    rol: str = 'cliente'
    estado: str = 'activo'

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None

class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str

# Schemas para Carrito
class CarritoBase(BaseModel):
    producto_id: int
    cantidad: int

class CarritoCreate(CarritoBase):
    pass

class CarritoResponse(CarritoBase):
    id: int
    usuario_id: int
    producto: ProductoResponse

    class Config:
        from_attributes = True

# Schemas para Ventas
class VentaBase(BaseModel):
    total: Decimal

class VentaCreate(VentaBase):
    pass

class VentaResponse(VentaBase):
    id: int
    usuario_id: int
    fecha: datetime

    class Config:
        from_attributes = True

# Schemas para Detalle de Venta
class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(DetalleVentaBase):
    id: int
    venta_id: int
    producto: ProductoResponse

    class Config:
        from_attributes = True 