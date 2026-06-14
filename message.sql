CREATE DATABASE IF NOT EXISTS devops;
USE devops;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO messages (message) VALUES ('Welcome to DevOps Two-Tier App!');
INSERT INTO messages (message) VALUES ('This message was created during deployment!');
