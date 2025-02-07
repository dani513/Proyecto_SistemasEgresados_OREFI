-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: egresados_mysql
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('4a224c752697');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cambio_numerico`
--

DROP TABLE IF EXISTS `cambio_numerico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cambio_numerico` (
  `numero` int NOT NULL DEFAULT '9',
  `cadena` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`numero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cambio_numerico`
--

LOCK TABLES `cambio_numerico` WRITE;
/*!40000 ALTER TABLE `cambio_numerico` DISABLE KEYS */;
/*!40000 ALTER TABLE `cambio_numerico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrera`
--

DROP TABLE IF EXISTS `carrera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrera` (
  `cod_carrera` int unsigned NOT NULL DEFAULT '0',
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cod_carrera`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrera`
--

LOCK TABLES `carrera` WRITE;
/*!40000 ALTER TABLE `carrera` DISABLE KEYS */;
INSERT INTO `carrera` VALUES (10,'INGENIERÍA DE SISTEMAS'),(20,'INGENIERÍA QUÍMICA'),(30,'INGENIERÍA MECÁNICA'),(40,'INGENIERÍA CIVIL'),(50,'INGENIERÍA GEOLÓGICA'),(60,'INGENIERÍA ELÉCTRICA'),(70,'INGENIERÍA FORESTAL');
/*!40000 ALTER TABLE `carrera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_periodo`
--

DROP TABLE IF EXISTS `estado_periodo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_periodo` (
  `cod_periodo` varchar(5) NOT NULL,
  `cod_carrera` varchar(50) NOT NULL,
  `cod_estado` varchar(7) NOT NULL,
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=243 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_periodo`
--

LOCK TABLES `estado_periodo` WRITE;
/*!40000 ALTER TABLE `estado_periodo` DISABLE KEYS */;
/*!40000 ALTER TABLE `estado_periodo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `informacion`
--

DROP TABLE IF EXISTS `informacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `informacion` (
  `director` varchar(50) NOT NULL,
  `decano` varchar(50) NOT NULL,
  PRIMARY KEY (`director`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informacion`
--

LOCK TABLES `informacion` WRITE;
/*!40000 ALTER TABLE `informacion` DISABLE KEYS */;
INSERT INTO `informacion` VALUES ('Msc. Richard G. Espinoza L.','Dr. Carlos A. Muñoz B.');
/*!40000 ALTER TABLE `informacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip`
--

DROP TABLE IF EXISTS `ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ip` (
  `num_ip` varchar(20) NOT NULL DEFAULT '',
  `desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`num_ip`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip`
--

LOCK TABLES `ip` WRITE;
/*!40000 ALTER TABLE `ip` DISABLE KEYS */;
/*!40000 ALTER TABLE `ip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `periodo`
--

DROP TABLE IF EXISTS `periodo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `periodo` (
  `cod_periodo` varchar(5) NOT NULL DEFAULT '',
  `ano` int DEFAULT NULL,
  `periodo` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`cod_periodo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `periodo`
--

LOCK TABLES `periodo` WRITE;
/*!40000 ALTER TABLE `periodo` DISABLE KEYS */;
INSERT INTO `periodo` VALUES ('A2000',2000,'A'),('A2024',2024,'A'),('A2025',2025,'A'),('B2000',2000,'B'),('B2023',2023,'B'),('B2024',2024,'B'),('I2018',2018,'I'),('U2017',2017,'U'),('U2018',2018,'U');
/*!40000 ALTER TABLE `periodo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registro_egresado`
--

DROP TABLE IF EXISTS `registro_egresado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_egresado` (
  `ag` varchar(10) DEFAULT NULL,
  `aa` varchar(10) DEFAULT NULL,
  `pg` varchar(10) DEFAULT NULL,
  `pa` varchar(10) DEFAULT NULL,
  `rendimiento` float DEFAULT NULL,
  `fecha_grado` date DEFAULT NULL,
  `cod_carrera` int unsigned DEFAULT NULL,
  `cod_periodo` varchar(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `num_periodo` varchar(10) DEFAULT NULL,
  `cedula` varchar(20) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `cod_carrera` (`cod_carrera`),
  KEY `cod_periodo` (`cod_periodo`),
  CONSTRAINT `fk_cod_carrera` FOREIGN KEY (`cod_carrera`) REFERENCES `carrera` (`cod_carrera`),
  CONSTRAINT `fk_cod_periodo` FOREIGN KEY (`cod_periodo`) REFERENCES `periodo` (`cod_periodo`)
) ENGINE=InnoDB AUTO_INCREMENT=17252 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_egresado`
--

LOCK TABLES `registro_egresado` WRITE;
/*!40000 ALTER TABLE `registro_egresado` DISABLE KEYS */;
INSERT INTO `registro_egresado` VALUES ('20','10','20','20',0.8,'2000-01-01',10,'A2000','10','4489668','Neyda Beatriz Quintero de Monsalve',17242),('19','12','19','20',0.95,'2000-02-02',10,'A2000','12','4356119','Mauro Anibal Monsalve Rosas',17243),('17','11','17','19',0.85,'2000-03-03',10,'A2000','14','13097279','Gustavo Adolfo Monsalve Quintero',17244),('15','10','15','18',0.98,'2000-04-04',10,'A2000','14','15516837','Jean Carlos Monsalve Quintero',17245),('18','12','18','17',1,'2000-06-02',10,'A2000','20','19751119','Maria Stefany Monsalve Quintero',17246),('16','10','16','17',0.7,'2000-12-20',10,'A2000','20','26285289','Arianna Nataly Cortes Chacon',17247),('20','12','20','18',0.96,'2000-12-01',10,'A2000','10','27777513','Daniel Andres Monsalve Quintero',17248),('12','10','12','16',0.5,'2025-02-20',10,'U2018','18','26880969','Luis Alejandro Cortes Chacon',17249),('10','10','10','10',0.25,'2025-02-12',40,'A2025','10','28119458','Graciela del Valle Torres Luna',17251);
/*!40000 ALTER TABLE `registro_egresado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `nombre` varchar(25) NOT NULL DEFAULT '',
  `clave` varchar(128) DEFAULT NULL,
  `p_acesso` int DEFAULT NULL,
  `id` int NOT NULL,
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES ('Daniel','1234',1,3),('usuario_prueba','D669820a*',1,1),('usuario_prueba2','D669820a*',2,2);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-07 15:15:37
