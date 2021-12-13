-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: admin_db
-- Generation Time: Dec 11, 2021 at 01:43 PM
-- Server version: 8.0.27
-- PHP Version: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_adminnotification`
--

CREATE TABLE `accountapp_adminnotification` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `message` longtext NOT NULL,
  `isRead` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `readBy_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_category`
--

CREATE TABLE `accountapp_category` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `publish` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_city`
--

CREATE TABLE `accountapp_city` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `publish` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `state_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_contactus`
--

CREATE TABLE `accountapp_contactus` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `message` longtext,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_language`
--

CREATE TABLE `accountapp_language` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `name` varchar(55) NOT NULL,
  `code` varchar(5) NOT NULL,
  `publish` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_newsletter`
--

CREATE TABLE `accountapp_newsletter` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_notification`
--

CREATE TABLE `accountapp_notification` (
  `id` bigint NOT NULL,
  `message` longtext NOT NULL,
  `isRead` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_plan`
--

CREATE TABLE `accountapp_plan` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `productid` varchar(55) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `period` varchar(55) NOT NULL,
  `amount` int NOT NULL,
  `info` longtext,
  `unlimited` tinyint(1) NOT NULL,
  `noofjob` int DEFAULT NULL,
  `noofrequest` int DEFAULT NULL,
  `publish` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_schedule`
--

CREATE TABLE `accountapp_schedule` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `sun` tinyint(1) NOT NULL,
  `sun_start_hr` int DEFAULT NULL,
  `sun_start_ap` varchar(10) DEFAULT NULL,
  `sun_end_hr` int DEFAULT NULL,
  `sun_end_ap` varchar(10) DEFAULT NULL,
  `mon` tinyint(1) NOT NULL,
  `mon_start_hr` int DEFAULT NULL,
  `mon_start_ap` varchar(10) DEFAULT NULL,
  `mon_end_hr` int DEFAULT NULL,
  `mon_end_ap` varchar(10) DEFAULT NULL,
  `tue` tinyint(1) NOT NULL,
  `tue_start_hr` int DEFAULT NULL,
  `tue_start_ap` varchar(10) DEFAULT NULL,
  `tue_end_hr` int DEFAULT NULL,
  `tue_end_ap` varchar(10) DEFAULT NULL,
  `wed` tinyint(1) NOT NULL,
  `wed_start_hr` int DEFAULT NULL,
  `wed_start_ap` varchar(10) DEFAULT NULL,
  `wed_end_hr` int DEFAULT NULL,
  `wed_end_ap` varchar(10) DEFAULT NULL,
  `thu` tinyint(1) NOT NULL,
  `thu_start_hr` int DEFAULT NULL,
  `thu_start_ap` varchar(10) DEFAULT NULL,
  `thu_end_hr` int DEFAULT NULL,
  `thu_end_ap` varchar(10) DEFAULT NULL,
  `fri` tinyint(1) NOT NULL,
  `fri_start_hr` int DEFAULT NULL,
  `fri_start_ap` varchar(10) DEFAULT NULL,
  `fri_end_hr` int DEFAULT NULL,
  `fri_end_ap` varchar(10) DEFAULT NULL,
  `sat` tinyint(1) NOT NULL,
  `sat_start_hr` int DEFAULT NULL,
  `sat_start_ap` varchar(10) DEFAULT NULL,
  `sat_end_hr` int DEFAULT NULL,
  `sat_end_ap` varchar(10) DEFAULT NULL,
  `part_time` tinyint(1) NOT NULL,
  `full_time` tinyint(1) NOT NULL,
  `status` varchar(10) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `updatedAt` datetime(6) NOT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_state`
--

CREATE TABLE `accountapp_state` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(255) DEFAULT NULL,
  `publish` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_subcategory`
--

CREATE TABLE `accountapp_subcategory` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `publish` tinyint(1) NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `category_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_subscription`
--

CREATE TABLE `accountapp_subscription` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `period` varchar(55) DEFAULT NULL,
  `stripeid` varchar(255) DEFAULT NULL,
  `stripe_subscription_id` varchar(255) DEFAULT NULL,
  `cancel_at_period_end` tinyint(1) NOT NULL,
  `membership` tinyint(1) NOT NULL,
  `unlimited` tinyint(1) NOT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `noofjob` int DEFAULT NULL,
  `noofrequest` int DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `expired` tinyint(1) NOT NULL,
  `recurring` tinyint(1) NOT NULL,
  `status` varchar(10) NOT NULL,
  `payment_amount` int DEFAULT NULL,
  `payment_type` varchar(55) NOT NULL,
  `payment_status` varchar(55) NOT NULL,
  `payment_response` json DEFAULT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `canceldate` datetime(6) DEFAULT NULL,
  `cancel_response` json DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `plan_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_temporarypassword`
--

CREATE TABLE `accountapp_temporarypassword` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `password` varchar(6) NOT NULL,
  `isUsed` tinyint(1) NOT NULL,
  `isExpired` tinyint(1) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_user`
--

CREATE TABLE `accountapp_user` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `token` char(32) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `zipcode` varchar(255) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `yourself` longtext,
  `bg_check` varchar(10) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `video` varchar(100) DEFAULT NULL,
  `available` tinyint(1) NOT NULL,
  `company` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `IsProComplete` tinyint(1) NOT NULL,
  `IsProCompleteStatus` varchar(15) NOT NULL,
  `IsVerified` tinyint(1) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `updatedAt` datetime(6) DEFAULT NULL,
  `device_id` longtext,
  `devicetoken` longtext,
  `city_id` bigint DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `state_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `accountapp_user`
--

INSERT INTO `accountapp_user` (`id`, `password`, `last_login`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `token`, `email`, `mobile`, `address`, `zipcode`, `latitude`, `longitude`, `yourself`, `bg_check`, `image`, `video`, `available`, `company`, `title`, `IsProComplete`, `IsProCompleteStatus`, `IsVerified`, `ipaddress`, `source`, `browserinfo`, `updatedAt`, `device_id`, `devicetoken`, `city_id`, `createdBy_id`, `state_id`) VALUES
(1, '', NULL, 0, 'Ahmed kabeer', 'kabeer', 0, 1, '2021-12-08 16:41:45.816786', '31ad1efb7cf444ddb5cd5db0c8b6083f', 'maliksblr92@gmail.com', '03441500542', NULL, NULL, NULL, NULL, NULL, NULL, 'users/images/Screenshot_from_2021-12-03_21-37-23.png', '', 0, 'codistan', '', 0, 'Register', 0, NULL, 'Web', NULL, '2021-12-08 16:41:46.274700', NULL, NULL, NULL, NULL, NULL),
(2, '', NULL, 0, 'Alan', 'kabeer', 0, 1, '2021-12-08 16:41:45.816786', '31ad1efb7cf444ddb5cd5db0c8b6084f', 'maliksblr93@gmail.com', '03441500543', NULL, NULL, NULL, NULL, NULL, NULL, 'users/images/Screenshot_from_2021-12-03_21-37-23.png', '', 0, 'codistan', '', 0, 'Register', 0, NULL, 'Web', NULL, '2021-12-08 16:41:46.274700', NULL, NULL, NULL, NULL, NULL),
(3, '', NULL, 0, 'Bob', 'kabeer', 0, 1, '2021-12-08 16:41:45.816787', '31ad1efb7cf444ddb5cd5db0c8b6085f', 'maliksblr94@gmail.com', '03441500544', NULL, NULL, NULL, NULL, NULL, NULL, 'users/images/Screenshot_from_2021-12-03_21-37-23.png', '', 0, 'codistan', '', 0, 'Register', 0, NULL, 'Web', NULL, '2021-12-08 16:41:46.274700', NULL, NULL, NULL, NULL, NULL),
(4, '', NULL, 0, 'Alan', 'kabeer', 0, 1, '2021-12-08 16:41:45.816788', '31ad1efb7cf444ddb5cd5db0c8b6086f', 'maliksblr95@gmail.com', '03441500545', NULL, NULL, NULL, NULL, NULL, NULL, 'users/images/Screenshot_from_2021-12-03_21-37-23.png', '', 0, 'codistan', '', 0, 'Register', 0, NULL, 'Web', NULL, '2021-12-08 16:41:46.274700', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_usercategory`
--

