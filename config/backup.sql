-- MySQL dump 10.13  Distrib 9.0.1, for Win64 (x86_64)
--
-- Host: localhost    Database: lapuntita
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `detalleventa`
--

DROP TABLE IF EXISTS `detalleventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleventa` (
  `idDetalleVenta` int NOT NULL AUTO_INCREMENT,
  `idVenta` int NOT NULL,
  `idProducto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precioUnitario` decimal(10,2) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idDetalleVenta`),
  KEY `idVenta` (`idVenta`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `detalleventa_ibfk_1` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`idVenta`),
  CONSTRAINT `detalleventa_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleventa`
--

LOCK TABLES `detalleventa` WRITE;
/*!40000 ALTER TABLE `detalleventa` DISABLE KEYS */;
INSERT INTO `detalleventa` VALUES (1,1,13,1,18.86,18.86),(2,1,35,1,13.12,13.12),(3,19,19,1,18.04,18.04),(4,19,36,1,13.12,13.12);
/*!40000 ALTER TABLE `detalleventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrega`
--

DROP TABLE IF EXISTS `entrega`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrega` (
  `idEntrega` int NOT NULL AUTO_INCREMENT,
  `idVenta` int NOT NULL,
  `idRepartidor` int NOT NULL,
  `fechaEntrega` datetime NOT NULL,
  `horaEstimada` time NOT NULL,
  `estadoEntrega` bit(1) NOT NULL,
  PRIMARY KEY (`idEntrega`),
  KEY `idVenta` (`idVenta`),
  KEY `idRepartidor` (`idRepartidor`),
  CONSTRAINT `entrega_ibfk_1` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`idVenta`),
  CONSTRAINT `entrega_ibfk_2` FOREIGN KEY (`idRepartidor`) REFERENCES `repartidor` (`idRepartidor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrega`
--

LOCK TABLES `entrega` WRITE;
/*!40000 ALTER TABLE `entrega` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrega` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `idProducto` int NOT NULL AUTO_INCREMENT,
  `idTipoProducto` int NOT NULL,
  `nombreProducto` varchar(50) NOT NULL,
  `descripcion` text,
  `precioUnitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idProducto`),
  KEY `idTipoProducto` (`idTipoProducto`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idTipoProducto`) REFERENCES `tipoproducto` (`idTipoProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,4,'Leche condensada',NULL,1.64),(2,4,'Fudge',NULL,1.64),(3,4,'Manjar',NULL,1.64),(4,4,'Fresa',NULL,1.64),(5,4,'Maracuyá',NULL,1.64),(6,4,'Nutella',NULL,2.64),(7,3,'Mini oreo',NULL,0.82),(8,3,'Lentejitas',NULL,0.82),(9,3,'Choco crispi',NULL,0.82),(10,3,'Fresa',NULL,0.82),(11,3,'Grageas',NULL,0.82),(12,1,'Latino','Bañado en Nutella con salpicaduras de coquito rayado',18.86),(13,1,'Suggar daddy','Chocolate blanco bañado en oro con relleno de Nutella',18.86),(14,1,'Europeo','Chocolate rosado con chorreo blanco más un topping a elección',18.04),(15,1,'Africano','Chocolate negro con chorreo blanco más un topping a elección',16.40),(16,1,'Dinamita','Chocolate negro con chorreo rosado más nuestro polvo explosivo',16.40),(17,1,'Cocolover','Relleno en Nutella con plátano, fresa, coco rallado y chorreo negro',18.04),(18,1,'Europea','Relleno en fudge con plátano, arándanos y chorreo rosado',18.04),(19,1,'Pichanguera','Relleno de manjar blanco con plátano, fresa y chorreo blanco',18.04),(20,1,'Power','Rellena de leche condensada con fresa, plátano y chorreo blanco con rosado',18.04),(21,1,'Malcriada','Relleno en fudge con helado y fruta',22.96),(22,1,'Moreno','Fresa, Nutella y azúcar impalpable',28.70),(23,1,'Gringo','Salsa de tomate, queso y jamón',26.24),(24,1,'Vergano','Salsa de tomate, queso, champiñón, zapallito italiano, aceituna y pimentón',29.52),(25,1,'Juguetón','Salsa de tomate, queso, jamón y piña',27.06),(26,1,'Carnoso','Salsa de tomate, queso, peperoni y salchicha',28.70),(27,2,'Jugo de naranja',NULL,8.20),(28,2,'Jugo de papaya',NULL,9.84),(29,2,'Jugo de fresa',NULL,9.84),(30,2,'Jugo de fresa con leche',NULL,10.66),(31,2,'Milkshake de oreo',NULL,12.30),(32,2,'Milkshake de strawberry',NULL,12.30),(33,2,'Milkshake de brownie',NULL,13.12),(34,2,'Milkshake de nutella',NULL,13.12),(35,2,'Frozen de fresa',NULL,13.12),(36,2,'Frozen de piña',NULL,13.12),(37,2,'Frozen de maracumango',NULL,13.12);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repartidor`
--

DROP TABLE IF EXISTS `repartidor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repartidor` (
  `idRepartidor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `disponibilidad` bit(1) NOT NULL,
  PRIMARY KEY (`idRepartidor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repartidor`
--

LOCK TABLES `repartidor` WRITE;
/*!40000 ALTER TABLE `repartidor` DISABLE KEYS */;
INSERT INTO `repartidor` VALUES (1,'Carlos','Rodríguez','987654321',_binary ''),(2,'Javier','González','996543210',_binary ''),(3,'Andrés','Martínez','919876543',_binary '');
/*!40000 ALTER TABLE `repartidor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipoproducto`
--

DROP TABLE IF EXISTS `tipoproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipoproducto` (
  `idTipoProducto` int NOT NULL AUTO_INCREMENT,
  `tipoProducto` varchar(10) NOT NULL,
  PRIMARY KEY (`idTipoProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipoproducto`
--

LOCK TABLES `tipoproducto` WRITE;
/*!40000 ALTER TABLE `tipoproducto` DISABLE KEYS */;
INSERT INTO `tipoproducto` VALUES (1,'Alimento'),(2,'Bebida'),(3,'Topping'),(4,'Relleno');
/*!40000 ALTER TABLE `tipoproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipousuario`
--

DROP TABLE IF EXISTS `tipousuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipousuario` (
  `idTipoUsuario` int NOT NULL AUTO_INCREMENT,
  `tipoUsuario` varchar(10) NOT NULL,
  PRIMARY KEY (`idTipoUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipousuario`
--

LOCK TABLES `tipousuario` WRITE;
/*!40000 ALTER TABLE `tipousuario` DISABLE KEYS */;
INSERT INTO `tipousuario` VALUES (1,'Admin'),(2,'Cliente');
/*!40000 ALTER TABLE `tipousuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `idTipoUsuario` int NOT NULL,
  `dni` varchar(8) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `email` varchar(255) NOT NULL,
  `direccion` text NOT NULL,
  `referencia` text,
  `passw` text NOT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `idTipoUsuario` (`idTipoUsuario`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`idTipoUsuario`) REFERENCES `tipousuario` (`idTipoUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,2,'73065779','Ashley','Bayona','981258941','ashley.bayonav@gmail.com','Av. Oscar R. Benavides 5737',NULL,'pbkdf2:sha256:30$TcelsqDduQrqLlJwuzVvz6zPn6rBbb$199b607d07dc2d40b945b166691d25ec38ae0a2306653393135e8c6f21704afa'),(3,2,'74845983','Francisco','Abad','989744544','fran.abad@gmail.com','Calle Germán Amézaga s/n - Lima',NULL,'pbkdf2:sha256:30$Yutb7lzdXr0bOdPmLehmPOJlijibLn$3050b219a45ca701de69687d7c891858bb5f8629361911d9e594bbf1135d2c93'),(5,1,'88888888','Admin','San Miguel','999999999','admin@lapuntita.com','La Marina 2274',NULL,'admin123');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `idVenta` int NOT NULL AUTO_INCREMENT,
  `idUsuario` int NOT NULL,
  `importeVenta` decimal(10,2) NOT NULL,
  `importeIGV` decimal(10,2) NOT NULL,
  `importeTotal` decimal(10,2) NOT NULL,
  `fecha` datetime NOT NULL,
  `codigoBoleta` char(8) NOT NULL,
  `estado` bit(1) NOT NULL,
  PRIMARY KEY (`idVenta`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,1,31.98,5.76,37.74,'2024-10-02 19:25:47','3eb20071',_binary '\0'),(19,3,31.16,5.61,36.77,'2024-10-02 20:40:07','0054f41a',_binary '\0'),(27,1,0.00,0.00,0.00,'2024-10-07 18:54:09','722b2c95',_binary '\0');
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-08  1:46:30
