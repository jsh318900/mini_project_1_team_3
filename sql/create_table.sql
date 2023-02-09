CREATE DATABASE IF NOT EXISTS MELON;
USE MELON;

-- COMPANY: 소속사
CREATE TABLE IF NOT EXISTS COMPANY (
	ID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(100) NOT NULL
);

-- ALBUM: 앨범
CREATE TABLE IF NOT EXISTS ALBUM (
	ID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(100) NOT NULL,
    RELEASE_DATE DATE NOT NULL,
    NUM_LIKE INT UNSIGNED NULL,
    RATING FLOAT NULL,
    NUM_RATING INT NULL,
    NUM_COMMENT INT NULL
);

-- SONG: 곡
CREATE TABLE IF NOT EXISTS SONG (
	ID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(100) NOT NULL,
    ALBUM_ID INT UNSIGNED NOT NULL,
    GENRE VARCHAR(20) NULL,
    NUM_LIKE INT NULL,
    NUM_COMMENT INT NULL,
    IS_TITLE BOOL NULL,-- TINYINT(1) 
    FOREIGN KEY (ALBUM_ID) REFERENCES ALBUM(ID)
);

-- SINGER: 가수
CREATE TABLE IF NOT EXISTS SINGER(
	ID INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    COMPANY_ID INT UNSIGNED NOT NULL,
    NAME VARCHAR(20) NOT NULL,
    DEBUT_DATE DATE NOT NULL,
    DEBUT_SONG_ID INT UNSIGNED NOT NULL,
    NUM_FAN INT NULL,
    FOREIGN KEY (COMPANY_ID) REFERENCES COMPANY(ID),
    FOREIGN KEY (DEBUT_SONG_ID) REFERENCES SONG(ID)
);

-- SONG_SINGER: 노래를 부른 가수
CREATE TABLE IF NOT EXISTS SONG_SINGER(
	SONG_ID INT UNSIGNED NOT NULL,
    SINGER_ID INT UNSIGNED NOT NULL,
    FOREIGN KEY (SONG_ID) REFERENCES SONG(ID),
    FOREIGN KEY (SINGER_ID) REFERENCES SINGER(ID),
    PRIMARY KEY (SONG_ID, SINGER_ID)
);

-- ALBUM_SINGER: 앨범을 낸 가수
CREATE TABLE IF NOT EXISTS ALBUM_SINGER(
	ALBUM_ID INT UNSIGNED NOT NULL,
    SINGER_ID INT UNSIGNED NOT NULL,
    FOREIGN KEY (ALBUM_ID) REFERENCES ALBUM(ID),
    FOREIGN KEY (SINGER_ID) REFERENCES SINGER(ID),
    PRIMARY KEY (ALBUM_ID, SINGER_ID)
);

-- ALBUM_SONG: 앨범에 수록된 노래
CREATE TABLE IF NOT EXISTS ALBUM_SONG(
	ALBUM_ID INT UNSIGNED NOT NULL,
    SONG_ID INT UNSIGNED NOT NULL,
    FOREIGN KEY (ALBUM_ID) REFERENCES ALBUM(ID),
    FOREIGN KEY (SONG_ID) REFERENCES SONG(ID),
    PRIMARY KEY (ALBUM_ID, SONG_ID)
);

-- YEAR_CHART: 연도별 차트
CREATE TABLE IF NOT EXISTS YEAR_CHART(
	YEAR DATE NOT NULL,
    RANKS INT UNSIGNED NOT NULL,
    SONG_ID INT UNSIGNED NOT NULL,
    FOREIGN KEY (SONG_ID) REFERENCES SONG(ID),
    PRIMARY KEY (YEAR, RANKS)
);

-- TEN_YEARS_CHART: 연대별 차트
CREATE TABLE IF NOT EXISTS TEN_YEARS_CHART(
	START_YEAR DATE NOT NULL,
    RANKS INT UNSIGNED NOT NULL,
    SONG_ID INT UNSIGNED NOT NULL,
    FOREIGN KEY (SONG_ID) REFERENCES SONG(ID),
    PRIMARY KEY (START_YEAR, RANKS)
);