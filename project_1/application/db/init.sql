--
-- Current Database: `facefivedb`
--

DROP DATABASE IF EXISTS `facefivedb`;
CREATE DATABASE `facefivedb`;

CREATE USER IF NOT EXISTS 'facefive'@'%' IDENTIFIED BY 'facefivepass';
GRANT all privileges ON facefivedb.* TO 'facefive'@'%';
FLUSH PRIVILEGES
