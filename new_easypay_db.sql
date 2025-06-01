-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: May 28, 2025 at 10:23 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `new_easypay_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `transaction_type` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `recipient` varchar(255) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `sender_phone` varchar(20) DEFAULT NULL,
  `recipient_phone` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `transaction_type`, `amount`, `recipient`, `details`, `date`, `sender_phone`, `recipient_phone`) VALUES
(1, 'Send Money', -250.00, 'cris manzano (09638222990)', NULL, '2025-05-23 04:41:11', NULL, NULL),
(2, 'Send Money', -500.00, 'keren loayon (09784136264)', NULL, '2025-05-23 04:44:47', NULL, NULL),
(3, 'Send Money', -100.00, 'cris estal (09874545465)', NULL, '2025-05-23 04:49:28', NULL, NULL),
(4, 'Send Money', -250.00, 'keren loayon (09784136264)', NULL, '2025-05-23 04:50:39', NULL, NULL),
(5, 'Send Money', -250.00, 'keren loayon (09784136264)', NULL, '2025-05-23 04:51:05', NULL, NULL),
(6, 'Send Money', -250.00, 'keren loayon (09784136264)', NULL, '2025-05-23 05:06:59', NULL, NULL),
(7, 'Received Money', 250.00, '09638222990', NULL, '2025-05-23 05:06:59', NULL, NULL),
(8, 'Send Money', -100.00, NULL, NULL, '2025-05-23 05:26:39', '09638222990', '09784136264'),
(9, 'Received Money', 100.00, NULL, NULL, '2025-05-23 05:26:39', '09784136264', '09638222990'),
(10, 'Send Money', -350.00, NULL, NULL, '2025-05-23 05:27:21', '09784136264', '09784136264'),
(11, 'Received Money', 350.00, NULL, NULL, '2025-05-23 05:27:21', '09784136264', '09784136264'),
(12, 'Buy Load', -50.00, NULL, 'Globe - GOSURF50', '2025-05-23 14:32:58', '09638222990', NULL),
(13, 'Buy Load', -100.00, NULL, 'Globe - GO100', '2025-05-23 15:14:44', '09638222990', NULL),
(14, 'Add Money', 500.00, NULL, 'Cash In', '2025-05-25 05:08:09', '09638222990', NULL),
(15, 'Add Money', 1500.00, NULL, 'Cash In', '2025-05-25 05:08:22', '09638222990', NULL),
(16, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-25 05:09:44', '09638222990', NULL),
(17, 'Add Money', 50000.00, NULL, 'Cash In', '2025-05-25 05:11:48', '09638222990', NULL),
(18, 'Buy Load', -299.00, NULL, 'Smart - GIGA299', '2025-05-25 05:12:06', '09638222990', NULL),
(19, 'Add Money', 100000.00, NULL, 'Cash In', '2025-05-25 05:12:23', '09638222990', NULL),
(20, 'Send Money', -50000.00, NULL, NULL, '2025-05-25 05:12:56', '09638222990', '09784136264'),
(21, 'Received Money', 50000.00, NULL, NULL, '2025-05-25 05:12:56', '09784136264', '09638222990'),
(22, 'Send Money', -50000.00, NULL, NULL, '2025-05-25 05:13:42', '09784136264', '09638222990'),
(23, 'Received Money', 50000.00, NULL, NULL, '2025-05-25 05:13:42', '09638222990', '09784136264'),
(24, 'Send Money', -100000.00, NULL, NULL, '2025-05-25 05:19:27', '09638222990', '09784136264'),
(25, 'Received Money', 100000.00, NULL, NULL, '2025-05-25 05:19:27', '09784136264', '09638222990'),
(26, 'Add Money', 1.00, NULL, 'Cash In', '2025-05-25 12:11:15', '09434234782', NULL),
(27, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-25 12:14:38', '09434234782', NULL),
(28, 'Send Money', -2500.00, NULL, NULL, '2025-05-25 12:15:17', '09434234782', '09638222790'),
(29, 'Received Money', 2500.00, NULL, NULL, '2025-05-25 12:15:17', '09638222790', '09434234782'),
(30, 'Buy Load', -299.00, NULL, 'Smart - GIGA299', '2025-05-25 12:15:44', '09434234782', NULL),
(31, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-25 12:49:11', '09736436427', NULL),
(32, 'Buy Load', -299.00, NULL, 'Smart - GIGA299', '2025-05-25 12:49:35', '09736436427', NULL),
(33, 'Send Money', -3000.00, NULL, NULL, '2025-05-25 12:50:00', '09736436427', '09434234782'),
(34, 'Received Money', 3000.00, NULL, NULL, '2025-05-25 12:50:00', '09434234782', '09736436427'),
(35, 'Add Money', 78.67, NULL, 'Cash In', '2025-05-25 12:54:59', '09736436427', NULL),
(36, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-25 12:56:41', '09638222990', NULL),
(37, 'Buy Load', -90.00, NULL, 'tnt - UNLI 90', '2025-05-25 12:58:59', '09638222990', NULL),
(38, 'Add Money', 5656.00, NULL, 'Cash In', '2025-05-25 13:10:28', '09677564567', NULL),
(39, 'Add Money', 150.00, NULL, 'Cash In', '2025-05-25 13:13:49', '09343463473', NULL),
(40, 'Buy Load', -100.00, NULL, 'Globe - GO100', '2025-05-25 13:14:07', '09343463473', NULL),
(41, 'Add Money', 50.00, NULL, 'Cash In', '2025-05-26 17:28:07', '09638222990', NULL),
(42, 'Add Money', 50.00, NULL, 'Cash In', '2025-05-26 17:28:07', '09638222990', NULL),
(43, 'Buy Load', -50.00, NULL, 'Globe - GOSURF50', '2025-05-26 17:30:00', '09638222990', NULL),
(44, 'Send Money', -60.00, NULL, 'Transfer to user2', '2025-05-26 17:37:38', '09638222990', '09736436427'),
(45, 'Received Money', 60.00, NULL, 'Transfer from cris', '2025-05-26 17:37:38', '09736436427', '09638222990'),
(46, 'Send Money', -500.00, NULL, 'Transfer to user2', '2025-05-26 17:39:33', '09638222990', '09736436427'),
(47, 'Received Money', 500.00, NULL, 'Transfer from cris', '2025-05-26 17:39:33', '09736436427', '09638222990'),
(48, 'Send Money', -400.00, NULL, 'Transfer to user1', '2025-05-26 17:41:02', '09638222990', '09434234782'),
(49, 'Received Money', 400.00, NULL, 'Transfer from cris', '2025-05-26 17:41:02', '09434234782', '09638222990'),
(50, 'Send Money', -2000.00, NULL, 'Transfer to user4', '2025-05-26 17:46:22', '09638222990', '09343463473'),
(51, 'Received Money', 2000.00, NULL, 'Transfer from cris', '2025-05-26 17:46:22', '09343463473', '09638222990'),
(52, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-26 17:46:48', '09638222990', NULL),
(53, 'Send Money', -1000.00, NULL, 'Transfer to user1', '2025-05-26 18:03:48', '09638222990', '09434234782'),
(54, 'Received Money', 1000.00, NULL, 'Transfer from cris', '2025-05-26 18:03:48', '09434234782', '09638222990'),
(55, 'Send Money', -6000.00, NULL, 'Transfer to user1', '2025-05-26 19:52:32', '09638222990', '09434234782'),
(56, 'Received Money', 6000.00, NULL, 'Transfer from cris', '2025-05-26 19:52:32', '09434234782', '09638222990'),
(57, 'Add Money', 500.00, NULL, 'Cash In', '2025-05-26 20:02:34', '09638322990', NULL),
(58, 'Buy Load', -200.00, NULL, 'Globe - GO200', '2025-05-26 20:03:37', '09638322990', NULL),
(59, 'Add Money', 150.00, NULL, 'Cash In', '2025-05-26 20:12:58', '09638222990', NULL),
(60, 'Buy Load', -150.00, NULL, 'Globe - GO150', '2025-05-26 20:13:15', '09638222990', NULL),
(61, 'Add Money', 1200.00, NULL, 'Cash In', '2025-05-26 20:13:45', '09638222990', NULL),
(62, 'Buy Load', -100.00, NULL, 'Globe - GO100', '2025-05-26 20:13:59', '09638222990', NULL),
(63, 'Send Money', -2000.00, NULL, 'Transfer to cris manzano', '2025-05-26 20:16:16', '09343463473', '09638222990'),
(64, 'Received Money', 2000.00, NULL, 'Transfer from user4', '2025-05-26 20:16:16', '09638222990', '09343463473'),
(65, 'Send Money', -10000.00, NULL, 'Transfer to cris manzano', '2025-05-26 20:22:30', '09434234782', '09638222990'),
(66, 'Received Money', 10000.00, NULL, 'Transfer from user1', '2025-05-26 20:22:30', '09638222990', '09434234782'),
(67, 'Received Money', 10000.00, NULL, 'Transfer from cris', '2025-05-26 20:26:26', '09434234782', '09638222990'),
(68, 'Received Money', 10000.00, NULL, 'Transfer from cris', '2025-05-26 20:26:26', '09434234782', '09638222990'),
(69, 'Send Money', -100.00, NULL, 'Transfer to user1', '2025-05-26 20:27:15', '09638222990', '09434234782'),
(70, 'Received Money', 100.00, NULL, 'Transfer from cris', '2025-05-26 20:27:15', '09434234782', '09638222990'),
(71, 'Send Money', -1000.00, NULL, 'Transfer to user1', '2025-05-26 20:30:55', '09638222990', '09434234782'),
(72, 'Received Money', 1000.00, NULL, 'Transfer from cris', '2025-05-26 20:30:55', '09638222990', '09434234782'),
(73, 'Received Money', 1000.00, NULL, 'Transfer from cris', '2025-05-26 20:30:55', '09434234782', '09638222990'),
(74, 'Send Money', -10000.00, NULL, 'Transfer to user 1', '2025-05-26 20:32:13', '09434234782', '09638322990'),
(75, 'Received Money', 10000.00, NULL, 'Transfer from user1', '2025-05-26 20:32:13', '09434234782', '09638322990'),
(76, 'Received Money', 10000.00, NULL, 'Transfer from user1', '2025-05-26 20:32:13', '09638322990', '09434234782'),
(77, 'Buy Load', -149.00, NULL, 'Smart - GIGA149', '2025-05-26 20:32:46', '09434234782', NULL),
(78, 'Buy Load', -299.00, NULL, 'GOMO - GO299', '2025-05-26 20:58:21', '09638222990', NULL),
(79, 'Buy Load', -99.00, NULL, 'DITO - DATA99', '2025-05-27 12:07:44', '09638222990', NULL),
(80, 'Send Money', -500.00, NULL, 'Transfer to user1', '2025-05-27 12:08:15', '09638222990', '09434234782'),
(81, 'Received Money', 500.00, NULL, 'Transfer from cris', '2025-05-27 12:08:15', '09638222990', '09434234782'),
(82, 'Received Money', 500.00, NULL, 'Transfer from cris', '2025-05-27 12:08:15', '09434234782', '09638222990'),
(83, 'Send Money', -150.00, NULL, 'Transfer to user1', '2025-05-27 12:12:44', '09638222990', '09434234782'),
(84, 'Received Money', 150.00, NULL, 'Transfer from cris', '2025-05-27 12:12:44', '09434234782', '09638222990'),
(85, 'Send Money', -100.00, NULL, 'Transfer to user1', '2025-05-27 12:15:28', '09638222990', '09434234782'),
(86, 'Send Money', -400.00, NULL, 'Transfer to user4', '2025-05-27 12:15:45', '09638222990', '09343463473'),
(87, 'Send Money', -200.00, NULL, 'Transfer to user1', '2025-05-27 12:20:45', '09638222990', '09434234782'),
(88, 'Send Money', -1500.00, NULL, 'Transfer to cris manzano', '2025-05-27 12:21:24', '09434234782', '09638222990'),
(89, 'Subscription', -99.00, NULL, 'Subscription to Mobile Legends Weekly Diamond', '2025-05-27 12:33:24', '09638222990', 'Mobile Legends Weekl'),
(90, 'Subscription', -159.00, NULL, 'Subscription to Disney+ Mobile', '2025-05-27 12:55:42', '09638222990', 'Disney+ Mobile'),
(91, 'Subscription', -369.00, NULL, 'Subscription to Disney+ Premium', '2025-05-27 13:03:35', '09638222990', 'Disney+ Premium'),
(92, 'Subscription', -199.00, NULL, 'Subscription to Netflix Basic', '2025-05-27 13:28:07', '09638222990', 'Netflix Basic'),
(93, 'Subscription', -199.00, NULL, 'Subscription to Netflix Basic', '2025-05-27 13:49:20', '09638222990', 'Netflix Basic'),
(94, 'Subscription', -159.00, NULL, 'Subscription to YouTube Premium Individual', '2025-05-27 13:49:34', '09638222990', 'YouTube Premium Indi'),
(95, 'Subscription', -199.00, NULL, 'Subscription to Netflix Basic', '2025-05-27 13:52:09', '09638222990', 'Netflix Basic'),
(96, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-27 13:52:19', '09638222990', NULL),
(97, 'Subscription', -99.00, NULL, 'Subscription to PUBG Mobile Weekly UC', '2025-05-27 13:52:34', '09638222990', 'PUBG Mobile Weekly U'),
(98, 'Subscription', -399.00, NULL, 'Subscription to Netflix Standard', '2025-05-27 14:00:40', '09638222990', 'Netflix Standard'),
(99, 'Subscription', -199.00, NULL, 'Subscription to Netflix Basic', '2025-05-27 14:00:43', '09638222990', 'Netflix Basic'),
(100, 'Subscription', -159.00, NULL, 'Subscription to YouTube Premium Individual', '2025-05-27 14:00:52', '09638222990', 'YouTube Premium Indi'),
(101, 'Subscription', -199.00, NULL, 'Subscription to Netflix Basic', '2025-05-27 14:04:03', '09638222990', 'Netflix Basic'),
(102, 'Subscription', -199.00, NULL, 'Subscription to Netflix Basic', '2025-05-27 14:08:43', '09638222990', 'Netflix Basic'),
(103, 'Subscription', -239.00, NULL, 'Subscription to YouTube Premium Family', '2025-05-27 14:08:57', '09638222990', 'YouTube Premium Fami'),
(104, 'Netflix Subscription', -199.00, NULL, 'Netflix Basic Plan - sefsef', '2025-05-27 14:32:58', '09638222990', NULL),
(105, 'Netflix Subscription', -199.00, NULL, 'Netflix Basic Plan - asdasd', '2025-05-27 14:41:18', '09638222990', NULL),
(106, 'PUBG Mobile Subscription', -99.00, NULL, 'PUBG Mobile Weekly UC Plan - adasd (asdasdd)', '2025-05-27 14:41:35', '09638222990', NULL),
(107, 'Send Money', -5000.00, NULL, 'Transfer to cris manzano', '2025-05-27 14:46:02', '09677564567', '09638222990'),
(108, 'Mobile Legends Subscription', -299.00, NULL, 'Mobile Legends Monthly Diamond Plan - adasd (asdad)', '2025-05-27 14:48:17', '09638222990', NULL),
(109, 'Add Money', 5000.00, NULL, 'Cash In', '2025-05-27 14:51:09', '09343478564', NULL),
(110, 'Send Money', -2500.00, NULL, 'Transfer to cris manzano', '2025-05-27 14:51:41', '09343478564', '09638222990'),
(111, 'Buy Load', -199.00, NULL, 'DITO - DATA199', '2025-05-27 14:52:04', '09343478564', NULL),
(112, 'Mobile Legends Subscription', -299.00, NULL, 'Mobile Legends Monthly Diamond Plan - cris (2443352)', '2025-05-27 14:52:25', '09343478564', NULL),
(113, 'Valorant Subscription', -499.00, NULL, 'Valorant Premium Points Plan - wrer (343434)', '2025-05-27 15:03:06', '09638222990', NULL),
(114, 'Netflix Subscription', -199.00, NULL, 'Netflix Basic Plan - asdasd', '2025-05-27 15:05:53', '09638222990', NULL),
(115, 'Add Money', 1000.00, NULL, 'Cash In', '2025-05-28 05:48:11', '09638222990', NULL),
(116, 'Buy Load', -50.00, NULL, 'Globe - GOSURF50', '2025-05-28 05:48:32', '09638222990', NULL),
(117, 'Netflix Subscription', -399.00, NULL, 'Netflix Standard Plan - cris aasd', '2025-05-28 05:49:03', '09638222990', NULL),
(118, 'Add Money', 10.00, NULL, 'Cash In', '2025-05-28 05:49:58', '09512465986', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `sex` enum('Male','Female','Prefer not to say') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `balance` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `phone`, `password`, `first_name`, `middle_name`, `last_name`, `sex`, `created_at`, `balance`) VALUES
(72, '09638222990', '111b1aa631daa820ee51ca710a672abaf4ab7c067f755f3eecae342e9b2c5c64', 'cris', 'estal', 'manzano', 'Male', '2025-05-15 05:33:08', 10433.00),
(79, '09434234782', '0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90', 'user1', '', ' ', 'Male', '2025-05-25 12:09:06', 3003.00),
(80, '09736436427', '6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3', 'user2', '', ' ', 'Prefer not to say', '2025-05-25 12:48:55', 2339.67),
(81, '09677564567', '5860faf02b6bc6222ba5aca523560f0e364ccd8b67bee486fe8bf7c01d492ccb', 'user3', '', ' ', 'Prefer not to say', '2025-05-25 13:09:32', 656.00),
(82, '09343463473', '5269ef980de47819ba3d14340f4665262c41e933dc92c1a27dd5d01b047ac80e', 'user4', '', ' ', 'Male', '2025-05-25 13:13:26', 450.00),
(83, '09638322990', '5a39bead318f306939acb1d016647be2e38c6501c58367fdb3e9f52542aa2442', 'user', '', '1', 'Male', '2025-05-26 18:53:00', 10300.00),
(84, '09343478564', 'ecb48a1cc94f951252ec462fe9ecc55c3ef123fadfe935661396c26a45a5809d', 'user6', '', ' ', 'Male', '2025-05-27 14:50:25', 2002.00),
(85, '09512465986', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 'Keren', 'Sarmiento', 'Loayon', 'Female', '2025-05-28 05:41:24', 10.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
