-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: air_ms
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `flight_view`
--

DROP TABLE IF EXISTS `flight_view`;
/*!50001 DROP VIEW IF EXISTS `flight_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `flight_view` AS SELECT 
 1 AS `flight_id`,
 1 AS `dep_iata`,
 1 AS `dep_city`,
 1 AS `dep_airport_name`,
 1 AS `arr_iata`,
 1 AS `arr_city`,
 1 AS `arr_airport_name`,
 1 AS `dep_time`,
 1 AS `arr_time`,
 1 AS `air_company`,
 1 AS `aircraft_type`,
 1 AS `flight_date`,
 1 AS `ft_left`,
 1 AS `ft_price`,
 1 AS `ct_left`,
 1 AS `ct_price`,
 1 AS `yt_left`,
 1 AS `yt_price`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `flight_view`
--

/*!50001 DROP VIEW IF EXISTS `flight_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `flight_view` (`flight_id`,`dep_iata`,`dep_city`,`dep_airport_name`,`arr_iata`,`arr_city`,`arr_airport_name`,`dep_time`,`arr_time`,`air_company`,`aircraft_type`,`flight_date`,`ft_left`,`ft_price`,`ct_left`,`ct_price`,`yt_left`,`yt_price`) AS select `flight_info`.`flight_id` AS `flight_id`,`flight_info`.`dep_iata` AS `dep_iata`,`c1`.`city` AS `city`,`c1`.`airport_name` AS `airport_name`,`flight_info`.`arr_iata` AS `arr_iata`,`c2`.`city` AS `city`,`c2`.`airport_name` AS `airport_name`,`flight_info`.`dep_time` AS `dep_time`,`flight_info`.`arr_time` AS `arr_time`,`flight_info`.`air_company` AS `air_company`,`flight_info`.`aircraft_type` AS `aircraft_type`,`standby_ticket_info`.`flight_date` AS `flight_date`,`standby_ticket_info`.`ft_left` AS `ft_left`,`standby_ticket_info`.`ft_price` AS `ft_price`,`standby_ticket_info`.`ct_left` AS `ct_left`,`standby_ticket_info`.`ct_price` AS `ct_price`,`standby_ticket_info`.`yt_left` AS `yt_left`,`standby_ticket_info`.`yt_price` AS `yt_price` from (((`flight_info` join `city_airport_info` `c1`) join `city_airport_info` `c2`) join `standby_ticket_info`) where ((`flight_info`.`flight_id` = `standby_ticket_info`.`flight_id`) and (`flight_info`.`dep_iata` = `c1`.`airport_iata`) and (`flight_info`.`arr_iata` = `c2`.`airport_iata`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-01  4:20:06
