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
/*Table structure for table `roles` */

CREATE TABLE `roles` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `NOMBRE` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `roles` */

insert  into `roles`(`ID`,`NOMBRE`) values (1,'ADMIN');
insert  into `roles`(`ID`,`NOMBRE`) values (2,'VOLUNTARIO');

/*Table structure for table `usuarios` */

CREATE TABLE `usuarios` (
  `ID` int(2) NOT NULL AUTO_INCREMENT,
  `ROL_ID` int(2) NOT NULL DEFAULT 1,
  `USUARIO` varchar(256) NOT NULL DEFAULT '',
  `PASSWORD` varchar(256) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UNIQUE` (`USUARIO`),
  KEY `ROL_ID` (`ROL_ID`),
  CONSTRAINT `ROL_ID` FOREIGN KEY (`ROL_ID`) REFERENCES `roles` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `usuarios` */

insert  into `usuarios`(`ID`,`ROL_ID`,`USUARIO`,`PASSWORD`) values (1,1,'ADMIN','ADMIN');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
