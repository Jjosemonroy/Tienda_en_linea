-- --------------------------------------------------------
-- Host:                         localhost
-- Versión del servidor:         8.3.0 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para tienda_online
CREATE DATABASE IF NOT EXISTS `tienda_online` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tienda_online`;

-- Volcando estructura para tabla tienda_online.carrito
CREATE TABLE IF NOT EXISTS `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tienda_online.carrito: ~2 rows (aproximadamente)
DELETE FROM `carrito`;
INSERT INTO `carrito` (`id`, `usuario_id`, `producto_id`, `cantidad`) VALUES
	(5, 2, 1, 5),
	(6, 2, 2, 20);

-- Volcando estructura para tabla tienda_online.detalle_venta
CREATE TABLE IF NOT EXISTS `detalle_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `venta_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_id` (`venta_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`),
  CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tienda_online.detalle_venta: ~2 rows (aproximadamente)
DELETE FROM `detalle_venta`;
INSERT INTO `detalle_venta` (`id`, `venta_id`, `producto_id`, `cantidad`, `precio_unitario`) VALUES
	(1, 1, 1, 5, 10.00),
	(2, 3, 1, 5, 10.00);

-- Volcando estructura para tabla tienda_online.productos
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `precio` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tienda_online.productos: ~2 rows (aproximadamente)
DELETE FROM `productos`;
INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `stock`, `imagen`) VALUES
	(1, 'MAC', 'Esta es una computadora MAC 2025', 10.00, 35, 'https://cdn.pixabay.com/photo/2015/01/21/14/14/apple-606761_960_720.jpg'),
	(2, 'Prueba2', 'es una prueba', 10.00, 5, 'no hay'),
	(3, 'Prueba 3', 'no se que es', 25.00, 2, 'no hay '),
	(4, 'Iphone 16 pro max', 'Este es un telefono', 500.00, 3, '/static/imagenes/ac327fcd8bd546d2909f60948d0898a2.webp'),
	(5, 'Iphone 16 pro', 'Este es otro telelfono', 500.00, 3, '/static/imagenes/6b1bd44655e24d59bf8249c8a788c445.jpg'),
	(6, 'Iphone 333', 'fefecd', 2255.00, 2, '/static/imagenes/ffe6588c16f94e40a959d44cf52c1cb4.jpg');

-- Volcando estructura para tabla tienda_online.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `rol` enum('cliente','admin') DEFAULT 'cliente',
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tienda_online.usuarios: ~2 rows (aproximadamente)
DELETE FROM `usuarios`;
INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `contraseña`, `rol`, `estado`) VALUES
	(1, 'Jose', 'prueba@prueba.com', '$2b$12$5vio8PGB8CwdkqrC9qxEl..G2ph7SRe9vrJxDPdMSaNJKEcuiG8H6', 'cliente', 'activo'),
	(2, 'Jose', 'jose@prueba.com', '$2b$12$cujvNLdMZPHNPTODlwKutOGf4lM1gb.SMpK.DyFOxrK3MXJraEQqW', 'admin', 'activo'),
	(3, 'Pablo Perez', 'pperez@gmail.com', '$2b$12$tYi34VAR3098fnlfMtzlCuqaPNq7cicdXpMVaXbJ9Bo3E.7kbJI0m', 'cliente', 'inactivo'),
	(4, 'Iliana', 'Iliana@prueba.com', '$2b$12$2aNMt6aFtl7sLkFMDM0l7e.2VUADplON5wx14Ph0ep1Brwhqk0S62', 'cliente', 'activo');

-- Volcando estructura para tabla tienda_online.ventas
CREATE TABLE IF NOT EXISTS `ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tienda_online.ventas: ~25 rows (aproximadamente)
DELETE FROM `ventas`;
INSERT INTO `ventas` (`id`, `usuario_id`, `fecha`, `total`) VALUES
	(1, 3, '2025-05-30 03:35:56', 130.00),
	(2, 3, '2025-05-30 03:40:26', 250.00),
	(3, 3, '2025-05-30 03:40:50', 250.00),
	(4, 2, '2025-05-30 03:43:59', 250.00),
	(5, 2, '2025-05-30 03:44:17', 250.00),
	(6, 2, '2025-05-30 03:44:26', 250.00),
	(7, 2, '2025-05-30 03:44:28', 250.00),
	(8, 2, '2025-05-30 03:44:28', 250.00),
	(9, 2, '2025-05-30 03:44:29', 250.00),
	(10, 2, '2025-05-30 03:44:29', 250.00),
	(11, 2, '2025-05-30 03:44:29', 250.00),
	(12, 2, '2025-05-30 03:44:29', 250.00),
	(13, 2, '2025-05-30 03:44:29', 250.00),
	(14, 2, '2025-05-30 03:44:30', 250.00),
	(15, 2, '2025-05-30 03:44:30', 250.00),
	(16, 2, '2025-05-30 03:44:30', 250.00),
	(17, 2, '2025-05-30 03:44:30', 250.00),
	(18, 2, '2025-05-30 03:44:30', 250.00),
	(19, 2, '2025-05-30 03:44:31', 250.00),
	(20, 2, '2025-05-30 03:44:31', 250.00),
	(21, 2, '2025-05-30 03:44:31', 250.00),
	(22, 2, '2025-05-30 03:44:31', 250.00),
	(23, 2, '2025-05-30 03:44:31', 250.00),
	(24, 2, '2025-05-30 03:44:32', 250.00),
	(25, 2, '2025-05-30 03:44:32', 250.00),
	(26, 2, '2025-05-30 03:51:33', 250.00);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
