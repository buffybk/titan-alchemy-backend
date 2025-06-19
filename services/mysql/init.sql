-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS titan_alchemy;
USE titan_alchemy;

-- Create a dedicated user for the application
CREATE USER IF NOT EXISTS 'titan_user'@'%' IDENTIFIED BY 'titan_password';
GRANT ALL PRIVILEGES ON titan_alchemy.* TO 'titan_user'@'%';
FLUSH PRIVILEGES;

-- Enable performance schema for monitoring
UPDATE performance_schema.setup_consumers SET ENABLED = 'YES' WHERE NAME LIKE '%events_statements%';
UPDATE performance_schema.setup_instruments SET ENABLED = 'YES', TIMED = 'YES' WHERE NAME LIKE '%statement/%'; 