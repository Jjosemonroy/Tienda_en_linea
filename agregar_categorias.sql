-- Script para agregar tabla de categorías y modificar tabla de productos
-- Ejecutar en la base de datos tienda_online

USE tienda_online;

-- Crear tabla de categorías
CREATE TABLE IF NOT EXISTS `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `activo` boolean DEFAULT true,
  `fecha_creacion` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insertar categorías básicas
INSERT INTO `categorias` (`nombre`, `descripcion`) VALUES
('Electrónicos', 'Productos electrónicos y tecnología'),
('Ropa', 'Vestimenta y accesorios'),
('Hogar', 'Artículos para el hogar'),
('Deportes', 'Equipamiento deportivo'),
('Libros', 'Libros y material educativo'),
('Juguetes', 'Juguetes y entretenimiento'),
('Alimentos', 'Productos alimenticios'),
('Belleza', 'Productos de belleza y cuidado personal');

-- Agregar columna categoria_id a la tabla productos
ALTER TABLE `productos` 
ADD COLUMN `categoria_id` int DEFAULT NULL AFTER `imagen`,
ADD CONSTRAINT `productos_ibfk_categoria` 
FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`);

-- Asignar categorías a productos existentes (ejemplo)
UPDATE `productos` SET `categoria_id` = 1 WHERE `nombre` LIKE '%MAC%' OR `nombre` LIKE '%Iphone%';
UPDATE `productos` SET `categoria_id` = 2 WHERE `categoria_id` IS NULL;

-- Verificar que todos los productos tengan categoría
UPDATE `productos` SET `categoria_id` = 1 WHERE `categoria_id` IS NULL; 