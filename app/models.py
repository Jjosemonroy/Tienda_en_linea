from cgitb import text
from re import escape
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DECIMAL, TIMESTAMP, Boolean, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100), unique=True, index=True)
    contraseña = Column(String(255))
    rol = Column(Enum('cliente', 'admin'), default='cliente')
    estado = Column(Enum('activo', 'inactivo'), default='activo')

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP)

    # Relación con productos
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2))
    stock = Column(Integer)
    imagen = Column(String(255))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    # Relación con categoría
    categoria = relationship("Categoria", back_populates="productos")

class Carrito(Base):
    __tablename__ = "carrito"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(TIMESTAMP)
    total = Column(DECIMAL(10, 2))

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(10, 2))

class MetodoPago(Base):
    __tablename__ = "metodo_pago"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)
    descripcion = Column(Text)
    tipo = Column(Enum('tarjeta', 'transferencia', 'efectivo', 'paypal'), default='tarjeta')
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP)

class EstadoTransaccion(Base):
    __tablename__ = "estados_transaccion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)
    descripcion = Column(Text)

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    metodo_pago_id = Column(Integer, ForeignKey("metodo_pago.id"))
    estado_id = Column(Integer, ForeignKey("estados_transaccion.id"))
    referencia = Column(String(255), unique=True, index=True)
    monto = Column(DECIMAL(10, 2))
    datos_pago = Column(JSON) # Datos de la transacción
    fecha_creacion = Column(TIMESTAMP)
    fecha_actualizacion = Column(TIMESTAMP)

class DireccionEnvio(Base):
    __tablename__ = "direccion_envio"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    alias = Column(String(50))
    nombre_completo = Column(String(200))
    direccion = Column(Text)
    ciudad = Column(String(100))
    codigo_postal = Column(String(20))
    telefono = Column(String(20))
    es_principal = Column(Boolean, default=False)
    fecha_creacion = Column(TIMESTAMP)
