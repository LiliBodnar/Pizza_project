-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: PizzaProject
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `AccountID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Password` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`AccountID`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (2,'firstcustomer@gmail.com','strongpassword'),(3,'birthdaygirl','happybirthday');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `area` (
  `AreaID` int NOT NULL AUTO_INCREMENT,
  `PostalCode` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`AreaID`),
  UNIQUE KEY `PostalCode` (`PostalCode`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area`
--

LOCK TABLES `area` WRITE;
/*!40000 ALTER TABLE `area` DISABLE KEYS */;
INSERT INTO `area` VALUES (3,'1122TF'),(4,'1234'),(2,'2345HD');
/*!40000 ALTER TABLE `area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `CouponID` int NOT NULL AUTO_INCREMENT,
  `CouponCode` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `DiscountPercentage` decimal(5,2) NOT NULL,
  `ExpirationDate` date DEFAULT NULL,
  `Used` bit(1) DEFAULT b'0',
  PRIMARY KEY (`CouponID`),
  UNIQUE KEY `CouponCode` (`CouponCode`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

LOCK TABLES `coupons` WRITE;
/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
INSERT INTO `coupons` VALUES (1,'fc123',5.00,'2024-12-01',_binary '\0'),(2,'fc111',10.00,'2024-12-01',_binary '\0');
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `LastName` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Gender` char(1) DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `Phone` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `NumberOfPizzas` int DEFAULT NULL,
  `AccountID` int DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  KEY `AccountID` (`AccountID`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (2,'First','Customer','f','2024-10-01','914091343',NULL,2),(3,'sarah','clark','f','2024-10-06','456387234',NULL,3);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customerdeliveryaddress`
--

DROP TABLE IF EXISTS `customerdeliveryaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customerdeliveryaddress` (
  `DeliveryAddressID` int NOT NULL,
  `CustomerID` int NOT NULL,
  PRIMARY KEY (`CustomerID`,`DeliveryAddressID`),
  KEY `DeliveryAddressID` (`DeliveryAddressID`),
  CONSTRAINT `customerdeliveryaddress_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  CONSTRAINT `customerdeliveryaddress_ibfk_2` FOREIGN KEY (`DeliveryAddressID`) REFERENCES `deliveryaddress` (`DeliveryAddressID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customerdeliveryaddress`
--

LOCK TABLES `customerdeliveryaddress` WRITE;
/*!40000 ALTER TABLE `customerdeliveryaddress` DISABLE KEYS */;
INSERT INTO `customerdeliveryaddress` VALUES (3,2),(4,3),(5,2);
/*!40000 ALTER TABLE `customerdeliveryaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `LastName` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Gender` char(1) DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `Phone` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `AccountID` int DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  KEY `AccountID` (`AccountID`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`AccountID`) REFERENCES `account` (`AccountID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custompizzaingredients`
--

DROP TABLE IF EXISTS `custompizzaingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `custompizzaingredients` (
  `CustomPizzaID` int NOT NULL AUTO_INCREMENT,
  `OrderItemID` int DEFAULT NULL,
  `IngredientID` int DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  PRIMARY KEY (`CustomPizzaID`),
  KEY `OrderItemID` (`OrderItemID`),
  KEY `IngredientID` (`IngredientID`),
  CONSTRAINT `custompizzaingredients_ibfk_1` FOREIGN KEY (`OrderItemID`) REFERENCES `orderitem` (`OrderItemID`),
  CONSTRAINT `custompizzaingredients_ibfk_2` FOREIGN KEY (`IngredientID`) REFERENCES `ingredient` (`IngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custompizzaingredients`
--

LOCK TABLES `custompizzaingredients` WRITE;
/*!40000 ALTER TABLE `custompizzaingredients` DISABLE KEYS */;
INSERT INTO `custompizzaingredients` VALUES (1,34,2,1),(2,34,8,1),(3,37,1,1),(4,37,8,1),(5,40,1,1);
/*!40000 ALTER TABLE `custompizzaingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliveryaddress`
--

DROP TABLE IF EXISTS `deliveryaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveryaddress` (
  `DeliveryAddressID` int NOT NULL AUTO_INCREMENT,
  `StreetName` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `HouseNumber` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `PostalCode` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`DeliveryAddressID`),
  KEY `PostalCode` (`PostalCode`),
  CONSTRAINT `deliveryaddress_ibfk_1` FOREIGN KEY (`PostalCode`) REFERENCES `area` (`PostalCode`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveryaddress`
--

LOCK TABLES `deliveryaddress` WRITE;
/*!40000 ALTER TABLE `deliveryaddress` DISABLE KEYS */;
INSERT INTO `deliveryaddress` VALUES (3,'Cornelia Street','1','2345HD'),(4,'super street','23','1122TF'),(5,'newaddress','11','1234');
/*!40000 ALTER TABLE `deliveryaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliveryperson`
--

DROP TABLE IF EXISTS `deliveryperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveryperson` (
  `DeliveryPersonID` int NOT NULL AUTO_INCREMENT,
  `Availability` enum('Available','Not available') DEFAULT NULL,
  PRIMARY KEY (`DeliveryPersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveryperson`
--

LOCK TABLES `deliveryperson` WRITE;
/*!40000 ALTER TABLE `deliveryperson` DISABLE KEYS */;
/*!40000 ALTER TABLE `deliveryperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliverypersonarea`
--

DROP TABLE IF EXISTS `deliverypersonarea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliverypersonarea` (
  `DeliveryPersonID` int NOT NULL,
  `AreaID` int NOT NULL,
  PRIMARY KEY (`DeliveryPersonID`,`AreaID`),
  KEY `AreaID` (`AreaID`),
  CONSTRAINT `deliverypersonarea_ibfk_1` FOREIGN KEY (`DeliveryPersonID`) REFERENCES `deliveryperson` (`DeliveryPersonID`),
  CONSTRAINT `deliverypersonarea_ibfk_2` FOREIGN KEY (`AreaID`) REFERENCES `area` (`AreaID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliverypersonarea`
--

LOCK TABLES `deliverypersonarea` WRITE;
/*!40000 ALTER TABLE `deliverypersonarea` DISABLE KEYS */;
/*!40000 ALTER TABLE `deliverypersonarea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient` (
  `IngredientID` int NOT NULL AUTO_INCREMENT,
  `IngredientName` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`IngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Dough',4.00),(2,'Calzone base',4.50),(3,'Tomato Sauce',1.00),(4,'Mozzarella',2.00),(5,'Vegan cheese',3.00),(6,'Pepperoni',3.00),(7,'BBQ Sauce',1.20),(8,'Grilled Chicken',3.50),(9,'Bell Peppers',1.00),(10,'Mushrooms',1.00),(11,'Onions',0.50),(12,'Bacon',2.50),(13,'Ham',2.50),(14,'Hot Sausage',3.50),(15,'Blue Cheese',2.50),(16,'Robiola Cheese',2.50),(17,'Gruyère Cheese',2.50),(18,'Pecorino Cheese',2.50),(19,'Pineapple',1.00),(20,'Cola',2.50),(21,'Lemonade',2.80),(22,'Water',1.50),(23,'Iced Tea',2.50),(24,'Tiramisu',4.80),(25,'Cheesecake',5.50),(26,'Chocolate Cake',4.20),(27,'Vanilla Ice Cream',5.00);
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredientlist`
--

DROP TABLE IF EXISTS `ingredientlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredientlist` (
  `IngredientListID` int NOT NULL AUTO_INCREMENT,
  `ItemID` int DEFAULT NULL,
  `IngredientID` int DEFAULT NULL,
  PRIMARY KEY (`IngredientListID`),
  KEY `ItemID` (`ItemID`),
  KEY `IngredientID` (`IngredientID`),
  CONSTRAINT `ingredientlist_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`),
  CONSTRAINT `ingredientlist_ibfk_2` FOREIGN KEY (`IngredientID`) REFERENCES `ingredient` (`IngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredientlist`
--

LOCK TABLES `ingredientlist` WRITE;
/*!40000 ALTER TABLE `ingredientlist` DISABLE KEYS */;
INSERT INTO `ingredientlist` VALUES (1,1,1),(2,1,3),(3,1,4),(4,2,1),(5,2,3),(6,2,4),(7,2,6),(8,3,1),(9,3,3),(10,3,4),(11,3,7),(12,3,8),(13,4,1),(14,4,3),(15,4,4),(16,4,9),(17,4,10),(18,4,11),(19,5,1),(20,5,3),(21,5,4),(22,5,6),(23,5,12),(24,5,13),(25,5,14),(26,6,1),(27,6,3),(28,6,4),(29,6,13),(30,7,1),(31,7,3),(32,7,15),(33,7,16),(34,7,17),(35,7,18),(36,8,1),(37,8,3),(38,8,4),(39,8,13),(40,8,19),(41,10,20),(42,11,21),(43,12,22),(44,13,23),(45,14,24),(46,15,25),(47,16,26),(48,17,27);
/*!40000 ALTER TABLE `ingredientlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredienttype`
--

DROP TABLE IF EXISTS `ingredienttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredienttype` (
  `IngredientID` int DEFAULT NULL,
  `RestrictionTypeID` int DEFAULT NULL,
  KEY `IngredientID` (`IngredientID`),
  KEY `RestrictionTypeID` (`RestrictionTypeID`),
  CONSTRAINT `ingredienttype_ibfk_1` FOREIGN KEY (`IngredientID`) REFERENCES `ingredient` (`IngredientID`),
  CONSTRAINT `ingredienttype_ibfk_2` FOREIGN KEY (`RestrictionTypeID`) REFERENCES `restrictiontype` (`RestrictionTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredienttype`
--

LOCK TABLES `ingredienttype` WRITE;
/*!40000 ALTER TABLE `ingredienttype` DISABLE KEYS */;
INSERT INTO `ingredienttype` VALUES (1,5),(2,5),(3,16),(4,6),(5,16),(6,1),(7,16),(8,1),(9,16),(10,16),(11,16),(12,1),(13,1),(14,1),(15,5),(16,5),(17,5),(18,5),(19,16),(20,16),(21,16),(22,16),(23,16),(24,7),(25,7),(26,7),(27,7);
/*!40000 ALTER TABLE `ingredienttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `ItemID` int NOT NULL AUTO_INCREMENT,
  `ItemName` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ItemType` enum('Pizza','Drink','Dessert') DEFAULT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'Margherita','Pizza'),(2,'Pepperoni','Pizza'),(3,'BBQ Chicken','Pizza'),(4,'Vegetarian','Pizza'),(5,'Meat Lover','Pizza'),(6,'Ham and Cheese','Pizza'),(7,'Quattro Formaggi','Pizza'),(8,'Hawaiian','Pizza'),(9,'Personalized Pizza','Pizza'),(10,'Cola','Drink'),(11,'Lemonade','Drink'),(12,'Water','Drink'),(13,'Iced Tea','Drink'),(14,'Tiramisu','Dessert'),(15,'Cheesecake','Dessert'),(16,'Chocolate Cake','Dessert'),(17,'Vanilla Ice Cream','Dessert');
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int DEFAULT NULL,
  `DeliveryAddressID` int DEFAULT NULL,
  `OrderStatus` enum('In processing','Being Prepared','On the way','Delivered') DEFAULT 'In processing',
  `OrderPlacementTime` datetime DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `CustomerID` (`CustomerID`),
  KEY `DeliveryAddressID` (`DeliveryAddressID`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`DeliveryAddressID`) REFERENCES `deliveryaddress` (`DeliveryAddressID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (5,2,NULL,'Being Prepared','2024-10-07 18:26:45'),(6,2,NULL,'Being Prepared','2024-10-07 18:45:42'),(13,2,NULL,'In processing','2024-10-07 20:50:56'),(14,2,NULL,'In processing','2024-10-07 20:52:53'),(15,2,NULL,'In processing','2024-10-07 20:54:44'),(17,2,NULL,'In processing','2024-10-07 21:08:34'),(18,2,NULL,'In processing','2024-10-07 21:19:07'),(21,2,NULL,'In processing','2024-10-07 21:35:04'),(22,2,NULL,'In processing','2024-10-07 21:43:05'),(23,2,3,'In processing','2024-10-08 11:51:25'),(24,2,3,'In processing','2024-10-08 11:53:03'),(25,2,3,'In processing','2024-10-08 11:54:31'),(26,2,3,'In processing','2024-10-08 12:00:31'),(27,2,3,'In processing','2024-10-08 12:05:20'),(28,2,3,'In processing','2024-10-08 12:07:28'),(29,2,3,'In processing','2024-10-08 12:10:44'),(30,2,3,'In processing','2024-10-08 12:15:17'),(31,2,3,'In processing','2024-10-08 12:19:33'),(32,2,3,'In processing','2024-10-08 12:21:06');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderdelivery`
--

DROP TABLE IF EXISTS `orderdelivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderdelivery` (
  `OrderID` int DEFAULT NULL,
  `DeliveryPersonID` int DEFAULT NULL,
  `DeliveryStartTime` datetime DEFAULT NULL,
  `EstimatedDeliveryTime` datetime DEFAULT NULL,
  KEY `OrderID` (`OrderID`),
  KEY `DeliveryPersonID` (`DeliveryPersonID`),
  CONSTRAINT `orderdelivery_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`),
  CONSTRAINT `orderdelivery_ibfk_2` FOREIGN KEY (`DeliveryPersonID`) REFERENCES `deliveryperson` (`DeliveryPersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderdelivery`
--

LOCK TABLES `orderdelivery` WRITE;
/*!40000 ALTER TABLE `orderdelivery` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderdelivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `OrderID` int DEFAULT NULL,
  `ItemID` int DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `OrderItemID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`OrderItemID`),
  KEY `fk_order` (`OrderID`),
  KEY `fk_item` (`ItemID`),
  CONSTRAINT `fk_item` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`),
  CONSTRAINT `fk_order` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`),
  CONSTRAINT `orderitem_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `order` (`OrderID`),
  CONSTRAINT `orderitem_ibfk_2` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitem`
--

LOCK TABLES `orderitem` WRITE;
/*!40000 ALTER TABLE `orderitem` DISABLE KEYS */;
INSERT INTO `orderitem` VALUES (5,1,1,5),(6,1,1,6),(13,1,1,13),(14,1,1,14),(15,1,1,15),(17,1,1,17),(18,1,1,18),(21,1,1,21),(22,1,1,22),(23,1,1,23),(23,14,1,24),(24,1,1,25),(24,14,1,26),(25,1,1,27),(25,14,1,28),(26,1,1,29),(26,14,1,30),(27,1,1,31),(27,14,1,32),(29,9,1,34),(29,10,1,35),(30,1,1,36),(30,9,1,37),(30,10,1,38),(31,1,1,39),(31,9,1,40),(32,1,1,41);
/*!40000 ALTER TABLE `orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restrictiontype`
--

DROP TABLE IF EXISTS `restrictiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restrictiontype` (
  `RestrictionTypeID` int NOT NULL AUTO_INCREMENT,
  `Vegan` bit(1) DEFAULT NULL,
  `Vegetarian` bit(1) DEFAULT NULL,
  `GlutenFree` bit(1) DEFAULT NULL,
  `LactoseFree` bit(1) DEFAULT NULL,
  PRIMARY KEY (`RestrictionTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restrictiontype`
--

LOCK TABLES `restrictiontype` WRITE;
/*!40000 ALTER TABLE `restrictiontype` DISABLE KEYS */;
INSERT INTO `restrictiontype` VALUES (1,_binary '\0',_binary '\0',_binary '\0',_binary '\0'),(2,_binary '\0',_binary '\0',_binary '\0',_binary ''),(3,_binary '\0',_binary '\0',_binary '',_binary '\0'),(4,_binary '\0',_binary '\0',_binary '',_binary ''),(5,_binary '\0',_binary '',_binary '\0',_binary '\0'),(6,_binary '\0',_binary '',_binary '\0',_binary ''),(7,_binary '\0',_binary '',_binary '',_binary '\0'),(8,_binary '\0',_binary '',_binary '',_binary ''),(9,_binary '',_binary '\0',_binary '\0',_binary '\0'),(10,_binary '',_binary '\0',_binary '\0',_binary ''),(11,_binary '',_binary '\0',_binary '',_binary '\0'),(12,_binary '',_binary '\0',_binary '',_binary ''),(13,_binary '',_binary '',_binary '\0',_binary '\0'),(14,_binary '',_binary '',_binary '\0',_binary ''),(15,_binary '',_binary '',_binary '',_binary '\0'),(16,_binary '',_binary '',_binary '',_binary '');
/*!40000 ALTER TABLE `restrictiontype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-08 12:28:13
