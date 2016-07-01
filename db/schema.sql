-- MySQL dump 10.13  Distrib 5.6.27, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: med_apps
-- ------------------------------------------------------
-- Server version	5.6.27-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addons`
--

DROP TABLE IF EXISTS `addons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addons` (
  `name` varchar(100) NOT NULL,
  `addon_type` varchar(100) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `package` varchar(80) NOT NULL,
  UNIQUE KEY `unique_entry` (`package`,`name`,`addon_type`),
  CONSTRAINT `addons_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `am`
--

DROP TABLE IF EXISTS `am`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `am` (
  `package` varchar(100) NOT NULL,
  `title` varchar(512)  ,
  `version` varchar(255)  ,
  `asin` varchar(255)  ,
  `category` varchar(255)  ,
  `company` varchar(255)  ,
  `price` float(10,2)  ,
  `rating` float(10,2)  ,
  `popularity` int(11)  ,
  `release_date` date  ,
  `mom` varchar(50)  ,
  `pripol` varchar(500)  ,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `package` (`package`),
  CONSTRAINT `am_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `analysis`
--

DROP TABLE IF EXISTS `analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis` (
  `package` varchar(80) NOT NULL COMMENT 'Package name as extracted from apk',
  `Type` varchar(20)   COMMENT 'DIABETS, BP OR BOTH',
  `pripol_in_app` int(1)  ,
  `path_to_exports` varchar(150)   COMMENT 'path to exported data in smart phone',
  `safety_check_bp` int(1)   COMMENT '0 = no, 1 = yes, 2 = NA (not applicable)',
  `safety_check_gl` int(1)   COMMENT '0 = no, 1 = yes, 2 = NA (not applicable)',
  `safety_check_pulse` int(1)   COMMENT '0 = no, 1 = yes, 2 = NA (not applicable)',
  `export_SD` int(1)  ,
  `export_mail` int(1)  ,
  `export_web_native` int(1)  ,
  `export_other` varchar(100)  ,
  `authentication` int(1)   COMMENT 'Additional Authentication over pin / password for app given',
  `wipe` int(1)   COMMENT 'wipe after deletion, 0 = no, 1=yes',
  `comment` text   COMMENT 'any addition comment',
  UNIQUE KEY `Package` (`package`),
  KEY `package name` (`package`),
  CONSTRAINT `analysis_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_perm`
--

DROP TABLE IF EXISTS `app_perm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_perm` (
  `id_app` int(11) DEFAULT NULL,
  `id_perm` int(11) DEFAULT NULL,
  KEY `id_app` (`id_app`),
  KEY `id_perm` (`id_perm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `apps`
--

DROP TABLE IF EXISTS `apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apps` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `label` varchar(512) NOT NULL,
  `package` varchar(80) NOT NULL COMMENT 'Package name as extracted from apk',
  `version` varchar(255)  ,
  `versioncode` varchar(100)   COMMENT 'Version Code out of manifest',
  `filesize` int(15)   COMMENT 'File size in Byte',
  `timestamp` timestamp   DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of last change',
  `path_to_icon` varchar(50)  ,
  `Type` varchar(20)   COMMENT 'DIABETS, GLUCOSE OR BOTH',
  `path_to_exports` varchar(50)   COMMENT 'path to exported data in smart phone',
  `path_to_internal_data` varchar(50)   COMMENT 'path to internal data',
  `path_to_apk` varchar(500) COMMENT 'full path to apk file',
  `comment` text   COMMENT 'any addition comment',
  PRIMARY KEY (`id`),
  UNIQUE KEY `package name` (`package`)
) ENGINE=InnoDB AUTO_INCREMENT=184 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `certificates` (
  `package` varchar(80) NOT NULL COMMENT 'Package name as extracted from apk',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of last change',
  `cert_version` int(1)  ,
  `cert_sig_algo` varchar(40)  ,
  `cert_issuer` varchar(200)  ,
  `cert_subject` varchar(200)  ,
  `cert_nb` varchar(50)   DEFAULT '0000-00-00 00:00:00' COMMENT 'validity: not before',
  `cert_na` varchar(50)   DEFAULT '0000-00-00 00:00:00' COMMENT 'validity not after',
  `cert_pka` varchar(50)  ,
  `cert_pkl` int(5)  ,
  `cert_sn` varchar(100)  ,
  UNIQUE KEY `package name` (`package`),
  CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `code_analysis`
--

DROP TABLE IF EXISTS `code_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `code_analysis` (
  `package` varchar(80) NOT NULL,
  `debuggable` varchar(1)   COMMENT 'App set as debuggable in manifest',
  `contentprovider_used` varchar(1)  ,
  `contentprovider_accessible` varchar(1)  ,
  `contentprovider_gives_medical_app` varchar(1)  ,
  `malware` int(1)   COMMENT 'Identified as malware or pup',
  UNIQUE KEY `package` (`package`),
  CONSTRAINT `code_analysis_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='stores results of source code analysis';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crypto`
--

DROP TABLE IF EXISTS `crypto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crypto` (
  `package` varchar(100) NOT NULL,
  `class` varchar(200)  ,
  `keyword` varchar(20)  ,
  `time` timestamp   DEFAULT CURRENT_TIMESTAMP,
  `obfuscation` int(1)   COMMENT 'Is Proguard obfuscation used in app',
  UNIQUE KEY `3tuple` (`package`,`class`,`keyword`),
  KEY `package` (`package`),
  CONSTRAINT `crypto_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Stores info about crypto usage of apps';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `findbugs`
--

DROP TABLE IF EXISTS `findbugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `findbugs` (
  `package` varchar(80) NOT NULL,
  `total_classes` int(7)  ,
  `total_size` int(10)  ,
  `total_bugs` int(7)  ,
  `priority_2` int(7)  ,
  `priority_1` int(7)  ,
  `native_total_bugs` int(7)  ,
  `native_total_size` int(10)  ,
  `native_priority_2` int(7)  ,
  `native_priority_1` int(7)  ,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `package` (`package`),
  CONSTRAINT `findbugs_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='stores summary of bugs found with findbugs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `findbugs_details`
--

DROP TABLE IF EXISTS `findbugs_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `findbugs_details` (
  `package` varchar(80) NOT NULL,
  `type` varchar(100)  ,
  `priority` int(1)  ,
  `abbrev` varchar(10)  ,
  `category` varchar(20)  ,
  `time` timestamp   DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_entry` (`package`,`type`,`priority`,`abbrev`,`category`),
  KEY `package` (`package`),
  CONSTRAINT `findbugs_details_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Stores details about bugs found with findbugs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gp`
--

DROP TABLE IF EXISTS `gp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gp` (
  `package` varchar(80) NOT NULL,
  `title` text,
  `category` text,
  `creator` text,
  `version` text,
  `versionstring` text,
  `size` text,
  `avRating` float NOT NULL,
  `oneRating` int(11) DEFAULT NULL,
  `twoRating` int(11) DEFAULT NULL,
  `threeRating` int(11) DEFAULT NULL,
  `fourRating` int(11) DEFAULT NULL,
  `fiveRating` int(11) DEFAULT NULL,
  `date` text COMMENT 'uploadDate',
  `description` text,
  `developerEmail` text,
  `developerWebsite` text,
  `numDownload` int(10) DEFAULT NULL,
  `price` text,
  `pripol` varchar(128) DEFAULT NULL,
  `source` varchar(128) DEFAULT NULL,
  `androidTargetVersion` text,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `package2` (`package`),
  KEY `package` (`package`),
  CONSTRAINT `gp_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mallodroid`
--

DROP TABLE IF EXISTS `mallodroid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mallodroid` (
  `package` varchar(100) NOT NULL,
  `mallo_text` text  ,
  `vuln_in` int(11) NOT NULL COMMENT '1 = vuln in 3rd party, 2 = vuln in own code, 3 = both',
  `vuln_package` varchar(100)  ,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `package` (`package`),
  CONSTRAINT `mallodroid_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uname` (`name`(100))
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pripol`
--

DROP TABLE IF EXISTS `pripol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pripol` (
  `package` varchar(80) NOT NULL,
  `URL` varchar(100)   COMMENT 'stores URL of privacy policy, uses -none- if not found',
  `NumWords` int(6)  ,
  `NumChars` int(6)   COMMENT 'stores number of non white space chars',
  `version` varchar(100)  ,
  `Country` varchar(3)  ,
  `AP` varchar(6)   COMMENT 'Accountability Principle: Data Controller named / detailed contact data given in privacy policy? (E-Mail only => partly)',
  `SSP` varchar(6)   COMMENT 'Security Safeguards Principle: security safeguards described?',
  `OP` varchar(6)   COMMENT 'Openness Principle: Types of Data collected described?',
  `PSP` varchar(6)   COMMENT 'Purpose Specification Principle: Purpose of data collection and usage of data described?',
  `IPP` varchar(6)   COMMENT 'Individual Participation Principle: rights of the individual described',
  `intUsage` varchar(6)   COMMENT 'Medical Data can be used for other internal purposes like  for marketing, research',
  `3rdPartyStorage` varchar(6)   COMMENT 'Data stored by third party',
  `Merger` varchar(6)   COMMENT 'Medical Data passed on in case of merger or acquisition',
  `3rdPartyForward` varchar(6)   COMMENT 'Medical Data can  be passed on to  other 3rd parties (other than required by law)',
  `quotes` longtext  ,
  `comments` longtext  ,
  KEY `package` (`package`),
  CONSTRAINT `pripol_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='stores results of privacy policy comparison';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
  `id` int(1) NOT NULL,
  `name` varchar(20) NOT NULL,
  `url` varchar(50)  ,
  `currency` varchar(10)  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `urls`
--

DROP TABLE IF EXISTS `urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `urls` (
  `package` varchar(100) NOT NULL,
  `url` varchar(200) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `unique package plus url` (`package`,`url`),
  KEY `package` (`package`),
  CONSTRAINT `urls_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `web_security`
--

DROP TABLE IF EXISTS `web_security`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `web_security` (
  `package` varchar(80) NOT NULL,
  `WebServerURL` varchar(100) NOT NULL,
  `Protocolused` varchar(10) NOT NULL COMMENT 'HTTP, HTTPS, Both',
  `MinimumPasswordLength` int(2)   COMMENT 'Number of characters',
  `SamplePassworrd` varchar(20)   COMMENT 'Example of valid password',
  `PasswordinCleartext` varchar(3)   COMMENT 'Password transmitted in Cleartext',
  `MedicalDatainCleartext` varchar(3)   COMMENT 'Medical Data in Cleartext (text or pictures)',
  `Comments` longtext  ,
  `time` timestamp   DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `package` (`package`),
  CONSTRAINT `web_security_ibfk_1` FOREIGN KEY (`package`) REFERENCES `apps` (`package`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Saves results of web security analysis';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-30 11:01:47
