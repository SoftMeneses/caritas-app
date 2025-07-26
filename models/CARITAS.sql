/*
SQLyog Ultimate
MySQL - 10.3.23-MariaDB : Database - caritas
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `donacion_detalle` */

CREATE TABLE `donacion_detalle` (
  `DETALLE_ID` int(10) NOT NULL AUTO_INCREMENT,
  `DONACION_ID` int(10) DEFAULT NULL,
  `TIPO` varchar(200) NOT NULL DEFAULT '',
  `DESCRIPCION` varchar(200) NOT NULL DEFAULT '',
  `CANTIDAD` decimal(14,0) NOT NULL DEFAULT 0,
  `MONTO` decimal(14,0) NOT NULL DEFAULT 0,
  `METODO_PAGO` varchar(60) NOT NULL DEFAULT '',
  `UTILIZADO` decimal(14,0) NOT NULL DEFAULT 0,
  PRIMARY KEY (`DETALLE_ID`),
  KEY `DONACION` (`DONACION_ID`),
  CONSTRAINT `DONACION` FOREIGN KEY (`DONACION_ID`) REFERENCES `donaciones` (`ID_DONACION`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=latin1;

/*Data for the table `donacion_detalle` */

/*Table structure for table `donaciones` */

CREATE TABLE `donaciones` (
  `ID_DONACION` int(10) NOT NULL AUTO_INCREMENT,
  `DONANTE_ID` int(10) NOT NULL,
  `FECHA` date DEFAULT NULL,
  `DESCRIPCION` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID_DONACION`),
  KEY `DONANTE_ID` (`DONANTE_ID`),
  CONSTRAINT `DONANTE_ID` FOREIGN KEY (`DONANTE_ID`) REFERENCES `donantes` (`ID_DONANTE`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;

/*Data for the table `donaciones` */

/*Table structure for table `donantes` */

CREATE TABLE `donantes` (
  `ID_DONANTE` int(10) NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(50) NOT NULL DEFAULT '',
  `TELEFONO` varchar(20) NOT NULL DEFAULT '',
  `CORREO` varchar(30) NOT NULL DEFAULT '',
  `CEDULA` varchar(20) NOT NULL DEFAULT '',
  `DIRECCION` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID_DONANTE`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=latin1;

/*Data for the table `donantes` */

/*Table structure for table `jornada_detalle` */

CREATE TABLE `jornada_detalle` (
  `DETALLE_JORNADA_ID` int(10) NOT NULL AUTO_INCREMENT,
  `JORNADA_ID` int(10) DEFAULT NULL,
  `RECURSO_UTILIZADO` varchar(200) DEFAULT NULL,
  `CANTIDAD_UTILIZADA` varchar(200) DEFAULT NULL,
  `ID_DETALLE_DONACION` int(11) DEFAULT NULL,
  PRIMARY KEY (`DETALLE_JORNADA_ID`),
  KEY `jornada_detalle_ibfk_2` (`JORNADA_ID`),
  CONSTRAINT `jornada_detalle_ibfk_2` FOREIGN KEY (`JORNADA_ID`) REFERENCES `jornadas` (`ID_JORNADA`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=latin1;

/*Data for the table `jornada_detalle` */

/*Table structure for table `jornadas` */

CREATE TABLE `jornadas` (
  `ID_JORNADA` int(10) NOT NULL AUTO_INCREMENT,
  `FECHA` date DEFAULT NULL,
  `DESCRIPCION` varchar(200) DEFAULT NULL,
  `UBICACION` varchar(200) DEFAULT NULL,
  `COMPLETADA` int(1) NOT NULL DEFAULT 0,
  `OBSERVACION` varchar(500) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID_JORNADA`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

/*Data for the table `jornadas` */

/*Table structure for table `jornadas_voluntarios` */

CREATE TABLE `jornadas_voluntarios` (
  `ID_JORNADA_VOLUNTARIO` int(11) NOT NULL AUTO_INCREMENT,
  `ID_JORNADA` int(11) NOT NULL,
  `ID_VOLUNTARIO` int(11) NOT NULL,
  `PARTICIPACION` tinyint(1) DEFAULT 0,
  `HORAS_VOLUNTARIO` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID_JORNADA`,`ID_VOLUNTARIO`),
  KEY `ID_JORNADA_VOLUNTARIO` (`ID_JORNADA_VOLUNTARIO`),
  KEY `jornadas_voluntarios_ibfk_2` (`ID_VOLUNTARIO`),
  CONSTRAINT `jornadas_voluntarios_ibfk_1` FOREIGN KEY (`ID_JORNADA`) REFERENCES `jornadas` (`ID_JORNADA`) ON UPDATE CASCADE,
  CONSTRAINT `jornadas_voluntarios_ibfk_2` FOREIGN KEY (`ID_VOLUNTARIO`) REFERENCES `voluntarios` (`ID_VOLUNTARIO`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=latin1;

/*Data for the table `jornadas_voluntarios` */

/*Table structure for table `perfiles` */

CREATE TABLE `perfiles` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(20) NOT NULL DEFAULT '',
  `CONSULTA` tinyint(1) DEFAULT 0,
  `MODIFICAR` tinyint(1) DEFAULT 0,
  `INSERTAR` tinyint(1) DEFAULT 0,
  `ELIMINAR` tinyint(1) DEFAULT 0,
  `TOTAL` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `perfiles` */

insert  into `perfiles`(`ID`,`NOMBRE`,`CONSULTA`,`MODIFICAR`,`INSERTAR`,`ELIMINAR`,`TOTAL`) values (1,'ADMIN',0,0,0,0,1);
insert  into `perfiles`(`ID`,`NOMBRE`,`CONSULTA`,`MODIFICAR`,`INSERTAR`,`ELIMINAR`,`TOTAL`) values (2,'PRUEBA',1,0,1,0,0);

/*Table structure for table `usuarios` */

CREATE TABLE `usuarios` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `PERFIL_ID` int(2) NOT NULL DEFAULT 1,
  `USUARIO` varchar(256) NOT NULL DEFAULT '',
  `PASSWORD` varchar(256) NOT NULL DEFAULT '',
  `EMAIL` varchar(256) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UNIQUE` (`USUARIO`),
  KEY `PERFIL_ID` (`PERFIL_ID`),
  CONSTRAINT `PERFIL_ID` FOREIGN KEY (`PERFIL_ID`) REFERENCES `perfiles` (`ID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `usuarios` */

insert  into `usuarios`(`ID`,`PERFIL_ID`,`USUARIO`,`PASSWORD`,`EMAIL`) values (1,1,'ADMIN','ADMIN','PRUEBA@GMAIL.COM');

/*Table structure for table `voluntarios` */

CREATE TABLE `voluntarios` (
  `ID_VOLUNTARIO` int(10) NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(200) DEFAULT NULL,
  `CEDULA` varchar(20) DEFAULT NULL,
  `TELEFONO` varchar(20) DEFAULT NULL,
  `CORREO` varchar(50) DEFAULT NULL,
  `DISPONIBILIDAD` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID_VOLUNTARIO`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

/*Data for the table `voluntarios` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
