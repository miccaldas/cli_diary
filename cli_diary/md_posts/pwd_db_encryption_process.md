---
title: Password Database Encryption Process
date: 26/02/2023
mainfont: Iosevka
---

I'm revisiting again the idea of encrypting the 'password' database. Not all of 
it, mind you, just the specific password value.  Although it's not close to be 
being finished, I just wanted to jot down some information, so I don't forget.  
I'm using MySQL's own AES encryption process, and it works like this:  first you 
create a BLOB or VARBINARY column, to house the encrypted passwords, as they'll 
be bytes objects. I created a VARBINARY(8000) column that I called 'pwd'.  
The encryption and decryption operations are only accessible through a key.  
I created one with the command:  
```sql
set @key_str = SHA2('Zrd&iLnyC31._)K"çlk*I9h~', 512);
```
The key is called 'key_str' and is invoked with '@' before it. '@kill_str'.  
It's a SHA2 algorithm key, with a length of 512, and the string I generated on  
the 'password' app.  
I cloned the 'passwd' column, that has the original values in plain text, with 
this very simple command:  
```sql
UPDATE pwd SET pwd = AES_ENCRYPT(pwd, @key_str)
```
If you wanted to just encrypt a specific entry, you could do, for example:  
```sql
UPDATE pwd SET pwd = AES_ENCRYPT(pwd, @key_str) WHERE pwdid = 658
```
Now, if you want to decrypt all of columns values, you do:  
```sql 
SELECT *, CAST(AES_DECRYPT(pwd, @key_str) AS CHAR(80)) FROM pwd;
```
If you only need one value, you could do:
```sql
SELECT *, CAST(AES_DECRYPT(pwd, @key_str) AS CHAR(80)) FROM pwd WHERE pwdid = 658;
```
  
## UPDATE.
Apparently the key variable that I made yesterday, today,wasn't working when I started MySQL.   
A little digging revealed that variables started by '@' ', as @key_str mos certainly is,  
are user variables and exist only in the context of a session. To remedy this, and result of   
not finding a way to make the create key command a system variable, I just went along with the   
next best thing and invoked the key before making a db call through Python. That way it's  
always on when I need it. You can, and need to if you want to decrypt stuff you did before,   
use the same starting string. That's what defines the key and that's the information that   
needs to be kept secret. So as to not write the key initiation string on all my scripts, I  
made a environment variable called 'AES_MYSQL_KEY', that keeps it. In order to use a   
environment variable in Python, you have to do this:
```python
import os
aeskey = os.environ["AES_MYSQL_KEY"]
```
The MySQL query should always use prepared statements, otherwise MySQL flips with all the characters  
and doesn't accept the string. The query format I'm currently using is this:
```sql
query = "SET @key_str = SHA2(%s, 512)"
```
Then the encryption query for the 'pwd' database is this:
```sql
query5 = "UPDATE pwd SET pwd = AES_ENCRYPT(%s, @key_str) WHERE pwdid = %s"
```
If you only want to make an encryption/decryption but don't want to put it anywhere, you can do:
```sql
SELECT AES_ENCRYPT('text_to_encrypt', @str_key)
```
