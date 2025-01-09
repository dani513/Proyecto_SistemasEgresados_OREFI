
CREATE DATABASE IF NOT EXISTS egresados_mysql
DEFAULT CHARACTER SET latin1;

USE egresados_mysql;

-- Elimina la tabla si ya existe
DROP TABLE IF EXISTS `cambio_numerico`;


-- Crea la tabla
CREATE TABLE `cambio_numerico` (
  `numero` INT(11) NOT NULL DEFAULT 9, -- Columna entera con valor predeterminado 9
  `cadena` VARCHAR(255) DEFAULT NULL, -- Columna de texto que permite valores nulos
  PRIMARY KEY (`numero`) -- Clave primaria en la columna `numero`
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `carrera`;



-- Crear la tabla
CREATE TABLE `carrera` (
  `cod_carrera` INT(10) UNSIGNED NOT NULL DEFAULT 0, -- Columna entera sin signo con valor predeterminado 0
  `nombre` VARCHAR(50) DEFAULT NULL,                -- Columna de texto que permite valores nulos
  PRIMARY KEY (`cod_carrera`)                       -- Definir `cod_carrera` como clave primaria
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



-- Estructura de la tabla `estado_periodo`

-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `estado_periodo`;



-- Crear la tabla
CREATE TABLE `estado_periodo` (
  `cod_periodo` VARCHAR(5) NOT NULL,        -- Columna de texto, no permite valores nulos
  `cod_carrera` VARCHAR(50) NOT NULL,      -- Columna de texto, no permite valores nulos
  `cod_estado` VARCHAR(7) NOT NULL,        -- Columna de texto, no permite valores nulos
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT, -- Columna entera con incremento automático
  PRIMARY KEY (`id`)                       -- Clave primaria en la columna `id`
) ENGINE=InnoDB AUTO_INCREMENT=243 DEFAULT CHARSET=latin1;




-- Estructura de la tabla `informacion`

-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `informacion`;



-- Crear la tabla
CREATE TABLE `informacion` (
  `director` VARCHAR(50) NOT NULL, -- Columna de texto, no permite valores nulos
  `decano` VARCHAR(50) NOT NULL,   -- Columna de texto, no permite valores nulos
  PRIMARY KEY (`director`)         -- Clave primaria en la columna `director`
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



-- Estructura de la tabla `ip`

-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `ip`;


-- Crear la tabla
CREATE TABLE `ip` (
  `num_ip` VARCHAR(20) NOT NULL DEFAULT '', -- Columna de texto, no permite valores nulos
  `desc` VARCHAR(100) DEFAULT NULL,         -- Columna de texto que permite valores nulos
  PRIMARY KEY (`num_ip`)                    -- Clave primaria en la columna `num_ip`
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



-- Estructura de la tabla `periodo`

-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `periodo`;

-- Crear la tabla
CREATE TABLE `periodo` (
  `cod_periodo` VARCHAR(5) NOT NULL DEFAULT '', -- Código del periodo, no permite valores nulos
  `ano` INT(11) DEFAULT NULL,                  -- Año, puede ser nulo
  `periodo` VARCHAR(1) DEFAULT NULL,           -- Periodo, puede ser nulo
  PRIMARY KEY (`cod_periodo`),                 -- Clave primaria en `cod_periodo`
  KEY `cod_periodo_index` (`cod_periodo`)      -- Índice en la columna `cod_periodo`
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




-- Estructura de la tabla `registro_egresado`

-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `registro_egresado`;


-- Crear la tabla
CREATE TABLE `registro_egresado` (
  `ag` DECIMAL(10,3) DEFAULT NULL,           -- Columna decimal con tres decimales, permite valores nulos
  `aa` DECIMAL(10,3) DEFAULT NULL,           -- Columna decimal con tres decimales, permite valores nulos
  `pg` DECIMAL(10,3) DEFAULT NULL,           -- Columna decimal con tres decimales, permite valores nulos
  `pa` DECIMAL(10,3) DEFAULT NULL,           -- Columna decimal con tres decimales, permite valores nulos
  `rendimiento` DECIMAL(10,2) DEFAULT NULL,  -- Columna decimal con dos decimales, permite valores nulos
  `fecha_grado` VARCHAR(10) DEFAULT NULL,    -- Columna de texto de hasta 10 caracteres, permite valores nulos
  `cod_carrera` INT(11) DEFAULT NULL,        -- Columna entera de hasta 11 dígitos, permite valores nulos
  `cod_periodo` VARCHAR(5) DEFAULT NULL,     -- Columna de texto de hasta 5 caracteres, permite valores nulos
  `num_periodo` INT(11) DEFAULT NULL,        -- Columna entera de hasta 11 dígitos, permite valores nulos
  `cedula` VARCHAR(10) CHARACTER SET latin1 DEFAULT NULL, -- Columna de texto de hasta 10 caracteres en `latin1`, permite valores nulos
  `nombre` VARCHAR(255) DEFAULT NULL,        -- Columna de texto de hasta 255 caracteres, permite valores nulos
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT, -- Columna entera sin signo con incremento automático
  PRIMARY KEY (`id`),                        -- Clave primaria en la columna `id`
  KEY `cod_carrera` (`cod_carrera`),         -- Índice en la columna `cod_carrera`
  KEY `cod_periodo` (`cod_periodo`)          -- Índice en la columna `cod_periodo`
) ENGINE=InnoDB AUTO_INCREMENT=17234 DEFAULT CHARSET=utf8 
COMMENT='InnoDB; free: 37888 kB; InnoDB free: 8192 kB';


-- Estructura de la tabla `usuario`

-- Eliminar la tabla si ya existe
DROP TABLE IF EXISTS `usuario`;


-- Crear la tabla
CREATE TABLE `usuario` (
  `nombre` VARCHAR(25) NOT NULL DEFAULT '', -- Columna de texto, no permite valores nulos
  `clave` VARCHAR(15) DEFAULT NULL,        -- Columna de texto que permite valores nulos
  `p_acesso` INT(11) DEFAULT NULL          -- Columna entera, permite valores nulos
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


