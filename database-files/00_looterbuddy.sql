-- Armor: table
CREATE TABLE `Armor` (
  `itemID` int NOT NULL,
  `armorID` int NOT NULL,
  `defense` int NOT NULL,
  PRIMARY KEY (`itemID`,`armorID`),
  UNIQUE KEY `armorID` (`armorID`),
  CONSTRAINT `Armor_ibfk_1` FOREIGN KEY (`itemID`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Comments: table
CREATE TABLE `Comments` (
  `userID` int NOT NULL,
  `commentID` int NOT NULL,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(1000) NOT NULL,
  `postID` int NOT NULL,
  PRIMARY KEY (`userID`,`commentID`),
  UNIQUE KEY `commentID` (`commentID`),
  KEY `postID` (`postID`),
  CONSTRAINT `Comments_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`) ON DELETE CASCADE,
  CONSTRAINT `Comments_ibfk_2` FOREIGN KEY (`postID`) REFERENCES `Posts` (`postID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: postID (index)

-- ContentCreators: table
CREATE TABLE `ContentCreators` (
  `streamerID` int NOT NULL AUTO_INCREMENT,
  `followCount` int NOT NULL,
  `category` enum('guides','entertainment','competitive') DEFAULT NULL,
  `description` text,
  `userID` int NOT NULL,
  PRIMARY KEY (`streamerID`),
  UNIQUE KEY `userID` (`userID`),
  CONSTRAINT `ContentCreators_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Developers: table
CREATE TABLE `Developers` (
  `developerID` int NOT NULL AUTO_INCREMENT,
  `experienceYears` int DEFAULT NULL,
  `userID` int NOT NULL,
  PRIMARY KEY (`developerID`),
  UNIQUE KEY `userID` (`userID`),
  CONSTRAINT `Developers_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Follows: table
CREATE TABLE `Follows` (
  `userID` int NOT NULL,
  `followID` int NOT NULL,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `streamerID` int NOT NULL,
  PRIMARY KEY (`userID`,`followID`),
  UNIQUE KEY `followID` (`followID`),
  KEY `streamerID` (`streamerID`),
  CONSTRAINT `Follows_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`),
  CONSTRAINT `Follows_ibfk_2` FOREIGN KEY (`streamerID`) REFERENCES `ContentCreators` (`streamerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: streamerID (index)

-- Inventory: table
CREATE TABLE `Inventory` (
  `playerID` int NOT NULL,
  `inventoryID` int NOT NULL,
  `itemID` int NOT NULL,
  PRIMARY KEY (`playerID`,`inventoryID`,`itemID`),
  UNIQUE KEY `inventoryID` (`inventoryID`),
  KEY `itemID` (`itemID`),
  CONSTRAINT `Inventory_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `Players` (`playerID`) ON DELETE CASCADE,
  CONSTRAINT `Inventory_ibfk_2` FOREIGN KEY (`itemID`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: itemID (index)

-- Items: table
CREATE TABLE `Items` (
  `itemID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `type` enum('weapon','armor') NOT NULL,
  `rarity` enum('common','uncommon','rare','epic') NOT NULL,
  PRIMARY KEY (`itemID`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Likes: table
CREATE TABLE `Likes` (
  `userID` int NOT NULL,
  `likeID` int NOT NULL,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `postID` int NOT NULL,
  PRIMARY KEY (`userID`,`likeID`),
  UNIQUE KEY `likeID` (`likeID`),
  KEY `postID` (`postID`),
  CONSTRAINT `Likes_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`) ON DELETE CASCADE,
  CONSTRAINT `Likes_ibfk_2` FOREIGN KEY (`postID`) REFERENCES `Posts` (`postID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: postID (index)

-- Loadout: table
CREATE TABLE `Loadout` (
  `playerID` int NOT NULL,
  `loadoutID` int NOT NULL,
  `weapon1` int DEFAULT NULL,
  `weapon2` int DEFAULT NULL,
  `armor1` int DEFAULT NULL,
  `armor2` int DEFAULT NULL,
  `armor3` int DEFAULT NULL,
  `dateUpdated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`playerID`,`loadoutID`),
  UNIQUE KEY `loadoutID` (`loadoutID`),
  KEY `weapon1` (`weapon1`),
  KEY `weapon2` (`weapon2`),
  KEY `armor1` (`armor1`),
  KEY `armor2` (`armor2`),
  KEY `armor3` (`armor3`),
  CONSTRAINT `Loadout_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `Players` (`playerID`) ON DELETE CASCADE,
  CONSTRAINT `Loadout_ibfk_2` FOREIGN KEY (`weapon1`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Loadout_ibfk_3` FOREIGN KEY (`weapon2`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Loadout_ibfk_4` FOREIGN KEY (`armor1`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Loadout_ibfk_5` FOREIGN KEY (`armor2`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Loadout_ibfk_6` FOREIGN KEY (`armor3`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: weapon1 (index)

-- No native definition for element: weapon2 (index)

-- No native definition for element: armor1 (index)

-- No native definition for element: armor2 (index)

-- No native definition for element: armor3 (index)

-- LoadoutUse: table
CREATE TABLE `LoadoutUse` (
  `playerID` int NOT NULL,
  `missionID` int NOT NULL,
  `loadoutUseID` int NOT NULL AUTO_INCREMENT,
  `weapon1` int DEFAULT NULL,
  `weapon2` int DEFAULT NULL,
  `armor1` int DEFAULT NULL,
  `armor2` int DEFAULT NULL,
  `armor3` int DEFAULT NULL,
  `dateUsed` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`loadoutUseID`),
  KEY `playerID` (`playerID`),
  KEY `missionID` (`missionID`),
  KEY `weapon1` (`weapon1`),
  KEY `weapon2` (`weapon2`),
  KEY `armor1` (`armor1`),
  KEY `armor2` (`armor2`),
  KEY `armor3` (`armor3`),
  CONSTRAINT `LoadoutUse_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `Players` (`playerID`) ON DELETE CASCADE,
  CONSTRAINT `LoadoutUse_ibfk_2` FOREIGN KEY (`missionID`) REFERENCES `Missions` (`missionID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `LoadoutUse_ibfk_3` FOREIGN KEY (`weapon1`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `LoadoutUse_ibfk_4` FOREIGN KEY (`weapon2`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `LoadoutUse_ibfk_5` FOREIGN KEY (`armor1`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `LoadoutUse_ibfk_6` FOREIGN KEY (`armor2`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `LoadoutUse_ibfk_7` FOREIGN KEY (`armor3`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: playerID (index)

-- No native definition for element: missionID (index)

-- No native definition for element: weapon1 (index)

-- No native definition for element: weapon2 (index)

-- No native definition for element: armor1 (index)

-- No native definition for element: armor2 (index)

-- No native definition for element: armor3 (index)

-- Missions: table
CREATE TABLE `Missions` (
  `missionID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`missionID`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Performance: table
CREATE TABLE `Performance` (
  `playerID` int NOT NULL,
  `performanceID` int NOT NULL,
  `totalKills` int DEFAULT NULL,
  `totalDeaths` int DEFAULT NULL,
  `DPS` int DEFAULT NULL,
  `dateCompleted` datetime DEFAULT CURRENT_TIMESTAMP,
  `loadoutID` int NOT NULL,
  `missionID` int NOT NULL,
  PRIMARY KEY (`playerID`,`performanceID`),
  UNIQUE KEY `performanceID` (`performanceID`),
  KEY `loadoutID` (`loadoutID`),
  KEY `missionID` (`missionID`),
  CONSTRAINT `Performance_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `Players` (`playerID`) ON DELETE CASCADE,
  CONSTRAINT `Performance_ibfk_2` FOREIGN KEY (`loadoutID`) REFERENCES `Loadout` (`loadoutID`),
  CONSTRAINT `Performance_ibfk_3` FOREIGN KEY (`missionID`) REFERENCES `Missions` (`missionID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: loadoutID (index)

-- No native definition for element: missionID (index)

-- Players: table
CREATE TABLE `Players` (
  `playerID` int NOT NULL AUTO_INCREMENT,
  `level` int DEFAULT NULL,
  `experience` int DEFAULT NULL,
  `userID` int NOT NULL,
  PRIMARY KEY (`playerID`),
  UNIQUE KEY `userID` (`userID`),
  CONSTRAINT `Players_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `Users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Posts: table
CREATE TABLE `Posts` (
  `postID` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `tag` enum('update','social') NOT NULL,
  `dateUpdated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,
  `developerID` int DEFAULT NULL,
  `streamerID` int DEFAULT NULL,
  PRIMARY KEY (`postID`),
  KEY `developerID` (`developerID`),
  KEY `streamerID` (`streamerID`),
  CONSTRAINT `Posts_ibfk_1` FOREIGN KEY (`developerID`) REFERENCES `Developers` (`developerID`) ON DELETE SET NULL,
  CONSTRAINT `Posts_ibfk_2` FOREIGN KEY (`streamerID`) REFERENCES `ContentCreators` (`streamerID`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- No native definition for element: developerID (index)

-- No native definition for element: streamerID (index)

-- Users: table
CREATE TABLE `Users` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(30) NOT NULL,
  `lastName` varchar(30) DEFAULT NULL,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `type` enum('player','developer','streamer') NOT NULL DEFAULT 'player',
  `joinDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `phoneNumber` varchar(15) NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phoneNumber` (`phoneNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Weapons: table
CREATE TABLE `Weapons` (
  `itemID` int NOT NULL,
  `weaponID` int NOT NULL,
  `damage` int NOT NULL,
  `magSize` int NOT NULL,
  `fireRate` int NOT NULL,
  PRIMARY KEY (`itemID`,`weaponID`),
  UNIQUE KEY `weaponID` (`weaponID`),
  CONSTRAINT `Weapons_ibfk_1` FOREIGN KEY (`itemID`) REFERENCES `Items` (`itemID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


