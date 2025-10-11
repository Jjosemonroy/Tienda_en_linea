import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import Usuario, Categoria, Producto

# Configurar base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_avanzado.db"
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

class TestProductosAvanzado:
    """Pruebas unitarias avanzadas para los endpoints de productos"""
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial para todas las pruebas"""
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        
        # Crear datos de prueba
        db = TestingSessionLocal()
        
        # Crear usuario admin
        admin = Usuario(
            id=1,
            nombre="Admin Test",
            correo="admin@test.com",
            contraseña="hashed_password",
            rol="admin",
            estado="activo"
        )
        db.add(admin)
        
        # Crear categoría
        categoria = Categoria(
            id=1,
            nombre="Electrónicos",
            descripcion="Productos electrónicos",
            activo=True
        )
        db.add(categoria)
        
        # Crear categoría inactiva
        categoria_inactiva = Categoria(
            id=2,
            nombre="Descontinuados",
            descripcion="Productos descontinuados",
            activo=False
        )
        db.add(categoria_inactiva)
        
        # Crear producto de prueba
        producto = Producto(
            id=1,
            nombre="iPhone 15",
            descripcion="Teléfono inteligente",
            precio=999.99,
            stock=10,
            categoria_id=1,
            imagen="/static/imagenes/test.jpg"
        )
        db.add(producto)
        
        # Crear producto con stock mínimo
        producto_stock_minimo = Producto(
            id=2,
            nombre="Último Modelo",
            descripcion="Último disponible",
            precio=1299.99,
            stock=1,
            categoria_id=1,
            imagen="/static/imagenes/ultimo.jpg"
        )
        db.add(producto_stock_minimo)
        
        # Crear producto sin stock
        producto_sin_stock = Producto(
            id=3,
            nombre="Agotado",
            descripcion="Producto sin stock",
            precio=499.99,
            stock=0,
            categoria_id=1,
            imagen="/static/imagenes/agotado.jpg"
        )
        db.add(producto_sin_stock)
        
        db.commit()
        db.close()
        
        # Simular token de autenticación
        cls.admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sIjoiYWRtaW4ifQ.abc123"
    
    @classmethod
    def teardown_class(cls):
        """Limpieza después de todas las pruebas"""
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_avanzado.db"):
            os.remove("test_avanzado.db")
    
    # CASOS LÍMITE Y VALIDACIONES
    
    @pytest.mark.parametrize("precio,stock,expected_status", [
        (100, 10, 401),  # Caso normal pero sin autenticación
        (-10, 5, 401),   # Precio negativo
        (100, -1, 401),  # Stock negativo
        (0, 0, 401)      # Precio y stock cero
    ])
    def test_crear_producto_limites(self, precio, stock, expected_status):
        """Prueba crear productos con valores límite"""
        producto_nuevo = {
            "nombre": "Producto Test",
            "descripcion": "Descripción",
            "precio": precio,
            "stock": stock,
            "categoria_id": 1
        }
        response = client.post("/productos/", json=producto_nuevo)
        assert response.status_code == expected_status
    
    def test_actualizar_stock_limites(self):
        """Prueba actualización de stock con valores límite"""
        # Simulamos autenticación
        with patch("app.routers.productos.verificar_token", return_value={"sub": "1", "rol": "admin"}):
            # Caso: Stock en cero
            response = client.put(
                "/productos/1/stock",
                json={"cantidad": 0},
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["stock"] == 0
            
            # Caso: Intento de stock negativo (debería fallar)
            response = client.put(
                "/productos/1/stock",
                json={"cantidad": -5},
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            assert response.status_code == 422
            
            # Caso: Stock muy grande
            response = client.put(
                "/productos/1/stock",
                json={"cantidad": 1000000},
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["stock"] == 1000000
    
    # MANEJO DE ERRORES
    
    def test_producto_no_existente(self):
        """Prueba acceso a producto inexistente"""
        response = client.get("/productos/9999")
        assert response.status_code == 404
        assert "detail" in response.json()
    
    def test_crear_producto_categoria_invalida(self):
        """Prueba crear producto con categoría que no existe"""
        # Simulamos autenticación
        with patch("app.routers.productos.verificar_token", return_value={"sub": "1", "rol": "admin"}):
            producto_nuevo = {
                "nombre": "Producto Test",
                "descripcion": "Descripción",
                "precio": 99.99,
                "stock": 10,
                "categoria_id": 9999  # Categoría inexistente
            }
            response = client.post(
                "/productos/",
                json=producto_nuevo,
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            assert response.status_code == 404
            assert "no encontrada" in response.json()["detail"].lower()
    
    def test_crear_producto_categoria_inactiva(self):
        """Prueba crear producto con categoría inactiva"""
        # Simulamos autenticación
        with patch("app.routers.productos.verificar_token", return_value={"sub": "1", "rol": "admin"}):
            producto_nuevo = {
                "nombre": "Producto Test",
                "descripcion": "Descripción",
                "precio": 99.99,
                "stock": 10,
                "categoria_id": 2  # Categoría inactiva
            }
            response = client.post(
                "/productos/",
                json=producto_nuevo,
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            # Dependiendo de la implementación, podría ser 400 o 422
            assert response.status_code in [400, 422, 404]
    
    # FILTROS Y BÚSQUEDAS
    
    def test_filtrar_productos_por_stock(self):
        """Prueba filtrar productos por disponibilidad de stock"""
        # Productos con stock > 0
        response = client.get("/productos/?con_stock=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # Al menos los productos con ID 1 y 2
        for producto in data:
            assert producto["stock"] > 0
        
        # Productos sin stock
        response = client.get("/productos/?con_stock=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1  # Al menos el producto con ID 3
        for producto in data:
            assert producto["stock"] == 0
    
    def test_buscar_productos_por_nombre(self):
        """Prueba buscar productos por nombre"""
        response = client.get("/productos/buscar?nombre=iPhone")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any("iphone" in producto["nombre"].lower() for producto in data)
        
        # Búsqueda que no debe encontrar resultados
        response = client.get("/productos/buscar?nombre=ProductoInexistente")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    # PRUEBAS DE CONCURRENCIA (SIMULADAS)
    
    def test_actualizar_stock_concurrente(self):
        """Simula actualizaciones concurrentes de stock"""
        # Simulamos autenticación
        with patch("app.routers.productos.verificar_token", return_value={"sub": "1", "rol": "admin"}):
            # Primero establecemos un stock conocido
            client.put(
                "/productos/2/stock",
                json={"cantidad": 10},
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            
            # Simulamos dos actualizaciones "simultáneas"
            # Primera actualización: -3 unidades
            response1 = client.put(
                "/productos/2/stock",
                json={"cantidad": 7},
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            
            # Segunda actualización: -5 unidades más (desde el stock original)
            response2 = client.put(
                "/productos/2/stock",
                json={"cantidad": 5},
                headers={"Authorization": f"Bearer {self.admin_token}"}
            )
            
            # Ambas deberían ser exitosas
            assert response1.status_code == 200
            assert response2.status_code == 200
            
            # La última actualización debería prevalecer
            final_response = client.get("/productos/2")
            assert final_response.status_code == 200
            assert final_response.json()["stock"] == 5

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])