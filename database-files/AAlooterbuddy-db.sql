DROP DATABASE IF EXISTS looterbuddy;
CREATE DATABASE IF NOT EXISTS looterbuddy;

USE looterbuddy;

CREATE TABLE Users (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(30) NOT NULL,
    lastName VARCHAR(30),
    username VARCHAR(25) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    type ENUM('player', 'developer', 'streamer') NOT NULL DEFAULT 'player',
    joinDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    phoneNumber VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE Players (
    playerID INT AUTO_INCREMENT PRIMARY KEY,
    level INT,
    experience INT,
    userID INT UNIQUE NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Developers (
    developerID INT AUTO_INCREMENT PRIMARY KEY,
    experienceYears INT,
    userID INT UNIQUE NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ContentCreators (
    streamerID INT AUTO_INCREMENT PRIMARY KEY,
    followCount INT NOT NULL,
    category ENUM('guides', 'entertainment', 'competitive'),
    description TEXT,
    userID INT UNIQUE NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Posts (
    postID INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    tag ENUM('update', 'social') NOT NULL,
    dateUpdated DATETIME DEFAULT CURRENT_TIMESTAMP
                   ON UPDATE CURRENT_TIMESTAMP,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    developerID INT,
    streamerID INT,
    FOREIGN KEY (developerID) REFERENCES Developers(developerID) ON DELETE SET NULL,
    FOREIGN KEY (streamerID) REFERENCES ContentCreators(streamerID) ON DELETE SET NULL
);

CREATE TABLE Likes (
    userID INT NOT NULL,
    likeID INT UNIQUE NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    postID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (postID) REFERENCES Posts(postID) ON DELETE CASCADE,
    PRIMARY KEY (userID, likeID)
);

CREATE TABLE Comments (
    userID INT NOT NULL,
    commentID INT UNIQUE NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    content VARCHAR(1000) NOT NULL,
    postID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (postID) REFERENCES Posts(postID) ON DELETE CASCADE,
    PRIMARY KEY (userID, commentID)
);

CREATE TABLE Follows (
    userID INT NOT NULL,
    followID INT AUTO_INCREMENT UNIQUE NOT NULL,
    dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    streamerID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (streamerID) REFERENCES ContentCreators(streamerID),
    PRIMARY KEY (followID)
);

CREATE TABLE Items (
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    type ENUM('weapon', 'armor') NOT NULL,
    rarity ENUM('common', 'uncommon', 'rare', 'epic') NOT NULL
);

CREATE TABLE Armor (
    itemID INT NOT NULL,
    armorID INT UNIQUE NOT NULL,
    defense INT NOT NULL,
    FOREIGN KEY (itemID) references Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (itemID, armorID)
);

CREATE TABLE Weapons (
    itemID INT NOT NULL,
    weaponID INT UNIQUE NOT NULL,
    damage INT NOT NULL,
    magSize INT NOT NULL,
    fireRate INT NOT NULL,
    FOREIGN KEY (itemID) references Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (itemID, weaponID)
);

CREATE TABLE Missions (
    missionID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE Inventory (
    playerID INT NOT NULL,
    inventoryID INT UNIQUE NOT NULL,
    itemID INT NOT NULL,
    FOREIGN KEY (playerID) REFERENCES Players(playerID) ON DELETE CASCADE,
    FOREIGN KEY (itemID) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (playerID, inventoryID, itemID)
);

CREATE TABLE Loadout (
    playerID INT NOT NULL,
    loadoutID INT UNIQUE NOT NULL,
    weapon1 INT,
    weapon2 INT,
    armor1 INT,
    armor2 INT,
    armor3 INT,
    dateUpdated DATETIME DEFAULT CURRENT_TIMESTAMP
                   ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (playerID) REFERENCES Players(playerID) ON DELETE CASCADE,
    FOREIGN KEY (weapon1) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (weapon2) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (armor1) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (armor2) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (armor3) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (playerID,loadoutID)
);

CREATE TABLE Performance (
    playerID INT NOT NULL,
    performanceID INT UNIQUE NOT NULL,
    totalKills INT,
    totalDeaths INT,
    DPS INT,
    dateCompleted DATETIME DEFAULT CURRENT_TIMESTAMP,
    loadoutID INT NOT NULL,
    missionID INT NOT NULL,
    FOREIGN KEY (playerID) REFERENCES Players(playerID) ON DELETE CASCADE,
    FOREIGN KEY (loadoutID) REFERENCES Loadout(loadoutID),
    FOREIGN KEY (missionID) REFERENCES Missions(missionID) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (playerID, performanceID)
);

CREATE TABLE LoadoutUse (
    playerID INT NOT NULL,
    missionID INT NOT NULL,
    loadoutUseID INT AUTO_INCREMENT PRIMARY KEY ,
    weapon1 INT,
    weapon2 INT,
    armor1 INT,
    armor2 INT,
    armor3 INT,
    dateUsed DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playerID) REFERENCES Players(playerID) ON DELETE CASCADE,
    FOREIGN KEY (missionID) REFERENCES Missions(missionID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (weapon1) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (weapon2) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (armor1) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (armor2) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (armor3) REFERENCES Items(itemID) ON UPDATE CASCADE ON DELETE CASCADE
);
