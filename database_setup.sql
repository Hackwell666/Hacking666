-- Database setup for security testing
-- This file creates a sample database structure for testing SQL injection and other database attacks

-- Create database
CREATE DATABASE IF NOT EXISTS security_test;
USE security_test;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create login_attempts table for tracking
CREATE TABLE IF NOT EXISTS login_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    ip_address VARCHAR(45),
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT FALSE
);

-- Create sensitive_data table
CREATE TABLE IF NOT EXISTS sensitive_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    credit_card VARCHAR(16),
    ssn VARCHAR(11),
    account_number VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert sample data for testing
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@example.com', 'admin'),
('john_doe', 'password123', 'john@example.com', 'user'),
('jane_smith', 'pass456', 'jane@example.com', 'user'),
('test_user', 'test123', 'test@example.com', 'user');

-- Insert sample sensitive data
INSERT INTO sensitive_data (user_id, credit_card, ssn, account_number) VALUES
(1, '1234567890123456', '123-45-6789', 'ACC001'),
(2, '9876543210987654', '987-65-4321', 'ACC002'),
(3, '5555444433332222', '555-44-3333', 'ACC003');

-- Create a view for user information
CREATE VIEW user_info AS
SELECT u.id, u.username, u.email, u.role, u.created_at
FROM users u;