CREATE TABLE `accountapp_usercategory` (
  `id` bigint NOT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `category_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_usercategory_subcategory`
--

CREATE TABLE `accountapp_usercategory_subcategory` (
  `id` bigint NOT NULL,
  `usercategory_id` bigint NOT NULL,
  `subcategory_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_userprofileview`
--

CREATE TABLE `accountapp_userprofileview` (
  `id` bigint NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `viewby_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_user_groups`
--

CREATE TABLE `accountapp_user_groups` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_user_language`
--

CREATE TABLE `accountapp_user_language` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `language_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accountapp_user_user_permissions`
--

CREATE TABLE `accountapp_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `apiapp_apiauthkey`
--

CREATE TABLE `apiapp_apiauthkey` (
  `key` char(32) NOT NULL,
  `isRevoked` tinyint(1) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Logging', 6, 'add_statuslog'),
(22, 'Can change Logging', 6, 'change_statuslog'),
(23, 'Can delete Logging', 6, 'delete_statuslog'),
(24, 'Can view Logging', 6, 'view_statuslog'),
(25, 'Can add pageview', 7, 'add_pageview'),
(26, 'Can change pageview', 7, 'change_pageview'),
(27, 'Can delete pageview', 7, 'delete_pageview'),
(28, 'Can view pageview', 7, 'view_pageview'),
(29, 'Can add visitor', 8, 'add_visitor'),
(30, 'Can change visitor', 8, 'change_visitor'),
(31, 'Can delete visitor', 8, 'delete_visitor'),
(32, 'Can view visitor', 8, 'view_visitor'),
(33, 'Can view visitor', 8, 'visitor_log'),
(34, 'Can add Token', 9, 'add_token'),
(35, 'Can change Token', 9, 'change_token'),
(36, 'Can delete Token', 9, 'delete_token'),
(37, 'Can view Token', 9, 'view_token'),
(38, 'Can add token', 10, 'add_tokenproxy'),
(39, 'Can change token', 10, 'change_tokenproxy'),
(40, 'Can delete token', 10, 'delete_tokenproxy'),
(41, 'Can view token', 10, 'view_tokenproxy'),
(42, 'Can add FCM device', 11, 'add_fcmdevice'),
(43, 'Can change FCM device', 11, 'change_fcmdevice'),
(44, 'Can delete FCM device', 11, 'delete_fcmdevice'),
(45, 'Can view FCM device', 11, 'view_fcmdevice'),
(46, 'Can add crontab', 12, 'add_crontabschedule'),
(47, 'Can change crontab', 12, 'change_crontabschedule'),
(48, 'Can delete crontab', 12, 'delete_crontabschedule'),
(49, 'Can view crontab', 12, 'view_crontabschedule'),
(50, 'Can add interval', 13, 'add_intervalschedule'),
(51, 'Can change interval', 13, 'change_intervalschedule'),
(52, 'Can delete interval', 13, 'delete_intervalschedule'),
(53, 'Can view interval', 13, 'view_intervalschedule'),
(54, 'Can add periodic task', 14, 'add_periodictask'),
(55, 'Can change periodic task', 14, 'change_periodictask'),
(56, 'Can delete periodic task', 14, 'delete_periodictask'),
(57, 'Can view periodic task', 14, 'view_periodictask'),
(58, 'Can add periodic tasks', 15, 'add_periodictasks'),
(59, 'Can change periodic tasks', 15, 'change_periodictasks'),
(60, 'Can delete periodic tasks', 15, 'delete_periodictasks'),
(61, 'Can view periodic tasks', 15, 'view_periodictasks'),
(62, 'Can add solar event', 16, 'add_solarschedule'),
(63, 'Can change solar event', 16, 'change_solarschedule'),
(64, 'Can delete solar event', 16, 'delete_solarschedule'),
(65, 'Can view solar event', 16, 'view_solarschedule'),
(66, 'Can add clocked', 17, 'add_clockedschedule'),
(67, 'Can change clocked', 17, 'change_clockedschedule'),
(68, 'Can delete clocked', 17, 'delete_clockedschedule'),
(69, 'Can view clocked', 17, 'view_clockedschedule'),
(70, 'Can add user', 18, 'add_user'),
(71, 'Can change user', 18, 'change_user'),
(72, 'Can delete user', 18, 'delete_user'),
(73, 'Can view user', 18, 'view_user'),
(74, 'Can add Category', 19, 'add_category'),
(75, 'Can change Category', 19, 'change_category'),
(76, 'Can delete Category', 19, 'delete_category'),
(77, 'Can view Category', 19, 'view_category'),
(78, 'Can add Language', 20, 'add_language'),
(79, 'Can change Language', 20, 'change_language'),
(80, 'Can delete Language', 20, 'delete_language'),
(81, 'Can view Language', 20, 'view_language'),
(82, 'Can add Plan', 21, 'add_plan'),
(83, 'Can change Plan', 21, 'change_plan'),
(84, 'Can delete Plan', 21, 'delete_plan'),
(85, 'Can view Plan', 21, 'view_plan'),
(86, 'Can add State', 22, 'add_state'),
(87, 'Can change State', 22, 'change_state'),
(88, 'Can delete State', 22, 'delete_state'),
(89, 'Can view State', 22, 'view_state'),
(90, 'Can add Sub Category', 23, 'add_subcategory'),
(91, 'Can change Sub Category', 23, 'change_subcategory'),
(92, 'Can delete Sub Category', 23, 'delete_subcategory'),
(93, 'Can view Sub Category', 23, 'view_subcategory'),
(94, 'Can add User Profile View', 24, 'add_userprofileview'),
(95, 'Can change User Profile View', 24, 'change_userprofileview'),
(96, 'Can delete User Profile View', 24, 'delete_userprofileview'),
(97, 'Can view User Profile View', 24, 'view_userprofileview'),
(98, 'Can add User Category', 25, 'add_usercategory'),
(99, 'Can change User Category', 25, 'change_usercategory'),
(100, 'Can delete User Category', 25, 'delete_usercategory'),
(101, 'Can view User Category', 25, 'view_usercategory'),
(102, 'Can add Temporary Password', 26, 'add_temporarypassword'),
(103, 'Can change Temporary Password', 26, 'change_temporarypassword'),
(104, 'Can delete Temporary Password', 26, 'delete_temporarypassword'),
(105, 'Can view Temporary Password', 26, 'view_temporarypassword'),
(106, 'Can add Subscription', 27, 'add_subscription'),
(107, 'Can change Subscription', 27, 'change_subscription'),
(108, 'Can delete Subscription', 27, 'delete_subscription'),
(109, 'Can view Subscription', 27, 'view_subscription'),
(110, 'Can add Schedule', 28, 'add_schedule'),
(111, 'Can change Schedule', 28, 'change_schedule'),
(112, 'Can delete Schedule', 28, 'delete_schedule'),
(113, 'Can view Schedule', 28, 'view_schedule'),
(114, 'Can add Notification', 29, 'add_notification'),
(115, 'Can change Notification', 29, 'change_notification'),
(116, 'Can delete Notification', 29, 'delete_notification'),
(117, 'Can view Notification', 29, 'view_notification'),
(118, 'Can add Newsletter', 30, 'add_newsletter'),
(119, 'Can change Newsletter', 30, 'change_newsletter'),
(120, 'Can delete Newsletter', 30, 'delete_newsletter'),
(121, 'Can view Newsletter', 30, 'view_newsletter'),
(122, 'Can add Contact Us', 31, 'add_contactus'),
(123, 'Can change Contact Us', 31, 'change_contactus'),
(124, 'Can delete Contact Us', 31, 'delete_contactus'),
(125, 'Can view Contact Us', 31, 'view_contactus'),
(126, 'Can add City', 32, 'add_city'),
(127, 'Can change City', 32, 'change_city'),
(128, 'Can delete City', 32, 'delete_city'),
(129, 'Can view City', 32, 'view_city'),
(130, 'Can add Admin Notification', 33, 'add_adminnotification'),
(131, 'Can change Admin Notification', 33, 'change_adminnotification'),
(132, 'Can delete Admin Notification', 33, 'delete_adminnotification'),
(133, 'Can view Admin Notification', 33, 'view_adminnotification'),
(134, 'Can add Job', 34, 'add_job'),
(135, 'Can change Job', 34, 'change_job'),
(136, 'Can delete Job', 34, 'delete_job'),
(137, 'Can view Job', 34, 'view_job'),
(138, 'Can add Job Offer', 35, 'add_joboffer'),
(139, 'Can change Job Offer', 35, 'change_joboffer'),
(140, 'Can delete Job Offer', 35, 'delete_joboffer'),
(141, 'Can view Job Offer', 35, 'view_joboffer'),
(142, 'Can add Job Shift Schedule', 36, 'add_jobshiftschedule'),
(143, 'Can change Job Shift Schedule', 36, 'change_jobshiftschedule'),
(144, 'Can delete Job Shift Schedule', 36, 'delete_jobshiftschedule'),
(145, 'Can view Job Shift Schedule', 36, 'view_jobshiftschedule'),
(146, 'Can add Job Action', 37, 'add_jobofferaction'),
(147, 'Can change Job Action', 37, 'change_jobofferaction'),
(148, 'Can delete Job Action', 37, 'delete_jobofferaction'),
(149, 'Can view Job Action', 37, 'view_jobofferaction'),
(150, 'Can add API Auth Key', 38, 'add_apiauthkey'),
(151, 'Can change API Auth Key', 38, 'change_apiauthkey'),
(152, 'Can delete API Auth Key', 38, 'delete_apiauthkey'),
(153, 'Can view API Auth Key', 38, 'view_apiauthkey'),
(154, 'Can add Blog', 39, 'add_blog'),
(155, 'Can change Blog', 39, 'change_blog'),
(156, 'Can delete Blog', 39, 'delete_blog'),
(157, 'Can view Blog', 39, 'view_blog'),
(158, 'Can add Category', 40, 'add_blogcategory'),
(159, 'Can change Category', 40, 'change_blogcategory'),
(160, 'Can delete Category', 40, 'delete_blogcategory'),
(161, 'Can view Category', 40, 'view_blogcategory'),
(162, 'Can add View', 41, 'add_blogview'),
(163, 'Can change View', 41, 'change_blogview'),
(164, 'Can delete View', 41, 'delete_blogview'),
(165, 'Can view View', 41, 'view_blogview'),
(166, 'Can add Comment', 42, 'add_blogcomment'),
(167, 'Can change Comment', 42, 'change_blogcomment'),
(168, 'Can delete Comment', 42, 'delete_blogcomment'),
(169, 'Can view Comment', 42, 'view_blogcomment');

-- --------------------------------------------------------

--
-- Table structure for table `blogapp_blog`
--

CREATE TABLE `blogapp_blog` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `publish` tinyint(1) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) DEFAULT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `createdBy_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blogapp_blogcategory`
--

CREATE TABLE `blogapp_blogcategory` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `publish` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blogapp_blogcomment`
--

CREATE TABLE `blogapp_blogcomment` (
  `id` bigint NOT NULL,
  `comment` longtext NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `blog_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blogapp_blogview`
--

CREATE TABLE `blogapp_blogview` (
  `id` bigint NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) DEFAULT NULL,
  `blog_id` bigint NOT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_clockedschedule`
--

CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int NOT NULL,
  `clocked_time` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int NOT NULL,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int NOT NULL,
  `every` int NOT NULL,
  `period` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_periodictask`
--

CREATE TABLE `django_celery_beat_periodictask` (
  `id` int NOT NULL,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int UNSIGNED NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int DEFAULT NULL,
  `interval_id` int DEFAULT NULL,
  `solar_id` int DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int UNSIGNED DEFAULT NULL,
  `headers` longtext NOT NULL DEFAULT (_utf8mb3'{}'),
  `clocked_id` int DEFAULT NULL,
  `expire_seconds` int UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_periodictasks`
--

CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint NOT NULL,
  `last_update` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_solarschedule`
--

CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int NOT NULL,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(33, 'accountapp', 'adminnotification'),
(19, 'accountapp', 'category'),
(32, 'accountapp', 'city'),
(31, 'accountapp', 'contactus'),
(20, 'accountapp', 'language'),
(30, 'accountapp', 'newsletter'),
(29, 'accountapp', 'notification'),
(21, 'accountapp', 'plan'),
(28, 'accountapp', 'schedule'),
(22, 'accountapp', 'state'),
(23, 'accountapp', 'subcategory'),
(27, 'accountapp', 'subscription'),
(26, 'accountapp', 'temporarypassword'),
(18, 'accountapp', 'user'),
(25, 'accountapp', 'usercategory'),
(24, 'accountapp', 'userprofileview'),
(1, 'admin', 'logentry'),
(38, 'apiapp', 'apiauthkey'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(9, 'authtoken', 'token'),
(10, 'authtoken', 'tokenproxy'),
(39, 'blogapp', 'blog'),
(40, 'blogapp', 'blogcategory'),
(42, 'blogapp', 'blogcomment'),
(41, 'blogapp', 'blogview'),
(4, 'contenttypes', 'contenttype'),
(17, 'django_celery_beat', 'clockedschedule'),
(12, 'django_celery_beat', 'crontabschedule'),
(13, 'django_celery_beat', 'intervalschedule'),
(14, 'django_celery_beat', 'periodictask'),
(15, 'django_celery_beat', 'periodictasks'),
(16, 'django_celery_beat', 'solarschedule'),
(6, 'django_db_logger', 'statuslog'),
(11, 'fcm_django', 'fcmdevice'),
(34, 'jobapp', 'job'),
(35, 'jobapp', 'joboffer'),
(37, 'jobapp', 'jobofferaction'),
(36, 'jobapp', 'jobshiftschedule'),
(5, 'sessions', 'session'),
(7, 'tracking', 'pageview'),
(8, 'tracking', 'visitor');

-- --------------------------------------------------------

--
-- Table structure for table `django_db_logger_statuslog`
--

CREATE TABLE `django_db_logger_statuslog` (
  `id` bigint NOT NULL,
  `logger_name` varchar(100) NOT NULL,
  `level` smallint UNSIGNED NOT NULL,
  `msg` longtext NOT NULL,
  `trace` longtext,
  `create_datetime` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_db_logger_statuslog`
--

INSERT INTO `django_db_logger_statuslog` (`id`, `logger_name`, `level`, `msg`, `trace`, `create_datetime`) VALUES
(1, 'accountapp', 40, 'Group matching query does not exist.', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 136, in sign_up\n    group = Group.objects.get(name=\'Employer\')\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/manager.py\", line 85, in manager_method\n    return getattr(self.get_queryset(), name)(*args, **kwargs)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 435, in get\n    raise self.model.DoesNotExist(\ndjango.contrib.auth.models.Group.DoesNotExist: Group matching query does not exist.', '2021-12-08 16:41:46.463931'),
(2, 'django.request', 40, 'Internal Server Error: /sign-up', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/base.py\", line 181, in _get_response\n    response = wrapped_callback(request, *callback_args, **callback_kwargs)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/views/decorators/cache.py\", line 32, in _cache_controlled\n    patch_cache_control(response, **kwargs)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/cache.py\", line 63, in patch_cache_control\n    if response.get(\'Cache-Control\'):\nAttributeError: \'DoesNotExist\' object has no attribute \'get\'', '2021-12-08 16:41:46.501846'),
(3, 'django.request', 30, 'Not Found: /favicon.ico', NULL, '2021-12-08 16:41:46.849963'),
(4, 'django.request', 30, 'Not Found: /fin-job-seekers', NULL, '2021-12-08 16:42:36.271025'),
(5, 'accountapp', 40, 'type object \'User\' has no attribute \'all\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 388, in find_job_seekers\n    records=User.all()\nAttributeError: type object \'User\' has no attribute \'all\'', '2021-12-08 16:58:35.127461'),
(6, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'AttributeError\' object has no attribute \'status_code\'', '2021-12-08 16:58:35.185618'),
(7, 'accountapp', 40, 'type object \'User\' has no attribute \'all\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 388, in find_job_seekers\n    records=User.all()\nAttributeError: type object \'User\' has no attribute \'all\'', '2021-12-08 16:59:11.147232'),
(8, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'AttributeError\' object has no attribute \'status_code\'', '2021-12-08 16:59:11.199116'),
(9, 'accountapp', 40, 'invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 392, in find_job_seekers\n    return render(request, template_name, data)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/shortcuts.py\", line 19, in render\n    content = loader.render_to_string(template_name, context, request, using=using)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader.py\", line 62, in render_to_string\n    return template.render(context, request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/backends/django.py\", line 61, in render\n    return self.template.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 170, in render\n    return self._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 150, in render\n    return compiled_parent._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 62, in render\n    result = block.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/defaulttags.py\", line 311, in render\n    if match:\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 284, in __bool__\n    self._fetch_all()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 1324, in _fetch_all\n    self._result_cache = list(self._iterable_class(self))\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 68, in __iter__\n    for row in compiler.results_iter(results):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py\", line 1122, in apply_converters\n    value = converter(value, expression, connection)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py\", line 318, in convert_uuidfield_value\n    value = uuid.UUID(value)\n  File \"/usr/lib/python3.8/uuid.py\", line 172, in __init__\n    int = int_(hex, 16)\nValueError: invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', '2021-12-08 17:00:22.917624'),
(10, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'ValueError\' object has no attribute \'status_code\'', '2021-12-08 17:00:22.957824'),
(11, 'accountapp', 40, 'invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 392, in find_job_seekers\n    return render(request, template_name, data)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/shortcuts.py\", line 19, in render\n    content = loader.render_to_string(template_name, context, request, using=using)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader.py\", line 62, in render_to_string\n    return template.render(context, request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/backends/django.py\", line 61, in render\n    return self.template.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 170, in render\n    return self._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 150, in render\n    return compiled_parent._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 62, in render\n    result = block.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/defaulttags.py\", line 311, in render\n    if match:\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 284, in __bool__\n    self._fetch_all()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 1324, in _fetch_all\n    self._result_cache = list(self._iterable_class(self))\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 68, in __iter__\n    for row in compiler.results_iter(results):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py\", line 1122, in apply_converters\n    value = converter(value, expression, connection)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py\", line 318, in convert_uuidfield_value\n    value = uuid.UUID(value)\n  File \"/usr/lib/python3.8/uuid.py\", line 172, in __init__\n    int = int_(hex, 16)\nValueError: invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', '2021-12-08 17:00:24.040891'),
(12, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'ValueError\' object has no attribute \'status_code\'', '2021-12-08 17:00:24.081160'),
(13, 'accountapp', 40, 'invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 392, in find_job_seekers\n    return render(request, template_name, data)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/shortcuts.py\", line 19, in render\n    content = loader.render_to_string(template_name, context, request, using=using)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader.py\", line 62, in render_to_string\n    return template.render(context, request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/backends/django.py\", line 61, in render\n    return self.template.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 170, in render\n    return self._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 150, in render\n    return compiled_parent._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 62, in render\n    result = block.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/defaulttags.py\", line 311, in render\n    if match:\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 284, in __bool__\n    self._fetch_all()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 1324, in _fetch_all\n    self._result_cache = list(self._iterable_class(self))\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 68, in __iter__\n    for row in compiler.results_iter(results):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py\", line 1122, in apply_converters\n    value = converter(value, expression, connection)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py\", line 318, in convert_uuidfield_value\n    value = uuid.UUID(value)\n  File \"/usr/lib/python3.8/uuid.py\", line 172, in __init__\n    int = int_(hex, 16)\nValueError: invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', '2021-12-08 17:01:54.954592'),
(14, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'ValueError\' object has no attribute \'status_code\'', '2021-12-08 17:01:55.018783'),
(15, 'accountapp', 40, 'invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 392, in find_job_seekers\n    return render(request, template_name, data)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/shortcuts.py\", line 19, in render\n    content = loader.render_to_string(template_name, context, request, using=using)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader.py\", line 62, in render_to_string\n    return template.render(context, request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/backends/django.py\", line 61, in render\n    return self.template.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 170, in render\n    return self._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 150, in render\n    return compiled_parent._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 62, in render\n    result = block.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/defaulttags.py\", line 311, in render\n    if match:\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 284, in __bool__\n    self._fetch_all()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 1324, in _fetch_all\n    self._result_cache = list(self._iterable_class(self))\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 68, in __iter__\n    for row in compiler.results_iter(results):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py\", line 1122, in apply_converters\n    value = converter(value, expression, connection)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py\", line 318, in convert_uuidfield_value\n    value = uuid.UUID(value)\n  File \"/usr/lib/python3.8/uuid.py\", line 172, in __init__\n    int = int_(hex, 16)\nValueError: invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', '2021-12-08 17:03:34.791413'),
(16, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'ValueError\' object has no attribute \'status_code\'', '2021-12-08 17:03:34.832735'),
(17, 'accountapp', 40, 'invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 392, in find_job_seekers\n    return render(request, template_name, data)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/shortcuts.py\", line 19, in render\n    content = loader.render_to_string(template_name, context, request, using=using)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader.py\", line 62, in render_to_string\n    return template.render(context, request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/backends/django.py\", line 61, in render\n    return self.template.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 170, in render\n    return self._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 150, in render\n    return compiled_parent._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 62, in render\n    result = block.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/defaulttags.py\", line 311, in render\n    if match:\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 284, in __bool__\n    self._fetch_all()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 1324, in _fetch_all\n    self._result_cache = list(self._iterable_class(self))\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/query.py\", line 68, in __iter__\n    for row in compiler.results_iter(results):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py\", line 1122, in apply_converters\n    value = converter(value, expression, connection)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py\", line 318, in convert_uuidfield_value\n    value = uuid.UUID(value)\n  File \"/usr/lib/python3.8/uuid.py\", line 172, in __init__\n    int = int_(hex, 16)\nValueError: invalid literal for int() with base 16: \'31ad1efb7cf444ddb5cd5db0c8b6083g\'', '2021-12-08 17:04:38.257655'),
(18, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'ValueError\' object has no attribute \'status_code\'', '2021-12-08 17:04:38.305400'),
(19, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 21:14:09.754193'),
(20, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 21:14:10.092814'),
(21, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 21:14:30.264976'),
(22, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 21:14:30.374560'),
(23, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 21:14:30.628544'),
(24, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:12:14.320007'),
(25, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:12:14.443030'),
(26, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:12:14.742162'),
(27, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:11.687144'),
(28, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:11.820349'),
(29, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:12.037947'),
(30, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:12.761233'),
(31, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:12.856023'),
(32, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:15.648836'),
(33, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.158527'),
(34, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.216927'),
(35, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.264403'),
(36, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.304877'),
(37, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.395099'),
(38, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.452184'),
(39, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.505416'),
(40, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.595659'),
(41, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.663814'),
(42, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.698382'),
(43, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.795258'),
(44, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.846717'),
(45, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.906219'),
(46, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:16.995257'),
(47, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.051850'),
(48, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.118767'),
(49, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.203826'),
(50, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.251807'),
(51, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.294427'),
(52, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.394645'),
(53, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.447526'),
(54, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.492286'),
(55, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.649234'),
(56, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.718323'),
(57, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.771694'),
(58, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.825210'),
(59, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.910612'),
(60, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:17.968272'),
(61, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.004946'),
(62, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.097439'),
(63, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.152328'),
(64, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.197995'),
(65, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.277957'),
(66, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.332467'),
(67, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.381399'),
(68, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.460261'),
(69, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.518984'),
(70, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.580609'),
(71, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.677168'),
(72, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.733932'),
(73, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.788449'),
(74, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.876847'),
(75, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.911258'),
(76, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:18.971030'),
(77, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.097301'),
(78, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.128907'),
(79, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.181358'),
(80, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.230050'),
(81, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.309266'),
(82, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.370848'),
(83, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.414815'),
(84, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.522708'),
(85, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.561474'),
(86, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.642708'),
(87, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.701604'),
(88, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.745914'),
(89, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.852087'),
(90, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.895187'),
(91, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:19.949866'),
(92, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.043854'),
(93, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.098374'),
(94, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.140792'),
(95, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.260795'),
(96, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.349485'),
(97, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.408217'),
(98, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.446626'),
(99, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.536599'),
(100, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.579878'),
(101, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.626407'),
(102, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.768667'),
(103, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.866303'),
(104, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.909335'),
(105, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:20.960803'),
(106, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.014406'),
(107, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.107235'),
(108, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.168323'),
(109, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.252404'),
(110, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.318295'),
(111, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.407666'),
(112, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.500158'),
(113, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.543860'),
(114, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.593021'),
(115, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.731297'),
(116, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.790304'),
(117, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.841714'),
(118, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.902795'),
(119, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:21.992852'),
(120, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.047109'),
(121, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.092591'),
(122, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.174883'),
(123, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.238180'),
(124, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.298878'),
(125, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.357514'),
(126, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.453928'),
(127, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.508588'),
(128, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.564035'),
(129, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.647954'),
(130, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.693683'),
(131, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.754228'),
(132, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.877112'),
(133, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.949148'),
(134, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:22.992075'),
(135, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.050344'),
(136, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.140090'),
(137, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.195757'),
(138, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.293449'),
(139, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.330216'),
(140, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.410392'),
(141, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.457986'),
(142, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.506142'),
(143, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.608947'),
(144, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.659637'),
(145, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.715967'),
(146, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.808021'),
(147, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.868711'),
(148, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.908323'),
(149, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:23.995992'),
(150, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.053235'),
(151, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.092288'),
(152, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.173153'),
(153, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.233632'),
(154, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.268029'),
(155, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.357052'),
(156, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.455711'),
(157, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.494009'),
(158, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.542274'),
(159, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.643433'),
(160, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.694824'),
(161, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.749990'),
(162, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.837243'),
(163, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.893632'),
(164, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:24.940425'),
(165, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.065498'),
(166, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.174627'),
(167, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.223094'),
(168, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.271306'),
(169, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.355096'),
(170, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.414622'),
(171, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.453588'),
(172, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.537173'),
(173, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.598807'),
(174, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.641101'),
(175, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.719919'),
(176, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.776231'),
(177, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.819544'),
(178, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:25.904194'),
(179, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:39.265386'),
(180, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:14:39.820202'),
(181, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:15:26.370498'),
(182, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:15:26.702076'),
(183, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:15:42.337850'),
(184, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:15:42.728112'),
(185, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:16:46.491706'),
(186, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:16:46.865050'),
(187, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:17:22.089964'),
(188, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:17:22.421737');
INSERT INTO `django_db_logger_statuslog` (`id`, `logger_name`, `level`, `msg`, `trace`, `create_datetime`) VALUES
(189, 'accountapp', 40, 'Invalid block tag on line 156: \'endif\'. Did you forget to register or load this tag?', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 470, in parse\n    compile_func = self.tags[command]\nKeyError: \'endif\'\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/gotoworkamerica/accountapp/views.py\", line 392, in find_job_seekers\n    return render(request, template_name, data)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/shortcuts.py\", line 19, in render\n    content = loader.render_to_string(template_name, context, request, using=using)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader.py\", line 62, in render_to_string\n    return template.render(context, request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/backends/django.py\", line 61, in render\n    return self.template.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 170, in render\n    return self._render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 162, in _render\n    return self.nodelist.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 938, in render\n    bit = node.render_annotated(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 905, in render_annotated\n    return self.render(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 127, in render\n    compiled_parent = self.get_parent(context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 124, in get_parent\n    return self.find_template(parent, context)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loader_tags.py\", line 103, in find_template\n    template, origin = context.template.engine.find_template(\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/engine.py\", line 125, in find_template\n    template = loader.get_template(name, skip=skip)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/loaders/base.py\", line 29, in get_template\n    return Template(\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 155, in __init__\n    self.nodelist = self.compile_nodelist()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 193, in compile_nodelist\n    return parser.parse()\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 472, in parse\n    self.invalid_block_tag(token, command, parse_until)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/template/base.py\", line 531, in invalid_block_tag\n    raise self.error(\ndjango.template.exceptions.TemplateSyntaxError: Invalid block tag on line 156: \'endif\'. Did you forget to register or load this tag?', '2021-12-10 22:22:23.867271'),
(190, 'django.request', 40, 'Internal Server Error: /find-job-seekers', 'Traceback (most recent call last):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/core/handlers/exception.py\", line 47, in inner\n    response = get_response(request)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/django/utils/deprecation.py\", line 119, in __call__\n    response = self.process_response(request, response)\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 156, in process_response\n    if not self._should_track(user, request, response):\n  File \"/home/asd/Desktop/development/gotoworkamerica/venv/lib/python3.8/site-packages/tracking/middleware.py\", line 57, in _should_track\n    if response.status_code in TRACK_IGNORE_STATUS_CODES:\nAttributeError: \'TemplateSyntaxError\' object has no attribute \'status_code\'', '2021-12-10 22:22:23.913526'),
(191, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:23:12.365389'),
(192, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:23:12.783657'),
(193, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:23:49.528218'),
(194, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:23:49.594709'),
(195, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:23:49.897266'),
(196, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:04.343450'),
(197, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:04.667372'),
(198, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:15.847557'),
(199, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:15.949772'),
(200, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:16.260441'),
(201, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:54.624893'),
(202, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:28:54.996718'),
(203, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:29:25.406900'),
(204, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:29:25.529056'),
(205, 'django.request', 30, 'Not Found: /MY_VIDEO_POSTER.jpg', NULL, '2021-12-10 22:29:25.795590');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2021-12-08 16:40:41.473807'),
(2, 'contenttypes', '0002_remove_content_type_name', '2021-12-08 16:40:41.702471'),
(3, 'auth', '0001_initial', '2021-12-08 16:40:42.772005'),
(4, 'auth', '0002_alter_permission_name_max_length', '2021-12-08 16:40:42.940371'),
(5, 'auth', '0003_alter_user_email_max_length', '2021-12-08 16:40:42.953777'),
(6, 'auth', '0004_alter_user_username_opts', '2021-12-08 16:40:42.969150'),
(7, 'auth', '0005_alter_user_last_login_null', '2021-12-08 16:40:42.991133'),
(8, 'auth', '0006_require_contenttypes_0002', '2021-12-08 16:40:43.001319'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2021-12-08 16:40:43.018739'),
(10, 'auth', '0008_alter_user_username_max_length', '2021-12-08 16:40:43.035811'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2021-12-08 16:40:43.050039'),
(12, 'auth', '0010_alter_group_name_max_length', '2021-12-08 16:40:43.084774'),
(13, 'auth', '0011_update_proxy_permissions', '2021-12-08 16:40:43.100367'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2021-12-08 16:40:43.115048'),
(15, 'accountapp', '0001_initial', '2021-12-08 16:40:51.423150'),
(16, 'admin', '0001_initial', '2021-12-08 16:40:51.900304'),
(17, 'admin', '0002_logentry_remove_auto_add', '2021-12-08 16:40:51.961920'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2021-12-08 16:40:51.997355'),
(19, 'apiapp', '0001_initial', '2021-12-08 16:40:52.261185'),
(20, 'authtoken', '0001_initial', '2021-12-08 16:40:52.611350'),
(21, 'authtoken', '0002_auto_20160226_1747', '2021-12-08 16:40:52.834902'),
(22, 'authtoken', '0003_tokenproxy', '2021-12-08 16:40:52.847472'),
(23, 'blogapp', '0001_initial', '2021-12-08 16:40:54.417528'),
(24, 'django_celery_beat', '0001_initial', '2021-12-08 16:40:55.192045'),
(25, 'django_celery_beat', '0002_auto_20161118_0346', '2021-12-08 16:40:55.473195'),
(26, 'django_celery_beat', '0003_auto_20161209_0049', '2021-12-08 16:40:55.554038'),
(27, 'django_celery_beat', '0004_auto_20170221_0000', '2021-12-08 16:40:55.570006'),
(28, 'django_celery_beat', '0005_add_solarschedule_events_choices', '2021-12-08 16:40:55.583722'),
(29, 'django_celery_beat', '0006_auto_20180322_0932', '2021-12-08 16:40:55.760841'),
(30, 'django_celery_beat', '0007_auto_20180521_0826', '2021-12-08 16:40:55.891957'),
(31, 'django_celery_beat', '0008_auto_20180914_1922', '2021-12-08 16:40:55.929325'),
(32, 'django_celery_beat', '0006_auto_20180210_1226', '2021-12-08 16:40:55.955785'),
(33, 'django_celery_beat', '0006_periodictask_priority', '2021-12-08 16:40:56.180300'),
(34, 'django_celery_beat', '0009_periodictask_headers', '2021-12-08 16:40:56.380841'),
(35, 'django_celery_beat', '0010_auto_20190429_0326', '2021-12-08 16:40:56.623563'),
(36, 'django_celery_beat', '0011_auto_20190508_0153', '2021-12-08 16:40:56.960958'),
(37, 'django_celery_beat', '0012_periodictask_expire_seconds', '2021-12-08 16:40:57.255394'),
(38, 'django_celery_beat', '0013_auto_20200609_0727', '2021-12-08 16:40:57.273921'),
(39, 'django_celery_beat', '0014_remove_clockedschedule_enabled', '2021-12-08 16:40:57.398856'),
(40, 'django_celery_beat', '0015_edit_solarschedule_events_choices', '2021-12-08 16:40:57.417518'),
(41, 'django_db_logger', '0001_initial', '2021-12-08 16:40:57.573364'),
(42, 'django_db_logger', '0002_auto_20190109_0052', '2021-12-08 16:40:57.600860'),
(43, 'django_db_logger', '0003_alter_statuslog_id', '2021-12-08 16:40:57.785809'),
(44, 'fcm_django', '0001_initial', '2021-12-08 16:40:58.133898'),
(45, 'fcm_django', '0002_auto_20160808_1645', '2021-12-08 16:40:58.379306'),
(46, 'fcm_django', '0003_auto_20170313_1314', '2021-12-08 16:40:58.480198'),
(47, 'fcm_django', '0004_auto_20181128_1642', '2021-12-08 16:40:58.626454'),
(48, 'fcm_django', '0005_auto_20170808_1145', '2021-12-08 16:40:58.670593'),
(49, 'fcm_django', '0006_alter_fcmdevice_id', '2021-12-08 16:40:58.872375'),
(50, 'jobapp', '0001_initial', '2021-12-08 16:41:03.707663'),
(51, 'sessions', '0001_initial', '2021-12-08 16:41:03.838058'),
(52, 'tracking', '0001_initial', '2021-12-08 16:41:04.482681'),
(53, 'tracking', '0002_auto_20180918_2014', '2021-12-08 16:41:04.558281'),
(54, 'tracking', '0003_alter_pageview_id', '2021-12-08 16:41:04.714101');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('rt04rjn0m2rkg523eqe9ow3g1p6tajqw', 'e30:1mv00D:6M_biRVvpAvpz6ZhvmIIaA8Gg6mVklsvjFqrirE1-lI', '2021-12-22 16:41:09.603002'),
('x86img5iv9vb0edcck93avohv5jrtzmi', 'e30:1mv04n:ccmh_EDV6q8fVAeXavl87506p4wHVs5-iJzs3U9cRn0', '2021-12-22 16:45:53.387042');

-- --------------------------------------------------------

--
-- Table structure for table `fcm_django_fcmdevice`
--

CREATE TABLE `fcm_django_fcmdevice` (
  `id` bigint NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `date_created` datetime(6) DEFAULT NULL,
  `device_id` varchar(150) DEFAULT NULL,
  `registration_id` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobapp_job`
--

CREATE TABLE `jobapp_job` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `hiring_manager_name` varchar(255) NOT NULL,
  `hiring_company` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext,
  `detail` longtext,
  `address` varchar(255) NOT NULL,
  `zipcode` varchar(255) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `hourly_rate` int NOT NULL,
  `number_of_roles` int DEFAULT NULL,
  `publish` tinyint(1) NOT NULL,
  `IsDeleted` tinyint(1) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `city_id` bigint NOT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `state_id` bigint NOT NULL,
  `subscription_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobapp_joboffer`
--

CREATE TABLE `jobapp_joboffer` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `instruction` longtext,
  `action` varchar(25) NOT NULL,
  `isPayrollService` tinyint(1) NOT NULL,
  `contacted` tinyint(1) NOT NULL,
  `rating` int DEFAULT NULL,
  `showed_up` varchar(10) DEFAULT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `IsRead` tinyint(1) NOT NULL,
  `read_ipaddress` char(39) DEFAULT NULL,
  `read_source` varchar(10) NOT NULL,
  `read_browserinfo` longtext,
  `read_datetime` datetime(6) DEFAULT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `job_id` bigint NOT NULL,
  `read_by_id` bigint DEFAULT NULL,
  `subscription_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobapp_jobofferaction`
--

CREATE TABLE `jobapp_jobofferaction` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `action` varchar(25) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `joboffer_id` bigint NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobapp_jobshiftschedule`
--

CREATE TABLE `jobapp_jobshiftschedule` (
  `id` bigint NOT NULL,
  `token` char(32) NOT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `sun` tinyint(1) NOT NULL,
  `sun_start_hr` int NOT NULL,
  `sun_start_ap` varchar(10) DEFAULT NULL,
  `sun_end_hr` int DEFAULT NULL,
  `sun_end_ap` varchar(10) DEFAULT NULL,
  `mon` tinyint(1) NOT NULL,
  `mon_start_hr` int NOT NULL,
  `mon_start_ap` varchar(10) DEFAULT NULL,
  `mon_end_hr` int DEFAULT NULL,
  `mon_end_ap` varchar(10) DEFAULT NULL,
  `tue` tinyint(1) NOT NULL,
  `tue_start_hr` int NOT NULL,
  `tue_start_ap` varchar(10) DEFAULT NULL,
  `tue_end_hr` int DEFAULT NULL,
  `tue_end_ap` varchar(10) DEFAULT NULL,
  `wed` tinyint(1) NOT NULL,
  `wed_start_hr` int NOT NULL,
  `wed_start_ap` varchar(10) DEFAULT NULL,
  `wed_end_hr` int DEFAULT NULL,
  `wed_end_ap` varchar(10) DEFAULT NULL,
  `thu` tinyint(1) NOT NULL,
  `thu_start_hr` int NOT NULL,
  `thu_start_ap` varchar(10) DEFAULT NULL,
  `thu_end_hr` int DEFAULT NULL,
  `thu_end_ap` varchar(10) DEFAULT NULL,
  `fri` tinyint(1) NOT NULL,
  `fri_start_hr` int NOT NULL,
  `fri_start_ap` varchar(10) DEFAULT NULL,
  `fri_end_hr` int DEFAULT NULL,
  `fri_end_ap` varchar(10) DEFAULT NULL,
  `sat` tinyint(1) NOT NULL,
  `sat_start_hr` int NOT NULL,
  `sat_start_ap` varchar(10) DEFAULT NULL,
  `sat_end_hr` int DEFAULT NULL,
  `sat_end_ap` varchar(10) DEFAULT NULL,
  `createdAt` datetime(6) NOT NULL,
  `ipaddress` char(39) DEFAULT NULL,
  `source` varchar(10) NOT NULL,
  `browserinfo` longtext,
  `updatedAt` datetime(6) NOT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  `job_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobapp_job_subcategory`
--

CREATE TABLE `jobapp_job_subcategory` (
  `id` bigint NOT NULL,
  `job_id` bigint NOT NULL,
  `subcategory_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tracking_pageview`
--

CREATE TABLE `tracking_pageview` (
  `id` bigint NOT NULL,
  `url` longtext NOT NULL,
  `referer` longtext,
  `query_string` longtext,
  `method` varchar(20) DEFAULT NULL,
  `view_time` datetime(6) NOT NULL,
  `visitor_id` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tracking_pageview`
--

INSERT INTO `tracking_pageview` (`id`, `url`, `referer`, `query_string`, `method`, `view_time`, `visitor_id`) VALUES
(1, '/find-job-seekers', 'http://localhost:8000/dashboard', '', 'GET', '2021-12-08 16:41:09.582017', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(2, '/', NULL, '', 'GET', '2021-12-08 16:41:13.191928', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(3, '/sign-up', 'http://localhost:8000/', '', 'GET', '2021-12-08 16:41:15.530302', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(4, '/find-job-seekers', NULL, '', 'GET', '2021-12-08 16:42:40.798905', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(5, '/', NULL, '', 'GET', '2021-12-08 16:45:53.357039', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(6, '/dashboard', NULL, '', 'GET', '2021-12-08 16:46:00.028785', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(7, '/find-job-seekers', NULL, '', 'GET', '2021-12-08 16:58:15.100403', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(8, '/', NULL, '', 'GET', '2021-12-08 16:58:30.949449', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(9, '/find-job-seekers', NULL, '', 'GET', '2021-12-08 17:00:57.484847', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(10, '/find-job-seekers', NULL, '', 'GET', '2021-12-08 17:05:40.351663', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(11, '/find-job-seekers', NULL, '', 'GET', '2021-12-08 17:06:24.557855', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(12, '/find-job-seekers', NULL, '', 'GET', '2021-12-08 17:09:24.698394', 'rt04rjn0m2rkg523eqe9ow3g1p6tajqw'),
(13, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:09:16.628302', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(14, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:09:17.043808', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(15, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:09:17.997066', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(16, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:09:38.718002', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(17, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:09:38.932785', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(18, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:14:09.274541', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(19, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 21:14:30.075611', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(20, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:12:14.095893', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(21, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:14:39.143360', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(22, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:15:26.023037', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(23, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:15:41.942954', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(24, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:16:46.212131', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(25, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:17:21.725503', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(26, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:23:11.909161', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(27, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:23:48.924646', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(28, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:28:03.973268', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(29, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:28:15.583466', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(30, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:28:54.320237', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(31, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:29:25.095297', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(32, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:30:17.276663', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(33, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:30:24.988927', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(34, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:30:36.825341', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(35, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:30:47.941863', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(36, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:31:03.767992', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(37, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:33:24.009176', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(38, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:33:51.429825', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(39, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:34:17.609970', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(40, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:35:59.866289', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(41, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:36:59.752055', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(42, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:38:56.979044', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(43, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:39:48.654179', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(44, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:40:25.411836', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(45, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:42:36.674500', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(46, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:43:28.521578', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(47, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:44:23.706933', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(48, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:44:55.060964', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(49, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:45:10.569222', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(50, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:46:07.736274', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(51, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:46:32.528487', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(52, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:47:26.884787', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(53, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:48:10.775720', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(54, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:50:21.643922', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(55, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:50:41.730472', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(56, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:50:54.472836', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(57, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:51:07.756576', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(58, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:52:25.478228', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(59, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:52:55.707952', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(60, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:53:57.183468', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(61, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:54:26.049634', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(62, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:55:01.400023', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(63, '/find-job-seekers', NULL, '', 'GET', '2021-12-10 22:55:33.151564', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(64, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:39:22.841427', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(65, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:42:57.875661', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(66, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:43:30.965619', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(67, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:45:00.781904', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(68, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:45:40.786980', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(69, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:45:52.488661', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(70, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:46:30.901072', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(71, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:48:31.677200', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(72, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:49:07.447903', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(73, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:49:43.407279', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(74, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:49:51.933026', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(75, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:50:06.282494', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(76, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:51:39.878898', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(77, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:52:50.065229', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(78, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:52:54.668323', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(79, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:53:11.709532', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(80, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:53:28.210285', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(81, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:53:48.792724', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(82, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:54:23.776697', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(83, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:54:39.804493', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(84, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:55:10.927056', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(85, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:55:26.172577', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(86, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:55:40.274470', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(87, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 11:56:20.110566', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(88, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:00:05.848428', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(89, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:00:37.943556', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(90, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:01:10.891921', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(91, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:01:48.310731', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(92, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:02:27.870168', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(93, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:03:09.673184', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(94, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:03:44.867276', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(95, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:03:58.662137', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(96, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 12:04:47.294008', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(97, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:11:36.069275', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(98, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:16:01.463862', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(99, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:16:21.269150', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(100, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:16:30.466081', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(101, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:16:47.213409', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(102, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:16:59.934809', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(103, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:17:07.280971', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(104, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:23:07.804009', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(105, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:40:17.290916', 'x86img5iv9vb0edcck93avohv5jrtzmi'),
(106, '/find-job-seekers', NULL, '', 'GET', '2021-12-11 13:41:44.707107', 'x86img5iv9vb0edcck93avohv5jrtzmi');

-- --------------------------------------------------------

--
-- Table structure for table `tracking_visitor`
--

CREATE TABLE `tracking_visitor` (
  `session_key` varchar(40) NOT NULL,
  `ip_address` varchar(39) NOT NULL,
  `user_agent` longtext,
  `start_time` datetime(6) NOT NULL,
  `expiry_age` int DEFAULT NULL,
  `expiry_time` datetime(6) DEFAULT NULL,
  `time_on_site` int DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tracking_visitor`
--

INSERT INTO `tracking_visitor` (`session_key`, `ip_address`, `user_agent`, `start_time`, `expiry_age`, `expiry_time`, `time_on_site`, `end_time`, `user_id`) VALUES
('rt04rjn0m2rkg523eqe9ow3g1p6tajqw', '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', '2021-12-08 16:41:09.583398', 1209600, '2021-12-22 17:09:24.699480', 1695, NULL, NULL),
('x86img5iv9vb0edcck93avohv5jrtzmi', '127.0.0.1', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', '2021-12-08 16:45:53.358851', 1209600, '2021-12-25 13:41:44.708764', 248151, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accountapp_adminnotification`
--
ALTER TABLE `accountapp_adminnotification`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `accountapp_adminnoti_createdBy_id_57ef06f8_fk_accountap` (`createdBy_id`),
  ADD KEY `accountapp_adminnoti_readBy_id_6c5833ba_fk_accountap` (`readBy_id`);

--
-- Indexes for table `accountapp_category`
--
ALTER TABLE `accountapp_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `accountapp_city`
--
ALTER TABLE `accountapp_city`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountapp_city_state_id_45aaf398_fk_accountapp_state_id` (`state_id`);

--
-- Indexes for table `accountapp_contactus`
--
ALTER TABLE `accountapp_contactus`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountapp_contactus_user_id_3a278398_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `accountapp_language`
--
ALTER TABLE `accountapp_language`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `accountapp_newsletter`
--
ALTER TABLE `accountapp_newsletter`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `accountapp_newsletter_user_id_66299ee0_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `accountapp_notification`
--
ALTER TABLE `accountapp_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountapp_notificat_createdBy_id_ef7fc978_fk_accountap` (`createdBy_id`),
  ADD KEY `accountapp_notification_user_id_beabaa86_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `accountapp_plan`
--
ALTER TABLE `accountapp_plan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `accountapp_plan_createdBy_id_8b2787f5_fk_accountapp_user_id` (`createdBy_id`);

--
-- Indexes for table `accountapp_schedule`
--
ALTER TABLE `accountapp_schedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `accountapp_schedule_createdBy_id_59ded338_fk_accountapp_user_id` (`createdBy_id`),
  ADD KEY `accountapp_schedule_user_id_796fc22d_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `accountapp_state`
--
ALTER TABLE `accountapp_state`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `accountapp_subcategory`
--
ALTER TABLE `accountapp_subcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `accountapp_subcatego_category_id_607e4f3b_fk_accountap` (`category_id`);

--
-- Indexes for table `accountapp_subscription`
--
ALTER TABLE `accountapp_subscription`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountapp_subscript_createdBy_id_3b7e28c9_fk_accountap` (`createdBy_id`),
  ADD KEY `accountapp_subscription_plan_id_15c2376b_fk_accountapp_plan_id` (`plan_id`),
  ADD KEY `accountapp_subscription_user_id_0e5c1c0a_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `accountapp_temporarypassword`
--
ALTER TABLE `accountapp_temporarypassword`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `accountapp_temporary_user_id_93980233_fk_accountap` (`user_id`);

--
-- Indexes for table `accountapp_user`
--
ALTER TABLE `accountapp_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `mobile` (`mobile`),
  ADD KEY `accountapp_user_city_id_7e222862_fk_accountapp_city_id` (`city_id`),
  ADD KEY `accountapp_user_createdBy_id_af0f974b_fk_accountapp_user_id` (`createdBy_id`),
  ADD KEY `accountapp_user_state_id_b1e34259_fk_accountapp_state_id` (`state_id`);

--
-- Indexes for table `accountapp_usercategory`
--
ALTER TABLE `accountapp_usercategory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountapp_usercateg_category_id_33e351c2_fk_accountap` (`category_id`),
  ADD KEY `accountapp_usercategory_user_id_98bff5b2_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `accountapp_usercategory_subcategory`
--
ALTER TABLE `accountapp_usercategory_subcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accountapp_usercategory__usercategory_id_subcateg_be8e2337_uniq` (`usercategory_id`,`subcategory_id`),
  ADD KEY `accountapp_usercateg_subcategory_id_43bb8b53_fk_accountap` (`subcategory_id`);

--
-- Indexes for table `accountapp_userprofileview`
--
ALTER TABLE `accountapp_userprofileview`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountapp_userprofi_user_id_a3c17b44_fk_accountap` (`user_id`),
  ADD KEY `accountapp_userprofi_viewby_id_995469af_fk_accountap` (`viewby_id`);

--
-- Indexes for table `accountapp_user_groups`
--
ALTER TABLE `accountapp_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accountapp_user_groups_user_id_group_id_6953f1cc_uniq` (`user_id`,`group_id`),
  ADD KEY `accountapp_user_groups_group_id_27db1783_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `accountapp_user_language`
--
ALTER TABLE `accountapp_user_language`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accountapp_user_language_user_id_language_id_ea5ee5e0_uniq` (`user_id`,`language_id`),
  ADD KEY `accountapp_user_lang_language_id_6d510edf_fk_accountap` (`language_id`);

--
-- Indexes for table `accountapp_user_user_permissions`
--
ALTER TABLE `accountapp_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accountapp_user_user_per_user_id_permission_id_e16405c7_uniq` (`user_id`,`permission_id`),
  ADD KEY `accountapp_user_user_permission_id_1a75c1eb_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `apiapp_apiauthkey`
--
ALTER TABLE `apiapp_apiauthkey`
  ADD PRIMARY KEY (`key`),
  ADD KEY `apiapp_apiauthkey_createdBy_id_a9f997a7_fk_accountapp_user_id` (`createdBy_id`);

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `blogapp_blog`
--
ALTER TABLE `blogapp_blog`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `blogapp_blog_category_id_51000120_fk_blogapp_blogcategory_id` (`category_id`),
  ADD KEY `blogapp_blog_createdBy_id_80ff3b68_fk_accountapp_user_id` (`createdBy_id`);

--
-- Indexes for table `blogapp_blogcategory`
--
ALTER TABLE `blogapp_blogcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `blogapp_blogcomment`
--
ALTER TABLE `blogapp_blogcomment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blogapp_blogcomment_blog_id_9fd8ba82_fk_blogapp_blog_id` (`blog_id`),
  ADD KEY `blogapp_blogcomment_user_id_1373c5cb_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `blogapp_blogview`
--
ALTER TABLE `blogapp_blogview`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blogapp_blogview_blog_id_e31d4a13_fk_blogapp_blog_id` (`blog_id`),
  ADD KEY `blogapp_blogview_user_id_1c3e1a16_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `django_celery_beat_clockedschedule`
--
ALTER TABLE `django_celery_beat_clockedschedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_celery_beat_crontabschedule`
--
ALTER TABLE `django_celery_beat_crontabschedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_celery_beat_intervalschedule`
--
ALTER TABLE `django_celery_beat_intervalschedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_celery_beat_periodictask`
--
ALTER TABLE `django_celery_beat_periodictask`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  ADD KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  ADD KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  ADD KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`);

--
-- Indexes for table `django_celery_beat_periodictasks`
--
ALTER TABLE `django_celery_beat_periodictasks`
  ADD PRIMARY KEY (`ident`);

--
-- Indexes for table `django_celery_beat_solarschedule`
--
ALTER TABLE `django_celery_beat_solarschedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_db_logger_statuslog`
--
ALTER TABLE `django_db_logger_statuslog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_db_logger_statuslog_level_3c380d31` (`level`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `fcm_django_fcmdevice`
--
ALTER TABLE `fcm_django_fcmdevice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fcm_django_fcmdevice_user_id_6cdfc0a2_fk_accountapp_user_id` (`user_id`),
  ADD KEY `fcm_django_fcmdevice_device_id_a9406c36` (`device_id`);

--
-- Indexes for table `jobapp_job`
--
ALTER TABLE `jobapp_job`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `jobapp_job_category_id_3a0e51b4_fk_accountapp_category_id` (`category_id`),
  ADD KEY `jobapp_job_city_id_d813d133_fk_accountapp_city_id` (`city_id`),
  ADD KEY `jobapp_job_createdBy_id_f319c4a5_fk_accountapp_user_id` (`createdBy_id`),
  ADD KEY `jobapp_job_state_id_aa4bc081_fk_accountapp_state_id` (`state_id`),
  ADD KEY `jobapp_job_subscription_id_169a50ae_fk_accountap` (`subscription_id`),
  ADD KEY `jobapp_job_user_id_0153e37a_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `jobapp_joboffer`
--
ALTER TABLE `jobapp_joboffer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobapp_joboffer_createdBy_id_f6582514_fk_accountapp_user_id` (`createdBy_id`),
  ADD KEY `jobapp_joboffer_job_id_64c4b15f_fk_jobapp_job_id` (`job_id`),
  ADD KEY `jobapp_joboffer_read_by_id_61a1353b_fk_accountapp_user_id` (`read_by_id`),
  ADD KEY `jobapp_joboffer_subscription_id_b7a36724_fk_accountap` (`subscription_id`),
  ADD KEY `jobapp_joboffer_user_id_8c83d1b2_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `jobapp_jobofferaction`
--
ALTER TABLE `jobapp_jobofferaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobapp_jobofferactio_createdBy_id_020fac6b_fk_accountap` (`createdBy_id`),
  ADD KEY `jobapp_jobofferaction_joboffer_id_53309c26_fk_jobapp_joboffer_id` (`joboffer_id`),
  ADD KEY `jobapp_jobofferaction_user_id_fb9cbe34_fk_accountapp_user_id` (`user_id`);

--
-- Indexes for table `jobapp_jobshiftschedule`
--
ALTER TABLE `jobapp_jobshiftschedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD UNIQUE KEY `job_id` (`job_id`),
  ADD KEY `jobapp_jobshiftsched_createdBy_id_b6c2aaf9_fk_accountap` (`createdBy_id`);

--
-- Indexes for table `jobapp_job_subcategory`
--
ALTER TABLE `jobapp_job_subcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `jobapp_job_subcategory_job_id_subcategory_id_1bc3c8a9_uniq` (`job_id`,`subcategory_id`),
  ADD KEY `jobapp_job_subcatego_subcategory_id_346ee970_fk_accountap` (`subcategory_id`);

--
-- Indexes for table `tracking_pageview`
--
ALTER TABLE `tracking_pageview`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tracking_pageview_visitor_id_a78682e5_fk_tracking_` (`visitor_id`);

--
-- Indexes for table `tracking_visitor`
--
ALTER TABLE `tracking_visitor`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `tracking_visitor_user_id_68f9235e_fk_accountapp_user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accountapp_adminnotification`
--
ALTER TABLE `accountapp_adminnotification`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_category`
--
ALTER TABLE `accountapp_category`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_city`
--
ALTER TABLE `accountapp_city`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_contactus`
--
ALTER TABLE `accountapp_contactus`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_language`
--
ALTER TABLE `accountapp_language`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_newsletter`
--
ALTER TABLE `accountapp_newsletter`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_notification`
--
ALTER TABLE `accountapp_notification`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_plan`
--
ALTER TABLE `accountapp_plan`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_schedule`
--
ALTER TABLE `accountapp_schedule`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_state`
--
ALTER TABLE `accountapp_state`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_subcategory`
--
ALTER TABLE `accountapp_subcategory`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_subscription`
--
ALTER TABLE `accountapp_subscription`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_temporarypassword`
--
ALTER TABLE `accountapp_temporarypassword`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_user`
--
ALTER TABLE `accountapp_user`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `accountapp_usercategory`
--
ALTER TABLE `accountapp_usercategory`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_usercategory_subcategory`
--
ALTER TABLE `accountapp_usercategory_subcategory`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_userprofileview`
--
ALTER TABLE `accountapp_userprofileview`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_user_groups`
--
ALTER TABLE `accountapp_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_user_language`
--
ALTER TABLE `accountapp_user_language`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accountapp_user_user_permissions`
--
ALTER TABLE `accountapp_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=170;

--
-- AUTO_INCREMENT for table `blogapp_blog`
--
ALTER TABLE `blogapp_blog`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blogapp_blogcategory`
--
ALTER TABLE `blogapp_blogcategory`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blogapp_blogcomment`
--
ALTER TABLE `blogapp_blogcomment`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blogapp_blogview`
--
ALTER TABLE `blogapp_blogview`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_clockedschedule`
--
ALTER TABLE `django_celery_beat_clockedschedule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_crontabschedule`
--
ALTER TABLE `django_celery_beat_crontabschedule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_intervalschedule`
--
ALTER TABLE `django_celery_beat_intervalschedule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_periodictask`
--
ALTER TABLE `django_celery_beat_periodictask`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_solarschedule`
--
ALTER TABLE `django_celery_beat_solarschedule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `django_db_logger_statuslog`
--
ALTER TABLE `django_db_logger_statuslog`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=206;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `fcm_django_fcmdevice`
--
ALTER TABLE `fcm_django_fcmdevice`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobapp_job`
--
ALTER TABLE `jobapp_job`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobapp_joboffer`
--
ALTER TABLE `jobapp_joboffer`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobapp_jobofferaction`
--
ALTER TABLE `jobapp_jobofferaction`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobapp_jobshiftschedule`
--
ALTER TABLE `jobapp_jobshiftschedule`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobapp_job_subcategory`
--
ALTER TABLE `jobapp_job_subcategory`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tracking_pageview`
--
ALTER TABLE `tracking_pageview`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=107;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accountapp_adminnotification`
--
ALTER TABLE `accountapp_adminnotification`
  ADD CONSTRAINT `accountapp_adminnoti_createdBy_id_57ef06f8_fk_accountap` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `accountapp_adminnoti_readBy_id_6c5833ba_fk_accountap` FOREIGN KEY (`readBy_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_city`
--
ALTER TABLE `accountapp_city`
  ADD CONSTRAINT `accountapp_city_state_id_45aaf398_fk_accountapp_state_id` FOREIGN KEY (`state_id`) REFERENCES `accountapp_state` (`id`);

--
-- Constraints for table `accountapp_contactus`
--
ALTER TABLE `accountapp_contactus`
  ADD CONSTRAINT `accountapp_contactus_user_id_3a278398_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_newsletter`
--
ALTER TABLE `accountapp_newsletter`
  ADD CONSTRAINT `accountapp_newsletter_user_id_66299ee0_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_notification`
--
ALTER TABLE `accountapp_notification`
  ADD CONSTRAINT `accountapp_notificat_createdBy_id_ef7fc978_fk_accountap` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `accountapp_notification_user_id_beabaa86_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_plan`
--
ALTER TABLE `accountapp_plan`
  ADD CONSTRAINT `accountapp_plan_createdBy_id_8b2787f5_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_schedule`
--
ALTER TABLE `accountapp_schedule`
  ADD CONSTRAINT `accountapp_schedule_createdBy_id_59ded338_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `accountapp_schedule_user_id_796fc22d_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_subcategory`
--
ALTER TABLE `accountapp_subcategory`
  ADD CONSTRAINT `accountapp_subcatego_category_id_607e4f3b_fk_accountap` FOREIGN KEY (`category_id`) REFERENCES `accountapp_category` (`id`);

--
-- Constraints for table `accountapp_subscription`
--
ALTER TABLE `accountapp_subscription`
  ADD CONSTRAINT `accountapp_subscript_createdBy_id_3b7e28c9_fk_accountap` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `accountapp_subscription_plan_id_15c2376b_fk_accountapp_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `accountapp_plan` (`id`),
  ADD CONSTRAINT `accountapp_subscription_user_id_0e5c1c0a_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_temporarypassword`
--
ALTER TABLE `accountapp_temporarypassword`
  ADD CONSTRAINT `accountapp_temporary_user_id_93980233_fk_accountap` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_user`
--
ALTER TABLE `accountapp_user`
  ADD CONSTRAINT `accountapp_user_city_id_7e222862_fk_accountapp_city_id` FOREIGN KEY (`city_id`) REFERENCES `accountapp_city` (`id`),
  ADD CONSTRAINT `accountapp_user_createdBy_id_af0f974b_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `accountapp_user_state_id_b1e34259_fk_accountapp_state_id` FOREIGN KEY (`state_id`) REFERENCES `accountapp_state` (`id`);

--
-- Constraints for table `accountapp_usercategory`
--
ALTER TABLE `accountapp_usercategory`
  ADD CONSTRAINT `accountapp_usercateg_category_id_33e351c2_fk_accountap` FOREIGN KEY (`category_id`) REFERENCES `accountapp_category` (`id`),
  ADD CONSTRAINT `accountapp_usercategory_user_id_98bff5b2_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_usercategory_subcategory`
--
ALTER TABLE `accountapp_usercategory_subcategory`
  ADD CONSTRAINT `accountapp_usercateg_subcategory_id_43bb8b53_fk_accountap` FOREIGN KEY (`subcategory_id`) REFERENCES `accountapp_subcategory` (`id`),
  ADD CONSTRAINT `accountapp_usercateg_usercategory_id_4bf3fba9_fk_accountap` FOREIGN KEY (`usercategory_id`) REFERENCES `accountapp_usercategory` (`id`);

--
-- Constraints for table `accountapp_userprofileview`
--
ALTER TABLE `accountapp_userprofileview`
  ADD CONSTRAINT `accountapp_userprofi_user_id_a3c17b44_fk_accountap` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `accountapp_userprofi_viewby_id_995469af_fk_accountap` FOREIGN KEY (`viewby_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_user_groups`
--
ALTER TABLE `accountapp_user_groups`
  ADD CONSTRAINT `accountapp_user_groups_group_id_27db1783_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `accountapp_user_groups_user_id_5cc42cbd_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_user_language`
--
ALTER TABLE `accountapp_user_language`
  ADD CONSTRAINT `accountapp_user_lang_language_id_6d510edf_fk_accountap` FOREIGN KEY (`language_id`) REFERENCES `accountapp_language` (`id`),
  ADD CONSTRAINT `accountapp_user_language_user_id_69ef6736_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `accountapp_user_user_permissions`
--
ALTER TABLE `accountapp_user_user_permissions`
  ADD CONSTRAINT `accountapp_user_user_permission_id_1a75c1eb_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `accountapp_user_user_user_id_f406cc6e_fk_accountap` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `apiapp_apiauthkey`
--
ALTER TABLE `apiapp_apiauthkey`
  ADD CONSTRAINT `apiapp_apiauthkey_createdBy_id_a9f997a7_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `blogapp_blog`
--
ALTER TABLE `blogapp_blog`
  ADD CONSTRAINT `blogapp_blog_category_id_51000120_fk_blogapp_blogcategory_id` FOREIGN KEY (`category_id`) REFERENCES `blogapp_blogcategory` (`id`),
  ADD CONSTRAINT `blogapp_blog_createdBy_id_80ff3b68_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `blogapp_blogcomment`
--
ALTER TABLE `blogapp_blogcomment`
  ADD CONSTRAINT `blogapp_blogcomment_blog_id_9fd8ba82_fk_blogapp_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blogapp_blog` (`id`),
  ADD CONSTRAINT `blogapp_blogcomment_user_id_1373c5cb_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `blogapp_blogview`
--
ALTER TABLE `blogapp_blogview`
  ADD CONSTRAINT `blogapp_blogview_blog_id_e31d4a13_fk_blogapp_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blogapp_blog` (`id`),
  ADD CONSTRAINT `blogapp_blogview_user_id_1c3e1a16_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `django_celery_beat_periodictask`
--
ALTER TABLE `django_celery_beat_periodictask`
  ADD CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  ADD CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  ADD CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  ADD CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`);

--
-- Constraints for table `fcm_django_fcmdevice`
--
ALTER TABLE `fcm_django_fcmdevice`
  ADD CONSTRAINT `fcm_django_fcmdevice_user_id_6cdfc0a2_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `jobapp_job`
--
ALTER TABLE `jobapp_job`
  ADD CONSTRAINT `jobapp_job_category_id_3a0e51b4_fk_accountapp_category_id` FOREIGN KEY (`category_id`) REFERENCES `accountapp_category` (`id`),
  ADD CONSTRAINT `jobapp_job_city_id_d813d133_fk_accountapp_city_id` FOREIGN KEY (`city_id`) REFERENCES `accountapp_city` (`id`),
  ADD CONSTRAINT `jobapp_job_createdBy_id_f319c4a5_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `jobapp_job_state_id_aa4bc081_fk_accountapp_state_id` FOREIGN KEY (`state_id`) REFERENCES `accountapp_state` (`id`),
  ADD CONSTRAINT `jobapp_job_subscription_id_169a50ae_fk_accountap` FOREIGN KEY (`subscription_id`) REFERENCES `accountapp_subscription` (`id`),
  ADD CONSTRAINT `jobapp_job_user_id_0153e37a_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `jobapp_joboffer`
--
ALTER TABLE `jobapp_joboffer`
  ADD CONSTRAINT `jobapp_joboffer_createdBy_id_f6582514_fk_accountapp_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `jobapp_joboffer_job_id_64c4b15f_fk_jobapp_job_id` FOREIGN KEY (`job_id`) REFERENCES `jobapp_job` (`id`),
  ADD CONSTRAINT `jobapp_joboffer_read_by_id_61a1353b_fk_accountapp_user_id` FOREIGN KEY (`read_by_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `jobapp_joboffer_subscription_id_b7a36724_fk_accountap` FOREIGN KEY (`subscription_id`) REFERENCES `accountapp_subscription` (`id`),
  ADD CONSTRAINT `jobapp_joboffer_user_id_8c83d1b2_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `jobapp_jobofferaction`
--
ALTER TABLE `jobapp_jobofferaction`
  ADD CONSTRAINT `jobapp_jobofferactio_createdBy_id_020fac6b_fk_accountap` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `jobapp_jobofferaction_joboffer_id_53309c26_fk_jobapp_joboffer_id` FOREIGN KEY (`joboffer_id`) REFERENCES `jobapp_joboffer` (`id`),
  ADD CONSTRAINT `jobapp_jobofferaction_user_id_fb9cbe34_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);

--
-- Constraints for table `jobapp_jobshiftschedule`
--
ALTER TABLE `jobapp_jobshiftschedule`
  ADD CONSTRAINT `jobapp_jobshiftsched_createdBy_id_b6c2aaf9_fk_accountap` FOREIGN KEY (`createdBy_id`) REFERENCES `accountapp_user` (`id`),
  ADD CONSTRAINT `jobapp_jobshiftschedule_job_id_b0fa972e_fk_jobapp_job_id` FOREIGN KEY (`job_id`) REFERENCES `jobapp_job` (`id`);

--
-- Constraints for table `jobapp_job_subcategory`
--
ALTER TABLE `jobapp_job_subcategory`
  ADD CONSTRAINT `jobapp_job_subcatego_subcategory_id_346ee970_fk_accountap` FOREIGN KEY (`subcategory_id`) REFERENCES `accountapp_subcategory` (`id`),
  ADD CONSTRAINT `jobapp_job_subcategory_job_id_105d7e51_fk_jobapp_job_id` FOREIGN KEY (`job_id`) REFERENCES `jobapp_job` (`id`);

--
-- Constraints for table `tracking_pageview`
--
ALTER TABLE `tracking_pageview`
  ADD CONSTRAINT `tracking_pageview_visitor_id_a78682e5_fk_tracking_` FOREIGN KEY (`visitor_id`) REFERENCES `tracking_visitor` (`session_key`);

--
-- Constraints for table `tracking_visitor`
--
ALTER TABLE `tracking_visitor`
  ADD CONSTRAINT `tracking_visitor_user_id_68f9235e_fk_accountapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `accountapp_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
