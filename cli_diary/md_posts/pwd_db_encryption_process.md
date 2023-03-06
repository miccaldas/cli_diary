# Password Database Encryption Process
26-02-2023
<br>
<br>
## UPDATE  
It is now 05/03/23, and since my last update (26/02/23), and everything  
changed. I was very unhappy with the limitations of using MySQL's own  
encryption mechanisms. In my opinion it had the following foibles:  
    1. The encryption key has to be activated at the start of every session.  
       User variables are only valid during a session. Because of this, I  
       started thinking on how to go around this limitation, like initiating  
       it when MySQL service was started; but:  
    2. I couldn't get the key activated at boot.    
       There's not even an option that remotely does something akin to this.  
       You can create triggers or tasks for a myriad of events, provided that  
       the session has has started. I then thought that I could create a Python   
       or Bash script that programmatically would send the activation command  
       at the beginning of all db calls. But:  
    3. The key activation command doesn't work though python-mysql-connector.  
       I don't know if this is a flaw or intentional, either way, you can't do  
       it through Python. Also:  
    4. The Python connector alters the passwords, making them impossible to  
       decode. Python's connector returns every bytes() stored in the database,  
       as a bytesarray. Since what was uploaded was a bytes string, it's easy  
       to understand the decryptor's confusion. Furthermore:  
    5. You can't export the key from MySQL. It resides only inside it and even  
       then, just for the length of a session. This illustrates nicely a  
       concern of mine, of a more philosophical   nature, but no less worrying;  
       that:  
    6. Most of the process was totally out of my hands. MySQL will manage the  
       entirety of the process, dictate the terms and conditions, and I could  
       just take it or leave it.  
  
Then I remembered that I had Sqlite3 installed. I remembered also that Python  
is much more integrated with it than with MySQL. In fact, it doesn't need a  
connector, it uses a native package. This could solve, at least, the problem of  
fucking my encrypted passwords values. I also decided that encryption  
process would be my own. I would get a library to encode and  decode data, I  
would set it up programmatically through Python's modules, and take full  
ownership of the project.  
  
I came up with the following structure:
  
### DATA ENCRYPTION/DECRYPTION.
This is done through [Themis](https://docs.cossacklabs.com/themis/), that is a simple to use, secure and sturdy  
encryption library. To see how it's implemented, see the template in the  
[encrypt_decrypt](./encrypt_decrypt.txt) file.    
  
### SENSITIVE DATA STORAGE.  
It wouldn't make much sense going to all this trouble and leaving the passwords  
and keys files unguarded.  
So we:  
    1. Create a new folder to house sensitive information. The folder and all  
       its contents, have a permissions profile of 700. This was as restrictive  
       as I could get, before making it impossible for the files to be accessed  
       through Python. There is no version control for these folders and files,  
       their backup is done to an external disk.  
    2. Store each database with encrypted information on its own subfolder, with  
       their own set of credentials.  
    3. The files location is obfuscated in Python files, through the use of  
       environment variables for their paths.  
       These are defined in project by project, and stored in a '.env' file  
       that's not monitored by Git.  
    4. The main folder is encrypted with [Encfs](https://github.com/vgough/encfs), a virtual filesystem for  
       encryption.  
       It works by requiring two folders, one with the decrypted documentation,  
       and another, completely, empty, that'll manage the hosting of encrypted  
       files:  
       1. If you already have a folder with sensitive information and want to  
          use its name as mount point, empty it of all files, then create a  
          empty folder in the same directory that'll host the encrypted files.  
       2. Create the mount point, using Encfs command 'mount'.  
       3. Put the files you took from the unencrypted folder back inside.  
       4. If you look now inside the encrypted folder, there'll be encrypted  
          versions of all documents in the unencrypted one.  
       5. After accessing the files through the unencrypted folder, unmount it.  
       6. You'll now see that the unencrypted folder is empty, but the  
          encrypted one still has coded versions.  
   5. If you want more details of Encfs' implementation, take a look at the  
      [config](./config.py) file. Specifically the 'Efs' class.  

### ENCRYPTION WORKFLOW.
1. The user, on his Python scripts, will access the Encfs password, through  
   environment variables, and check if the mount point is active:  
       1. Is active. Access the files.  
       2. It's not active. Give the 'mount' command and recheck if it's open.  
2. With access to the folder, get the Themis key correspondent to your  
   database.  
3. Use it to encrypt/decrypt data, as the case may be.  
4. After doing whatever you wanted to do, unmount it.  
   You can see an example, like many others, of this workflow in practice in  
   [update](/home/mic/python/pwd_encrypted/pwd_encrypted/update.py).

This is the current state of the art. Doesn't mean that it won't change in a  
day or two. But, for now, this is where we stand.  
I'll leave the old updates below this one, for documentation purposes. 

---------------------

## UPDATE
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
  

