-- =====================================================================
--  Projekt "Benni befreien" – Datenbank Dashboard-Team
--  Import: mysql -u root -p < benni_db.sql   (oder phpMyAdmin > Importieren)
--  Kompatibel: MySQL 8.x / MariaDB 10.x
-- =====================================================================

DROP DATABASE IF EXISTS benni_db;
CREATE DATABASE benni_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE benni_db;

-- ---------------------------------------------------------------------
--  Tabelle: user
--  Ein Spieler bzw. eine Spielgruppe mit Zugangscode und Schwierigkeit
-- ---------------------------------------------------------------------
CREATE TABLE `user` (
  user_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_name   VARCHAR(100) NOT NULL,
  user_code   INT NOT NULL,
  difficulty  ENUM('leicht', 'mittel', 'schwer') NOT NULL DEFAULT 'mittel',
  PRIMARY KEY (user_id),
  UNIQUE KEY uq_user_code (user_code)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
--  Tabelle: station
--  Die 5 Stationen des Spiels
-- ---------------------------------------------------------------------
CREATE TABLE station (
  station_id  TINYINT UNSIGNED NOT NULL,
  name        VARCHAR(100)     NOT NULL,
  PRIMARY KEY (station_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
--  Zwischentabelle: user_station  (Beziehung "enthält", n:m)
--  Speichert pro User und Station die Start- und Endzeit
-- ---------------------------------------------------------------------
CREATE TABLE user_station (
  user_id     INT UNSIGNED     NOT NULL,
  station_id  TINYINT UNSIGNED NOT NULL,
  time_start  DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  time_end    DATETIME         NULL,          -- NULL = Station noch nicht gelöst
  PRIMARY KEY (user_id, station_id),
  KEY idx_station (station_id),
  CONSTRAINT fk_us_user    FOREIGN KEY (user_id)    REFERENCES `user` (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_us_station FOREIGN KEY (station_id) REFERENCES station (station_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT chk_zeit CHECK (time_end IS NULL OR time_end >= time_start)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
--  View: Spielzeit pro User (z. B. für Highscore im Dashboard)
-- ---------------------------------------------------------------------
CREATE VIEW v_spielzeit AS
SELECT
  u.user_id,
  u.user_code,
  u.difficulty,
  COUNT(us.time_end)                               AS stationen_geloest,
  MIN(us.time_start)                               AS spielstart,
  MAX(us.time_end)                                 AS letzte_loesung,
  TIMEDIFF(MAX(us.time_end), MIN(us.time_start))   AS gesamtzeit
FROM `user` u
LEFT JOIN user_station us ON us.user_id = u.user_id
GROUP BY u.user_id, u.user_code, u.difficulty;

-- =====================================================================
--  Stammdaten: Stationen
-- =====================================================================
INSERT INTO station (station_id, name) VALUES
  (1, 'Standort von Benni herausfinden'),
  (2, 'In das Gebäude gelangen'),
  (3, 'Orientierung und Einhacken ins System'),
  (4, 'Benni im Gebäude lokalisieren'),
  (5, 'Benni befreien und entkommen');
