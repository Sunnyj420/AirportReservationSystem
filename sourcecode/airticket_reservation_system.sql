-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 08, 2022 at 06:59 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airticket_reservation_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
CREATE TABLE IF NOT EXISTS `airline` (
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

DROP TABLE IF EXISTS `airline_staff`;
CREATE TABLE IF NOT EXISTS `airline_staff` (
  `username` varchar(20) NOT NULL,
  `airline` varchar(20) DEFAULT NULL,
  `pass_word` varchar(100) DEFAULT NULL,
  `firstname` varchar(20) DEFAULT NULL,
  `lastname` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `airline` (`airline`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `airline`, `pass_word`, `firstname`, `lastname`, `date_of_birth`) VALUES
('avasmith52', 'NULL', '289dff07669d7a23de0ef88d2f7129e7', 'NULL', 'NULL', '1000-01-01'),
('jamessmith8', 'Jet Blue', '99c5e07b4d5de9d18c350cdf64c5aa3d', 'James', 'Smith', '1990-11-04');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff_email`
--

DROP TABLE IF EXISTS `airline_staff_email`;
CREATE TABLE IF NOT EXISTS `airline_staff_email` (
  `username` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`username`,`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_staff_email`
--

INSERT INTO `airline_staff_email` (`username`, `email`) VALUES
('jamessmith8', 'jamessmith8@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff_phone_number`
--

DROP TABLE IF EXISTS `airline_staff_phone_number`;
CREATE TABLE IF NOT EXISTS `airline_staff_phone_number` (
  `username` varchar(20) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`username`,`phone_number`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_staff_phone_number`
--

INSERT INTO `airline_staff_phone_number` (`username`, `phone_number`) VALUES
('avasmith52', '4586231548'),
('avasmith52', '9824658521'),
('jamessmith8', '6561452365');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

DROP TABLE IF EXISTS `airplane`;
CREATE TABLE IF NOT EXISTS `airplane` (
  `airline` varchar(20) NOT NULL,
  `airplane_id` varchar(20) NOT NULL,
  `num_of_seats` int(11) DEFAULT NULL,
  `manufacturing_company` varchar(40) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`airline`,`airplane_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline`, `airplane_id`, `num_of_seats`, `manufacturing_company`, `age`) VALUES
('Jet Blue', 'JB1', 130, 'Boeing', 5),
('Jet Blue', 'JB2', 150, 'Boeing', 1),
('Jet Blue', 'JB3', 140, 'Airbus', 12),
('Jet Blue', 'JB4', 100, 'Airbus', 7);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `name` varchar(20) NOT NULL,
  `city` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `airport_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`name`, `city`, `country`, `airport_type`) VALUES
('JFK', 'NYC', 'United States', 'Both'),
('PVG', 'Shanghai', 'China', 'Both'),
('LGA', 'NYC', 'United States', 'Both');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `email` varchar(50) NOT NULL,
  `pass_word` varchar(100) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `address_building_number` varchar(20) DEFAULT NULL,
  `address_street` varchar(100) DEFAULT NULL,
  `address_city` varchar(20) DEFAULT NULL,
  `address_state` varchar(20) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `pass_word`, `name`, `address_building_number`, `address_street`, `address_city`, `address_state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('ay2095@nyu.edu', '202cb962ac59075b964b07152d234b70', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', '1000-01-01', 'NULL', '1000-01-01'),
('kv932@nyu.edu', '250cf8b51c773f3f8dc8b4be867a9a02', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', '1000-01-01', 'NULL', '1000-01-01'),
('sj3048@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Sunny Jeong', '211', '101 Johnson Street', 'Brooklyn', 'New York', '3322629200', 'M12341234', '2024-12-12', 'Korea', '1234-12-12');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
CREATE TABLE IF NOT EXISTS `flight` (
  `airline` varchar(20) NOT NULL,
  `flight_number` int(11) NOT NULL,
  `departure_airport` varchar(20) DEFAULT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_airport` varchar(20) DEFAULT NULL,
  `arrival_date` date DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `base_price` decimal(10,2) DEFAULT NULL,
  `airplane_id` varchar(20) DEFAULT NULL,
  `flight_status` varchar(20) DEFAULT NULL,
  `seatCapacity` int(11) DEFAULT NULL,
  PRIMARY KEY (`airline`,`flight_number`,`departure_date`,`departure_time`),
  KEY `departure_airport` (`departure_airport`),
  KEY `arrival_airport` (`arrival_airport`),
  KEY `airplane_id` (`airplane_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline`, `flight_number`, `departure_airport`, `departure_date`, `departure_time`, `arrival_airport`, `arrival_date`, `arrival_time`, `base_price`, `airplane_id`, `flight_status`, `seatCapacity`) VALUES
('Jet Blue', 1000, 'JFK', '2022-12-25', '09:00:00', 'PVG', '2022-12-26', '12:00:00', '500.50', 'JB2', 'On time', NULL),
('Jet Blue', 2500, 'JFK', '2022-11-15', '03:30:00', 'PVG', '2022-11-16', '06:30:00', '420.75', 'JB1', 'On time', NULL),
('Jet Blue', 5000, 'PVG', '2021-11-10', '08:30:00', 'JFK', '2021-11-11', '11:30:00', '200.00', 'JB3', 'Canceled', NULL),
('Jet Blue', 6500, 'PVG', '2020-05-21', '01:00:00', 'JFK', '2020-05-22', '04:00:00', '150.50', 'JB1', 'On time', 0),
('Jet Blue', 1500, 'JFK', '2022-11-06', '07:30:00', 'PVG', '2022-11-07', '10:30:00', '800.99', 'JB2', 'Delayed', NULL),
('Jet Blue', 3000, 'JFK', '2022-12-04', '03:30:00', 'PVG', '2022-12-04', '10:00:00', '620.15', 'JB3', 'On time', NULL),
('Jet Blue', 4000, 'JFK', '2023-12-25', '09:00:00', 'PVG', '2023-12-26', '12:00:00', '1000.50', 'JB3', 'On time', 140);

-- --------------------------------------------------------

--
-- Table structure for table `rates`
--

DROP TABLE IF EXISTS `rates`;
CREATE TABLE IF NOT EXISTS `rates` (
  `flight_number` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `email` varchar(50) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `comments` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`flight_number`,`departure_date`,`departure_time`,`email`),
  KEY `departure_date` (`departure_date`),
  KEY `departure_time` (`departure_time`),
  KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rates`
--

INSERT INTO `rates` (`flight_number`, `departure_date`, `departure_time`, `email`, `rating`, `comments`) VALUES
(2500, '2022-11-15', '03:30:00', 'ay2095@nyu.edu', 2, 'Poor service'),
(2500, '2022-11-15', '03:30:00', 'kv932@nyu.edu', 1, 'Horrible turbulence');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `t_id` varchar(20) NOT NULL,
  `airline` varchar(20) DEFAULT NULL,
  `flight_number` int(11) DEFAULT NULL,
  `departure_date` date DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `c_email` varchar(50) DEFAULT NULL,
  `sold_price` decimal(10,2) DEFAULT NULL,
  `payment_info_card_type` varchar(20) DEFAULT NULL,
  `payment_info_card_number` varchar(50) DEFAULT NULL,
  `payment_info_name_on_card` varchar(20) DEFAULT NULL,
  `payment_info_expiration_date` date DEFAULT NULL,
  `curr_date` date DEFAULT NULL,
  `curr_time` time DEFAULT NULL,
  PRIMARY KEY (`t_id`),
  KEY `flight_number` (`flight_number`),
  KEY `departure_date` (`departure_date`),
  KEY `departure_time` (`departure_time`),
  KEY `c_email` (`c_email`),
  KEY `airline` (`airline`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`t_id`, `airline`, `flight_number`, `departure_date`, `departure_time`, `c_email`, `sold_price`, `payment_info_card_type`, `payment_info_card_number`, `payment_info_name_on_card`, `payment_info_expiration_date`, `curr_date`, `curr_time`) VALUES
('3230', 'Jet Blue', 2500, '2022-11-15', '03:30:00', 'ay2095@nyu.edu', '420.75', 'Visa', '0', 'Angela Yeung', '2025-01-01', '2022-12-03', '06:40:00'),
('8433', 'Jet Blue', 2500, '2022-11-15', '03:30:00', 'sj3048@nyu.edu', '550.00', 'Visa', '295355', 'Sunny Jeong', '2026-10-30', '2022-10-01', '06:30:00'),
('3515', 'Jet Blue', 6500, '2020-05-21', '01:00:00', 'ay2095@nyu.edu', '150.50', 'American Express', '654892', 'Angela Yeung', '2023-11-15', '2022-12-04', '03:17:55'),
('4715', 'Jet Blue', 5000, '2021-11-10', '08:30:00', 'kv932@nyu.edu', '200.00', 'MasterCard', '112', 'Ketan Vanjani', '2026-06-01', '2022-12-03', '07:20:00'),
('337', 'Jet Blue', 2500, '2022-11-15', '03:30:00', 'kv932@nyu.edu', '420.75', 'MasterCard', '112', 'Ketan Vanjani', '2026-06-01', '2022-12-03', '07:20:00'),
('6548', 'Jet Blue', 6500, '2020-05-21', '01:00:00', 'ay2095@nyu.edu', '1060.00', 'Visa', '156165', 'Angela Yeung', '2026-10-30', '2022-11-01', '06:30:00'),
('8855', 'Jet Blue', 6500, '2020-05-21', '01:00:00', 'kv932@nyu.edu', '560.00', 'Visa', '1561-6544-1111-2548', 'Ketan Vanjani', '2023-10-30', '2019-11-01', '06:30:00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
