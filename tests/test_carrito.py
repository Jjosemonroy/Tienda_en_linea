import pytest
import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import Usuario, Categoria, Producto, CarritoItem

# Configurar base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_carrito.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestCarrito:
    """Pruebas unitarias para el módulo de carrito de compras"""
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial para todas las pruebas"""
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        
        # Crear datos de prueba
        db = TestingSessionLocal()
        
        # Crear usuario cliente
        cliente = Usuario(
            id=1,
            nombre="Cliente Test",
            correo="cliente@test.com",
            contraseña="hashed_password",
            rol="cliente",
            estado="activo"
        )
        db.add(cliente)
        
        # Crear categoría
        categoria = Categoria(
            id=1,
            nombre="Electrónicos",
            descripcion="Productos electrónicos",
            activo=True
        )
        db.add(categoria)
        
        # Crear productos de prueba
        producto1 = Producto(
            id=1,
            nombre="Smartphone",
            descripcion="Teléfono inteligente",
            precio=999.99,
            stock=10,
            categoria_id=1,
            imagen="/static/imagenes/smartphone.jpg"
        )
        db.add(producto1)
        
        producto2 = Producto(
            id=2,
            nombre="Laptop",
            descripcion="Computadora portátil",
            precio=1499.99,
            stock=5,
            categoria_id=1,
            imagen="/static/imagenes/laptop.jpg"
        )
        db.add(producto2)
        
        # Producto con stock limitado
        producto3 = Producto(
            id=3,
            nombre="Tablet",
            descripcion="Tablet de última generación",
            precio=699.99,
            stock=1,
            categoria_id=1,
            imagen="/static/imagenes/tablet.jpg"
        )
        db.add(producto3)
        
        # Producto sin stock
        producto4 = Producto(
            id=4,
            nombre="Smartwatch",
            descripcion="Reloj inteligente",
            precio=299.99,
            stock=0,
            categoria_id=1,
            imagen="/static/imagenes/smartwatch.jpg"
        )
        db.add(producto4)
        
        db.commit()
        db.close()
        
        # Simular token de autenticación
        cls.cliente_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sIjoiY2xpZW50ZSJ9.xyz789"
    
    @classmethod
    def teardown_class(cls):
        """Limpieza después de todas las pruebas"""
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_carrito.db"):
            os.remove("test_carrito.db")
    
    # PRUEBAS BÁSICAS
    
    def test_agregar_producto_carrito(self):
        """Prueba agregar un producto al carrito"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            response = client.post(
                "/carrito/agregar",
                json={"producto_id": 1, "cantidad": 2},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["producto_id"] == 1
            assert data["cantidad"] == 2
    
    def test_ver_carrito(self):
        """Prueba ver el contenido del carrito"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            response = client.get(
                "/carrito/",
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) >= 1  # Al menos el producto agregado anteriormente
    
    # CASOS LÍMITE Y VALIDACIONES
    
    @pytest.mark.parametrize("producto_id,cantidad,expected_status", [
        (1, 0, 422),    # Cantidad cero
        (1, -1, 422),   # Cantidad negativa
        (1, 11, 400),   # Cantidad mayor al stock disponible
        (999, 1, 404),  # Producto inexistente
        (4, 1, 400)     # Producto sin stock
    ])
    def test_agregar_producto_carrito_limites(self, producto_id, cantidad, expected_status):
        """Prueba agregar productos al carrito con valores límite"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            response = client.post(
                "/carrito/agregar",
                json={"producto_id": producto_id, "cantidad": cantidad},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == expected_status
    
    def test_actualizar_cantidad_carrito(self):
        """Prueba actualizar la cantidad de un producto en el carrito"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            # Primero agregamos un producto
            client.post(
                "/carrito/agregar",
                json={"producto_id": 2, "cantidad": 1},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            
            # Luego actualizamos la cantidad
            response = client.put(
                "/carrito/actualizar",
                json={"producto_id": 2, "cantidad": 3},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["producto_id"] == 2
            assert data["cantidad"] == 3
    
    def test_actualizar_cantidad_excede_stock(self):
        """Prueba actualizar la cantidad a un valor que excede el stock disponible"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            response = client.put(
                "/carrito/actualizar",
                json={"producto_id": 2, "cantidad": 10},  # Stock es 5
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 400
            assert "stock disponible" in response.json()["detail"].lower()
    
    def test_eliminar_producto_carrito(self):
        """Prueba eliminar un producto del carrito"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            # Primero agregamos un producto
            client.post(
                "/carrito/agregar",
                json={"producto_id": 3, "cantidad": 1},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            
            # Luego lo eliminamos
            response = client.delete(
                f"/carrito/eliminar/{3}",
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 200
            
            # Verificamos que ya no está en el carrito
            response = client.get(
                "/carrito/",
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            data = response.json()
            assert not any(item["producto_id"] == 3 for item in data)
    
    def test_eliminar_producto_inexistente_carrito(self):
        """Prueba eliminar un producto que no está en el carrito"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            response = client.delete(
                f"/carrito/eliminar/{999}",
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 404
    
    def test_vaciar_carrito(self):
        """Prueba vaciar todo el carrito"""
        # Simulamos autenticación
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "1", "rol": "cliente"}):
            # Agregamos varios productos
            client.post(
                "/carrito/agregar",
                json={"producto_id": 1, "cantidad": 1},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            client.post(
                "/carrito/agregar",
                json={"producto_id": 2, "cantidad": 1},
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            
            # Vaciamos el carrito
            response = client.delete(
                "/carrito/vaciar",
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            assert response.status_code == 200
            
            # Verificamos que el carrito está vacío
            response = client.get(
                "/carrito/",
                headers={"Authorization": f"Bearer {self.cliente_token}"}
            )
            data = response.json()
            assert len(data) == 0
    
    # PRUEBAS DE SEGURIDAD
    
    def test_acceder_carrito_sin_autenticacion(self):
        """Prueba acceder al carrito sin autenticación"""
        response = client.get("/carrito/")
        assert response.status_code == 401
    
    def test_acceder_carrito_otro_usuario(self):
        """Prueba acceder al carrito de otro usuario"""
        # Simulamos autenticación con un usuario diferente
        with patch("app.routers.carrito.verificar_token", return_value={"sub": "2", "rol": "cliente"}):
            response = client.get(
                "/carrito/",
                headers={"Authorization": "Bearer otro_token"}
            )
            assert response.status_code == 200
            data = response.json()
            # Debería estar vacío porque es otro usuario
            assert len(data) == 0

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])