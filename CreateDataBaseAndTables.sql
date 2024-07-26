-- create_database.sql
CREATE DATABASE IF NOT EXISTS fitness_center_db;

USE fitness_center_db;

CREATE TABLE IF NOT EXISTS Members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL
);

CREATE TABLE IF NOT EXISTS WorkoutSessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    date VARCHAR(20) NOT NULL,
    duration_minutes INT NOT NULL,
    calories_burned INT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES Members(id)
);
