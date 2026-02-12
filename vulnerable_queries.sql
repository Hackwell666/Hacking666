-- Vulnerable SQL Query Patterns
-- These demonstrate common security flaws in SQL queries
-- DO NOT use these patterns in real applications

-- VULNERABLE PATTERN 1: Direct string concatenation in WHERE clause
-- Bad: SELECT * FROM users WHERE username = '$user_input'
SELECT * FROM users WHERE username = 'admin';
-- Injection: admin' OR '1'='1

-- VULNERABLE PATTERN 2: No input validation
-- Bad: SELECT * FROM users WHERE id = $id
SELECT * FROM users WHERE id = 1;
-- Injection: 1 OR 1=1

-- VULNERABLE PATTERN 3: Dynamic column names from user input
-- Bad: SELECT $column_name FROM users
SELECT username FROM users;
-- Injection: * FROM users WHERE role='admin'--

-- VULNERABLE PATTERN 4: ORDER BY with user input
-- Bad: SELECT * FROM users ORDER BY $sort_column
SELECT * FROM users ORDER BY username;
-- Injection: username; DROP TABLE users--

-- VULNERABLE PATTERN 5: LIKE clause with wildcards
-- Bad: SELECT * FROM users WHERE username LIKE '%$search%'
SELECT * FROM users WHERE username LIKE '%admin%';
-- Injection: %' OR '1'='1

-- VULNERABLE PATTERN 6: IN clause construction
-- Bad: SELECT * FROM users WHERE id IN ($ids)
SELECT * FROM users WHERE id IN (1,2,3);
-- Injection: 1) OR 1=1--

-- VULNERABLE PATTERN 7: Unescaped special characters
-- Bad: INSERT INTO users (username) VALUES ('$username')
INSERT INTO users (username, password, email) VALUES ('newuser', 'pass123', 'new@example.com');
-- Injection: admin'); DROP TABLE users--

-- VULNERABLE PATTERN 8: Dynamic table names
-- Bad: SELECT * FROM $table_name
SELECT * FROM users;
-- Injection: users; DROP TABLE sensitive_data--

-- VULNERABLE PATTERN 9: LIMIT with user input
-- Bad: SELECT * FROM users LIMIT $limit
SELECT * FROM users LIMIT 10;
-- Injection: 10; DELETE FROM users--

-- VULNERABLE PATTERN 10: Subquery injection
-- Bad: SELECT * FROM users WHERE role = (SELECT role FROM roles WHERE id = $id)
SELECT * FROM users WHERE role = (SELECT 'admin');
-- Injection: 1 UNION SELECT password FROM users WHERE username='admin'
