-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: localhost    Database: databridge
-- ------------------------------------------------------
-- Server version	8.0.18


--
-- Table structure for table `auth_account`
--

DROP TABLE IF EXISTS `auth_account`;
CREATE TABLE `auth_account` (
  `id` char(32) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `status` int(8) NOT NULL DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_account`
-- 系统初始化超级用户账号
--

INSERT INTO `auth_account` VALUES
('800be36b639211ebb61b821700fd42c0','系统管理员','/app/databridge/images/admin-avatar.jpg',0,'2021-01-31 07:04:03'),
('d5b78510b80d11ed841aa45e60efbf2d','研发','/app/databridge/images/dev-avatar.png',0,'2023-03-01 08:48:27'),
('c1389506b89011edb818a45e60efbf2d','测试','/app/databridge/images/test-avatar.jpg',0,'2023-03-02 00:25:37'),
('4b8ff3b4bedd11eda80fa45e60efbf2d','游客','/app/databridge/images/default-avatar.jpg',0,'2023-03-10 00:48:38'),
('c67bf4e1611211ee8b1fa45e60efbf2d','编辑','/app/databridge/images/dev-avatar.png',0,'2023-03-01 08:48:27');

--
-- Table structure for table `auth_login`
--

DROP TABLE IF EXISTS `auth_login`;
CREATE TABLE `auth_login` (
  `loginName` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL COMMENT 'username, email, phone, wx, dingTalk',
  `accountId` char(32) NOT NULL,
  `status` int(8) NOT NULL DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`loginname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_login`
-- 默认密码 1232556
--

INSERT INTO `auth_login` VALUES
('admin','$2b$10$PRVvPNvJzuV1Y6hXdgtGO.UKlnJl.zT4Ax4XNTHJw0.wbb2f72e6e','username','800be36b639211ebb61b821700fd42c0',0,'2021-01-31 07:04:03'),
('dev','$2b$10$3CAHWSFsDmp5zexbT5atpOM/n9L3RWAxIUreF9TNZXkKWtvZuhPsq','username','d5b78510b80d11ed841aa45e60efbf2d',0,'2023-03-01 08:48:27'),
('test','$2b$10$FBLRFdaayMZ8UoMjXI7eWO0feI7dEKZivbTNC9DK.GAN0YQWRyblO','username','c1389506b89011edb818a45e60efbf2d',0,'2023-03-02 00:25:37'),
('guest','$2b$10$CxluaTpkrF4HdqjoZxV2M.paeppneyOEFu.jlL34ycjYLLixEZq1C','username','4b8ff3b4bedd11eda80fa45e60efbf2d',0,'2023-03-10 00:48:38'),
('editor','$2b$10$CxluaTpkrF4HdqjoZxV2M.paeppneyOEFu.jlL34ycjYLLixEZq1C','username','c67bf4e1611211ee8b1fa45e60efbf2d',0,'2023-03-10 00:48:38');

--
-- Table structure for table `auth_menu`
--

DROP TABLE IF EXISTS `auth_menu`;
CREATE TABLE `auth_menu` (
  `id` char(32) NOT NULL,
  `pid` char(32) NOT NULL,
  `lft` int(11) NOT NULL,
  `rgt` int(11) NOT NULL,
  `depth` int(8) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `hideInMenu` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Dumping data for table `auth_menu`
--

INSERT INTO `auth_menu` VALUES
('6299958ab73d11eda3e2a45e60efbf2d','00000000000000000000000000000000',1,2,0,'ROOT_MENU','','',0);

--
-- Table structure for table `auth_policy`
--

DROP TABLE IF EXISTS `auth_policy`;
CREATE TABLE `auth_policy` (
  `id` char(32) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `objName` varchar(255) DEFAULT NULL,
  `objId` varchar(255) DEFAULT NULL,
  `resPath` varchar(255) DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  `access` varchar(255) DEFAULT NULL,
  `priority` int(8) DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_policy`
--

INSERT INTO `auth_policy` VALUES
('0ab8e3c6237611ed9d30a45e60efbf2d','role','admin','507b9fd4646711ebb586821700fd42c0','/api/*','*','allow',100,'2022-08-23 22:29:01'),
('407886383d6011ee8e37a45e60efbf2d','role','dev','04e6f868280111ed9c74a45e60efbf2d','/api/*','*','allow',200,'2023-08-18 00:43:30'),
('c67bf4e1611211ee8b1fa45e60efbf2d','role','editor','fcf21dc7611211eeb6e2a45e60efbf2d','/api/*','*','allow',400,'2023-08-18 00:43:30'),
('9a0597043d6011ee8e37a45e60efbf2d','role','user','57cf20cabedb11eda80fa45e60efbf2d','/api/report-outputs/*','*','allow',300,'2023-08-18 00:46:00');


--
-- Table structure for table `auth_role`
--

DROP TABLE IF EXISTS `auth_role`;
CREATE TABLE `auth_role` (
  `id` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_role`
--

INSERT INTO `auth_role` VALUES
('507b9fd4646711ebb586821700fd42c0','admin',0,'2021-02-01 08:27:25'),
('04e6f868280111ed9c74a45e60efbf2d','dev',0,'2022-08-30 01:13:56'),
('db5d0a9c540a11ed8c07a45e60efbf2d','test',0,'2022-10-25 02:15:12'),
('bce4c8de540a11ed8c07a45e60efbf2d','guest',0,'2022-10-26 02:14:21'),
('57cf20cabedb11eda80fa45e60efbf2d','user',0,'2023-03-10 00:34:39'),
('fcf21dc7611211eeb6e2a45e60efbf2d','editor',0,'2022-08-30 01:13:56');


--
-- Table structure for table `auth_role_menu`
--

DROP TABLE IF EXISTS `auth_role_menu`;
CREATE TABLE `auth_role_menu` (
  `roleId` char(32) NOT NULL,
  `menuId` char(32) NOT NULL,
  PRIMARY KEY (`roleId`,`menuId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



--
-- Table structure for table `auth_role_form`
--

DROP TABLE IF EXISTS `auth_role_form`;
CREATE TABLE `auth_role_form` (
  `roleId` char(32) NOT NULL,
  `formId` char(32) NOT NULL,
  `authCreate` varchar(45) DEFAULT NULL,
  `authRemove` varchar(45) DEFAULT NULL,
  `authModify` varchar(45) DEFAULT NULL,
  `authQuery` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`roleId`,`formId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `auth_account_role`
--

DROP TABLE IF EXISTS `auth_account_role`;
CREATE TABLE `auth_account_role` (
  `accountId` char(32) NOT NULL,
  `roleId` char(32) NOT NULL,
  PRIMARY KEY (`accountId`,`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_account_role`
--

INSERT INTO `auth_account_role` VALUES
('800be36b639211ebb61b821700fd42c0','507b9fd4646711ebb586821700fd42c0'),
('d5b78510b80d11ed841aa45e60efbf2d','04e6f868280111ed9c74a45e60efbf2d'),
('c1389506b89011edb818a45e60efbf2d','db5d0a9c540a11ed8c07a45e60efbf2d'),
('4b8ff3b4bedd11eda80fa45e60efbf2d','bce4c8de540a11ed8c07a45e60efbf2d'),
('c67bf4e1611211ee8b1fa45e60efbf2d','fcf21dc7611211eeb6e2a45e60efbf2d');

--
-- Table structure for table `auth_account_group`
--

DROP TABLE IF EXISTS `auth_account_group`;
CREATE TABLE `auth_account_group` (
  `accountId` char(32) NOT NULL,
  `groupId` char(32) NOT NULL,
  PRIMARY KEY (`accountId`,`groupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `auth_verify_code`
--

DROP TABLE IF EXISTS `auth_verify_code`;
CREATE TABLE `auth_verify_code` (
  `loginName` varchar(45) NOT NULL,
  `code` varchar(255) NOT NULL,
  `mtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expiresAt` datetime NOT NULL,
  PRIMARY KEY (`loginName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` char(32) NOT NULL,
  `pid` char(32) NOT NULL,
  `title` varchar(255) NOT NULL,
  `lft` int(11) NOT NULL,
  `rgt` int(11) NOT NULL,
  `depth` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` VALUES
('26f2bf8022a111eda774a45e60efbf2d','00000000000000000000000000000000','总公司',1,2,0);


--
-- Table structure for table `sys_log`
--

DROP TABLE IF EXISTS `sys_log`;
CREATE TABLE `sys_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accountId` char(32) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `method` varchar(255) NOT NULL COMMENT '操作方法: POST, PUT, DELETE',
  `path` varchar(255) NOT NULL,
  `params` varchar(255) DEFAULT NULL,
  `body` text COMMENT '承载text数据',
  `respCode` int(8) NOT NULL COMMENT '操作结果',
  `respMsg` varchar(255) NOT NULL COMMENT '操作结果',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipAddr` varchar(255) DEFAULT NULL,
  `userAgent` varchar(255) DEFAULT NULL COMMENT'获取浏览器信息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sys_profile`
--

DROP TABLE IF EXISTS `sys_profile`;
CREATE TABLE `sys_profile` (
  `id` char(32) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sys_tree`
--

DROP TABLE IF EXISTS `sys_tree`;
CREATE TABLE `sys_tree` (
  `id` char(32) NOT NULL,
  `pid` char(32) NOT NULL,
  `rootid` char(32) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `lft` int(11) NOT NULL,
  `rgt` int(11) NOT NULL,
  `depth` int(8) NOT NULL DEFAULT '0',
  `num` int(8) NOT NULL DEFAULT '0',
  `status` int(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `sys_tree`
--

INSERT INTO `sys_tree` VALUES
('8f3b5a21ba6e11edb30238c9860954df','00000000000000000000000000000000','8f3b5a21ba6e11edb30238c9860954df','博客文章分类',NULL,1,2,0,0,1),
('57dc25ba6f5511ee977638c9860954df','00000000000000000000000000000000','57dc25ba6f5511ee977638c9860954df','业务系统',NULL,1,2,0,0,1);


--
-- Table structure for table `sys_notify`
--

DROP TABLE IF EXISTS `sys_notify`;
CREATE TABLE `sys_notify` (
  `id` char(32) NOT NULL,
  `status` int(8) NOT NULL DEFAULT '0',
  `title` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `type` varchar(255) NOT NULL,
  `extra` varchar(255) NOT NULL,
  `fromAccountId` char(32) DEFAULT NULL,
  `toAccountId` char(32) NOT NULL,
  `taskId` varchar(255) DEFAULT NULL,
  `formKey` varchar(255) DEFAULT NULL,
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sys_dictionary`
--

DROP TABLE IF EXISTS `sys_dictionary`;
CREATE TABLE `sys_dictionary` (
  `id` varchar(32) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `seq` int(8) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sys_file_blob`
--

DROP TABLE IF EXISTS `sys_file_blob`;
CREATE TABLE `sys_file_blob` (
  `id` char(32) NOT NULL,
  `bizid` varchar(45) NOT NULL,
  `blobCurrNum` int(8) NOT NULL DEFAULT '0',
  `blobTotalNum` int(8) NOT NULL DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `accountId` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`,`bizid`,`blobCurrNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sys_file`
--

DROP TABLE IF EXISTS `sys_file`;
CREATE TABLE `sys_file` (
  `id` char(32) NOT NULL,
  `localUrl` varchar(255) DEFAULT NULL,
  `cloudUrl` varchar(255) DEFAULT NULL,
  `filetype` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `blobTotalNum` int(8) NOT NULL DEFAULT '0',
  `size` bigint(19) NOT NULL DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `accountId` char(32) DEFAULT NULL,
  `ext` varchar(255) DEFAULT NULL,
  `bizid` varchar(255) DEFAULT NULL,
  `syncId` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_local_url` (`localUrl`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `auth_app_secret`
--

DROP TABLE IF EXISTS `auth_app_secret`;
CREATE TABLE `auth_app_secret` (
  `id` char(32) NOT NULL,
  `appname` varchar(255) DEFAULT NULL,
  `appkey` varchar(255) NOT NULL COMMENT '公匙, 相当于账号',
  `appsecret` varchar(255) NOT NULL COMMENT '私匙, 相当于密码',
  `status` int(8) NOT NULL DEFAULT '0',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `mtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `auth_app_role`
--

DROP TABLE IF EXISTS `auth_app_role`;
CREATE TABLE `auth_app_role` (
  `appId` char(32) NOT NULL,
  `roleId` char(32) NOT NULL,
  PRIMARY KEY (`appId`,`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
