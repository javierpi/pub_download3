-- MySQL dump 10.14  Distrib 5.5.59-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: pub_download
-- ------------------------------------------------------
-- Server version	5.5.59-MariaDB-1ubuntu0.14.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add nonce',7,'add_nonce'),(20,'Can change nonce',7,'change_nonce'),(21,'Can delete nonce',7,'delete_nonce'),(22,'Can add partial',8,'add_partial'),(23,'Can change partial',8,'change_partial'),(24,'Can delete partial',8,'delete_partial'),(25,'Can add association',9,'add_association'),(26,'Can change association',9,'change_association'),(27,'Can delete association',9,'delete_association'),(28,'Can add code',10,'add_code'),(29,'Can change code',10,'change_code'),(30,'Can delete code',10,'delete_code'),(31,'Can add user social auth',11,'add_usersocialauth'),(32,'Can change user social auth',11,'change_usersocialauth'),(33,'Can delete user social auth',11,'delete_usersocialauth'),(34,'Can add metric',12,'add_metric'),(35,'Can change metric',12,'change_metric'),(36,'Can delete metric',12,'delete_metric'),(37,'Can add domain',13,'add_domain'),(38,'Can change domain',13,'change_domain'),(39,'Can delete domain',13,'delete_domain'),(40,'Can add period',14,'add_period'),(41,'Can change period',14,'change_period'),(42,'Can delete period',14,'delete_period'),(43,'Can add google_service',15,'add_google_service'),(44,'Can change google_service',15,'change_google_service'),(45,'Can delete google_service',15,'delete_google_service'),(46,'Can add google_service',16,'add_google_service'),(47,'Can change google_service',16,'change_google_service'),(48,'Can delete google_service',16,'delete_google_service'),(49,'Can add period',17,'add_period'),(50,'Can change period',17,'change_period'),(51,'Can delete period',17,'delete_period'),(52,'Can add metric',18,'add_metric'),(53,'Can change metric',18,'change_metric'),(54,'Can delete metric',18,'delete_metric'),(55,'Can add domain',19,'add_domain'),(56,'Can change domain',19,'change_domain'),(57,'Can delete domain',19,'delete_domain');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$100000$EGoumKouuU8j$MNZ4qzBuZDTAV9tfa6LbGImu5XaIRpE5yWYievgLxt4=','2018-07-13 13:53:09',1,'deployer','','','',1,1,'2018-07-13 13:52:47');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-07-17 15:24:10','1','test',1,'[{\"added\": {}}]',13,1),(2,'2018-07-17 15:27:06','2','afsd',1,'[{\"added\": {}}]',13,1),(3,'2018-07-17 15:47:49','1','Period object (1)',1,'[{\"added\": {}}]',14,1),(4,'2018-07-17 16:52:56','2','Google Analytics',1,'[{\"added\": {}}]',15,1),(5,'2018-07-17 17:10:03','1','2018-06-01',1,'[{\"added\": {}}]',17,1),(6,'2018-07-17 17:10:47','1','Google Analytics',1,'[{\"added\": {}}]',16,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(13,'google_analytics','domain'),(15,'google_analytics','google_service'),(12,'google_analytics','metric'),(14,'google_analytics','period'),(19,'gug','domain'),(16,'gug','google_service'),(18,'gug','metric'),(17,'gug','period'),(6,'sessions','session'),(9,'social_django','association'),(10,'social_django','code'),(7,'social_django','nonce'),(8,'social_django','partial'),(11,'social_django','usersocialauth');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-07-13 13:50:13'),(2,'auth','0001_initial','2018-07-13 13:50:16'),(3,'admin','0001_initial','2018-07-13 13:50:16'),(4,'admin','0002_logentry_remove_auto_add','2018-07-13 13:50:16'),(5,'contenttypes','0002_remove_content_type_name','2018-07-13 13:50:16'),(6,'auth','0002_alter_permission_name_max_length','2018-07-13 13:50:16'),(7,'auth','0003_alter_user_email_max_length','2018-07-13 13:50:17'),(8,'auth','0004_alter_user_username_opts','2018-07-13 13:50:17'),(9,'auth','0005_alter_user_last_login_null','2018-07-13 13:50:17'),(10,'auth','0006_require_contenttypes_0002','2018-07-13 13:50:17'),(11,'auth','0007_alter_validators_add_error_messages','2018-07-13 13:50:17'),(12,'auth','0008_alter_user_username_max_length','2018-07-13 13:50:17'),(13,'auth','0009_alter_user_last_name_max_length','2018-07-13 13:50:17'),(14,'sessions','0001_initial','2018-07-13 13:50:17'),(15,'default','0001_initial','2018-07-13 15:06:13'),(16,'social_auth','0001_initial','2018-07-13 15:06:13'),(17,'default','0002_add_related_name','2018-07-13 15:06:13'),(18,'social_auth','0002_add_related_name','2018-07-13 15:06:13'),(19,'default','0003_alter_email_max_length','2018-07-13 15:06:13'),(20,'social_auth','0003_alter_email_max_length','2018-07-13 15:06:13'),(21,'default','0004_auto_20160423_0400','2018-07-13 15:06:13'),(22,'social_auth','0004_auto_20160423_0400','2018-07-13 15:06:13'),(23,'social_auth','0005_auto_20160727_2333','2018-07-13 15:06:14'),(24,'social_django','0006_partial','2018-07-13 15:06:14'),(25,'social_django','0007_code_timestamp','2018-07-13 15:06:14'),(26,'social_django','0008_partial_timestamp','2018-07-13 15:06:14'),(27,'social_django','0001_initial','2018-07-13 15:06:14'),(28,'social_django','0004_auto_20160423_0400','2018-07-13 15:06:14'),(29,'social_django','0005_auto_20160727_2333','2018-07-13 15:06:14'),(30,'social_django','0003_alter_email_max_length','2018-07-13 15:06:14'),(31,'social_django','0002_add_related_name','2018-07-13 15:06:14'),(32,'google_analytics','0001_initial','2018-07-17 15:17:22'),(33,'google_analytics','0002_period','2018-07-17 15:47:28'),(34,'google_analytics','0003_google_service','2018-07-17 16:48:47'),(35,'gug','0001_initial','2018-07-17 17:07:05');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2ib2fm7lihsq6qlqs5n3iv3oolsgt1ak','ZWE5NDYxYjMyOWFlMmVlMGEyZjEwMzIxYjVlODJkYmU0Y2RlNDMxOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJhMjMyYzc2ZGE2ZGQzYzY1ZTFlNDNjZDE5MDljZGFlMTk0YTFhNTk4In0=','2018-07-27 13:53:09');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `google_analytics_domain`
--

DROP TABLE IF EXISTS `google_analytics_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_analytics_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ref` (`ref`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `google_analytics_domain`
--

LOCK TABLES `google_analytics_domain` WRITE;
/*!40000 ALTER TABLE `google_analytics_domain` DISABLE KEYS */;
INSERT INTO `google_analytics_domain` VALUES (1,'AIzaSyDL3FAKOL6xSCkv00UbR_cb_z28NXX1X3w','test'),(2,'asd','afsd');
/*!40000 ALTER TABLE `google_analytics_domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `google_analytics_google_service`
--

DROP TABLE IF EXISTS `google_analytics_google_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_analytics_google_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `scope` varchar(200) NOT NULL,
  `discovery` varchar(200) NOT NULL,
  `secret_json` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `google_analytics_google_service`
--

LOCK TABLES `google_analytics_google_service` WRITE;
/*!40000 ALTER TABLE `google_analytics_google_service` DISABLE KEYS */;
INSERT INTO `google_analytics_google_service` VALUES (2,'Google Analytics','https://www.googleapis.com/auth/analytics.readonly','https://analyticsreporting.googleapis.com/$discovery/rest','{\r\n  \"type\": \"service_account\",\r\n  \"project_id\": \"downloadpublicaciones\",\r\n  \"private_key_id\": \"a610ebc17b1e0ca0d34f46bd97f8f2529d3119fa\",\r\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDAAXronhmyHJ6v\\ndPE/sjso1TgxBC2GabMn0gdM3V0gWtAT63M2MA8NBi4b8guzkeP/PpEmpwJfkkWF\\nsZUgjR/+lZx4zmiOsbC1JOHKD10+t5vch5hPep7ehSMAyKOS1WgqJsx0TbFkqVvB\\noH19U3L67ejaBdO6roLiCoF3Ok0nbMfrmaKPdoE+0sfem2hqmO5uHTVAtsk9BXmi\\nU64t2/hfOwj4N1iFvrTWXVrTQSdlyBJRASCqmjFVMD4FP21tV00heKe1FexvJSWx\\njD9SuBDJYZ4JKKJJKBVBxYE9KxX5C7KxBzQPUWnQs481QyBa+5TCaeWyf28qRc+s\\nPZSQkqZ5AgMBAAECggEAGjzpipm2SbZrAe+RWyK0PmV6vwoC3ZwaoR2spTaX2AjI\\n5/v0G8rP97fpO6TlL/YHCdWHONi4NI60xOsKRa87WMshnYmZVKyYCP0ABOB6Hcyx\\n9h4qdGv9g0t+x8fjQHi8ugvgwyDt1aNmGEzh8Ssi6oLx379NmnRoCtMkM4KKUhFo\\n/HN+vtUEwoIZgvIGDkNd4gy7QahZE6/6+6AvRvEd/InBzg3fpdBCjkomkutdl3hg\\nqpc8SaAsoBBeAlf8JTfxX+Z1v+pAag6lBXetcHp1ahUJAaw7EkgRCxqX153yfgOY\\ndXKXgvjH7wG5uzj1/0kfEJcEsvMWQc+lzVfymv0MnQKBgQDspI1Q9KrICMq9fDb7\\n08sr9+1m8xFi96B7gp392GPRKKKyeCwSD9aBoCGqC5tIrr7I61W1S+03QYGCtTlP\\nbtIeo7v0vOw67HPMzmWql/dlB33BySSu1UYoBVhJLfh30yCJ2IxRG3BN1x+hGX1W\\nyxuR22J7OtFBDxfVkJgkM8JpVQKBgQDPtjONndxzQXSDTCxwwRjywFGR/f20w7IU\\n3gm+6Jlrxu2Rimwk3FgOjNjP1AxjxLyL4SyBa4Ltpl+vWdQmoqcYU/cCGKDTgrvk\\nkIx3ub93XfkCva67btGsixiEHGGk41zzNGTDTqgp3btFQin1CGD6Dnd7cqmmjx9+\\n1eJ0fN34lQKBgQC3SC+nnwhTC/Qy1G0lmIFI2aqGzQYPV+l1H9JMVHfi/I0em1LO\\n3nNuTF8me/zWS3m61gK4+0iMPnEXklMEAbo+PuSJhnWUoaSC4Oz/NtpG5olxON/v\\nhYHj51fcvf0umVgfS5hKDW1q7I4z0TExsvf0fS2GciS2NgFoyKf9ihUuTQKBgQC4\\nYpSXFVh509QbLcaRfUipTYHbqG3MRqBSF9zs5Mw0uY1w0kE344YjvHJG44TwF9gM\\nECKS7J54WmW8YnCKr37HgNnXuYci233x40NekLxfuULwZPO0nSZyFbP4qr0fQ1ni\\n51K/cZakO5ofXCGkzABSWf9Ezb++BHVAAZwaLjJZlQKBgQCPrgeOVqKNrlJydp9E\\nDnEeT31FIqCIn1LI15GomapRok7qrRecrAAABI0mRwJpfPzOynKdCGKP1Zf74Yfb\\nsuBFfbLrBQkydQcghouQHMXIsSWgmeFP2j7PrhoOwwuFkc7Vw98TheUAByaC/+GC\\nhZ9fFVik/xt2d6sjQCydu0KPeQ==\\n-----END PRIVATE KEY-----\\n\",\r\n  \"client_email\": \"srv-acc-don@downloadpublicaciones.iam.gserviceaccount.com\",\r\n  \"client_id\": \"113439559357330901407\",\r\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\r\n  \"token_uri\": \"https://accounts.google.com/o/oauth2/token\",\r\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\r\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/srv-acc-don%40downloadpublicaciones.iam.gserviceaccount.com\"\r\n}');
/*!40000 ALTER TABLE `google_analytics_google_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `google_analytics_metric`
--

DROP TABLE IF EXISTS `google_analytics_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_analytics_metric` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `google_analytics_metric_domain_id_ref_5919e0d6_uniq` (`domain_id`,`ref`),
  CONSTRAINT `google_analytics_met_domain_id_59376227_fk_google_an` FOREIGN KEY (`domain_id`) REFERENCES `google_analytics_domain` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `google_analytics_metric`
--

LOCK TABLES `google_analytics_metric` WRITE;
/*!40000 ALTER TABLE `google_analytics_metric` DISABLE KEYS */;
/*!40000 ALTER TABLE `google_analytics_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `google_analytics_period`
--

DROP TABLE IF EXISTS `google_analytics_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `google_analytics_period` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `google_analytics_period`
--

LOCK TABLES `google_analytics_period` WRITE;
/*!40000 ALTER TABLE `google_analytics_period` DISABLE KEYS */;
INSERT INTO `google_analytics_period` VALUES (1,'2018-06-01','2018-06-30');
/*!40000 ALTER TABLE `google_analytics_period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gug_domain`
--

DROP TABLE IF EXISTS `gug_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gug_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ref` (`ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gug_domain`
--

LOCK TABLES `gug_domain` WRITE;
/*!40000 ALTER TABLE `gug_domain` DISABLE KEYS */;
/*!40000 ALTER TABLE `gug_domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gug_google_service`
--

DROP TABLE IF EXISTS `gug_google_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gug_google_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `scope` varchar(200) NOT NULL,
  `discovery` varchar(200) NOT NULL,
  `secret_json` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gug_google_service`
--

LOCK TABLES `gug_google_service` WRITE;
/*!40000 ALTER TABLE `gug_google_service` DISABLE KEYS */;
INSERT INTO `gug_google_service` VALUES (1,'Google Analytics','https://www.googleapis.com/auth/analytics.readonly','https://analyticsreporting.googleapis.com/$discovery/rest','{\r\n  \"type\": \"service_account\",\r\n  \"project_id\": \"downloadpublicaciones\",\r\n  \"private_key_id\": \"a610ebc17b1e0ca0d34f46bd97f8f2529d3119fa\",\r\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDAAXronhmyHJ6v\\ndPE/sjso1TgxBC2GabMn0gdM3V0gWtAT63M2MA8NBi4b8guzkeP/PpEmpwJfkkWF\\nsZUgjR/+lZx4zmiOsbC1JOHKD10+t5vch5hPep7ehSMAyKOS1WgqJsx0TbFkqVvB\\noH19U3L67ejaBdO6roLiCoF3Ok0nbMfrmaKPdoE+0sfem2hqmO5uHTVAtsk9BXmi\\nU64t2/hfOwj4N1iFvrTWXVrTQSdlyBJRASCqmjFVMD4FP21tV00heKe1FexvJSWx\\njD9SuBDJYZ4JKKJJKBVBxYE9KxX5C7KxBzQPUWnQs481QyBa+5TCaeWyf28qRc+s\\nPZSQkqZ5AgMBAAECggEAGjzpipm2SbZrAe+RWyK0PmV6vwoC3ZwaoR2spTaX2AjI\\n5/v0G8rP97fpO6TlL/YHCdWHONi4NI60xOsKRa87WMshnYmZVKyYCP0ABOB6Hcyx\\n9h4qdGv9g0t+x8fjQHi8ugvgwyDt1aNmGEzh8Ssi6oLx379NmnRoCtMkM4KKUhFo\\n/HN+vtUEwoIZgvIGDkNd4gy7QahZE6/6+6AvRvEd/InBzg3fpdBCjkomkutdl3hg\\nqpc8SaAsoBBeAlf8JTfxX+Z1v+pAag6lBXetcHp1ahUJAaw7EkgRCxqX153yfgOY\\ndXKXgvjH7wG5uzj1/0kfEJcEsvMWQc+lzVfymv0MnQKBgQDspI1Q9KrICMq9fDb7\\n08sr9+1m8xFi96B7gp392GPRKKKyeCwSD9aBoCGqC5tIrr7I61W1S+03QYGCtTlP\\nbtIeo7v0vOw67HPMzmWql/dlB33BySSu1UYoBVhJLfh30yCJ2IxRG3BN1x+hGX1W\\nyxuR22J7OtFBDxfVkJgkM8JpVQKBgQDPtjONndxzQXSDTCxwwRjywFGR/f20w7IU\\n3gm+6Jlrxu2Rimwk3FgOjNjP1AxjxLyL4SyBa4Ltpl+vWdQmoqcYU/cCGKDTgrvk\\nkIx3ub93XfkCva67btGsixiEHGGk41zzNGTDTqgp3btFQin1CGD6Dnd7cqmmjx9+\\n1eJ0fN34lQKBgQC3SC+nnwhTC/Qy1G0lmIFI2aqGzQYPV+l1H9JMVHfi/I0em1LO\\n3nNuTF8me/zWS3m61gK4+0iMPnEXklMEAbo+PuSJhnWUoaSC4Oz/NtpG5olxON/v\\nhYHj51fcvf0umVgfS5hKDW1q7I4z0TExsvf0fS2GciS2NgFoyKf9ihUuTQKBgQC4\\nYpSXFVh509QbLcaRfUipTYHbqG3MRqBSF9zs5Mw0uY1w0kE344YjvHJG44TwF9gM\\nECKS7J54WmW8YnCKr37HgNnXuYci233x40NekLxfuULwZPO0nSZyFbP4qr0fQ1ni\\n51K/cZakO5ofXCGkzABSWf9Ezb++BHVAAZwaLjJZlQKBgQCPrgeOVqKNrlJydp9E\\nDnEeT31FIqCIn1LI15GomapRok7qrRecrAAABI0mRwJpfPzOynKdCGKP1Zf74Yfb\\nsuBFfbLrBQkydQcghouQHMXIsSWgmeFP2j7PrhoOwwuFkc7Vw98TheUAByaC/+GC\\nhZ9fFVik/xt2d6sjQCydu0KPeQ==\\n-----END PRIVATE KEY-----\\n\",\r\n  \"client_email\": \"srv-acc-don@downloadpublicaciones.iam.gserviceaccount.com\",\r\n  \"client_id\": \"113439559357330901407\",\r\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\r\n  \"token_uri\": \"https://accounts.google.com/o/oauth2/token\",\r\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\r\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/srv-acc-don%40downloadpublicaciones.iam.gserviceaccount.com\"\r\n}');
/*!40000 ALTER TABLE `gug_google_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gug_metric`
--

DROP TABLE IF EXISTS `gug_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gug_metric` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gug_metric_domain_id_ref_31ae578c_uniq` (`domain_id`,`ref`),
  CONSTRAINT `gug_metric_domain_id_0902e03d_fk_gug_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `gug_domain` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gug_metric`
--

LOCK TABLES `gug_metric` WRITE;
/*!40000 ALTER TABLE `gug_metric` DISABLE KEYS */;
/*!40000 ALTER TABLE `gug_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gug_period`
--

DROP TABLE IF EXISTS `gug_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gug_period` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gug_period`
--

LOCK TABLES `gug_period` WRITE;
/*!40000 ALTER TABLE `gug_period` DISABLE KEYS */;
INSERT INTO `gug_period` VALUES (1,'2018-06-01','2018-06-30');
/*!40000 ALTER TABLE `gug_period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_association`
--

LOCK TABLES `social_auth_association` WRITE;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_code`
--

DROP TABLE IF EXISTS `social_auth_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  KEY `social_auth_code_code_a2393167` (`code`),
  KEY `social_auth_code_timestamp_176b341f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_code`
--

LOCK TABLES `social_auth_code` WRITE;
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_nonce`
--

LOCK TABLES `social_auth_nonce` WRITE;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_partial`
--

DROP TABLE IF EXISTS `social_auth_partial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_partial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(32) NOT NULL,
  `next_step` smallint(5) unsigned NOT NULL,
  `backend` varchar(32) NOT NULL,
  `data` longtext NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `social_auth_partial_token_3017fea3` (`token`),
  KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_partial`
--

LOCK TABLES `social_auth_partial` WRITE;
/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` (`user_id`),
  CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_usersocialauth`
--

LOCK TABLES `social_auth_usersocialauth` WRITE;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-17 13:14:22
