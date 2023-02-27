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
