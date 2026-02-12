-- Secure SQL Query Patterns
-- These demonstrate best practices for preventing SQL injection
-- Use these patterns in production code

-- SECURE PATTERN 1: Prepared Statements with Parameterized Queries
-- Good: Using placeholders instead of direct concatenation
-- Example in code: cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
-- The actual query with parameters:
PREPARE stmt1 FROM 'SELECT * FROM users WHERE username = ?';
SET @username = 'admin';
EXECUTE stmt1 USING @username;
DEALLOCATE PREPARE stmt1;

-- SECURE PATTERN 2: Input Validation and Whitelisting
-- Only allow specific, validated values
-- Example: Only allow specific column names for ORDER BY
PREPARE stmt2 FROM 'SELECT * FROM users ORDER BY username';
EXECUTE stmt2;
DEALLOCATE PREPARE stmt2;

-- SECURE PATTERN 3: Stored Procedures
-- Encapsulate logic in stored procedures
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS GetUserByUsername(IN p_username VARCHAR(50))
BEGIN
    SELECT id, username, email, role FROM users WHERE username = p_username;
END //
DELIMITER ;

-- Call the stored procedure
CALL GetUserByUsername('admin');

-- SECURE PATTERN 4: Using parameterized INSERT
PREPARE stmt3 FROM 'INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)';
SET @username = 'secure_user';
SET @password = 'hashed_password';
SET @email = 'secure@example.com';
SET @role = 'user';
EXECUTE stmt3 USING @username, @password, @email, @role;
DEALLOCATE PREPARE stmt3;

-- SECURE PATTERN 5: Using parameterized UPDATE
PREPARE stmt4 FROM 'UPDATE users SET email = ? WHERE id = ?';
SET @email = 'updated@example.com';
SET @user_id = 1;
EXECUTE stmt4 USING @email, @user_id;
DEALLOCATE PREPARE stmt4;

-- SECURE PATTERN 6: Least Privilege Principle
-- Create users with minimal necessary permissions
CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON security_test.users TO 'app_user'@'localhost';
-- Do NOT grant DROP, CREATE, or other dangerous privileges

-- SECURE PATTERN 7: Input Sanitization Example
-- Whitelist approach for table names
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS GetDataFromTable(IN p_table_name VARCHAR(50))
BEGIN
    IF p_table_name = 'users' THEN
        SELECT * FROM users;
    ELSEIF p_table_name = 'login_attempts' THEN
        SELECT * FROM login_attempts;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid table name';
    END IF;
END //
DELIMITER ;

-- SECURE PATTERN 8: Password Hashing (structure example)
-- Always hash passwords, never store plain text
-- Example using SHA256 (use bcrypt or argon2 in production)
PREPARE stmt5 FROM 'INSERT INTO users (username, password, email) VALUES (?, SHA2(?, 256), ?)';
SET @username = 'hashed_user';
SET @password = 'plain_password';
SET @email = 'hashed@example.com';
EXECUTE stmt5 USING @username, @password, @email;
DEALLOCATE PREPARE stmt5;

-- SECURE PATTERN 9: Row-Level Security
-- Create a view that filters based on user context
CREATE VIEW my_data AS
SELECT * FROM sensitive_data WHERE user_id = CURRENT_USER();

-- SECURE PATTERN 10: Auditing and Logging
-- Create trigger to log all login attempts
DELIMITER //
CREATE TRIGGER IF NOT EXISTS log_login_attempt
AFTER INSERT ON login_attempts
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, table_name, record_id, timestamp)
    VALUES ('LOGIN_ATTEMPT', 'login_attempts', NEW.id, NOW());
END //
DELIMITER ;

-- Create audit log table if needed
CREATE TABLE IF NOT EXISTS audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(50),
    table_name VARCHAR(50),
    record_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
