---
title: new-password-manager-incarnation
mainfont: Iosevka
---

I just had a rethink of my password manager app. I finally created a version where I can choose to name the password myself, as sometimes you can't be bothered to find a true source of randomness just to create an account. It's such a simple thing but, up until now, if I needed to add an account that I created the password, I had to change it directly on the database server.  
Also I added a lot more crypto power to the these proceedings than in previous times. And if I still think it's an overkill for my threat profile, it still feels good to have done a good job. Or, at least, a better job.  
And the funniest thing is that, most probably, I won't use this version.  For no other reason than it's new and I don't want to risk my passwords with a folder that I still don't trust fully.  
I think that what will happen in the end is ... eventually I'll add the new features to the old app. One by one. Slowly. Softly.  
I probably won't implement all the changes, just the more urgent ones. And then I'll forget that I ever coded this version.  
This, I think, is very unbecoming. I'm usually irreflexive and reckless. It's not my thing to be cautious and mistrusting. But when were talking about my password accesses, I get violently middle-aged.   
And this is what I done:  
1. I had as objective to build a version that, as I said, would ask the user if he wanted to name the password himself, to have password length dependent of input, and seriously beef up security.  In this regard, as I don't understand a lot about the subject, I think I went overboard, and have now a cartoonishly inadequate setup. Seriously, I would laugh if I was more sure about myself on this subject.  
I create a inaugural function that collects all information needed to manage the process. From username, service, to if he wants to name it himself, it's all here.  
```python
  @logger.catch
  def info():
      """All information but the password"""
  
      info.service = input("What is the service? ")
      info.username = input("What is the email/username? ")
      info.string = input("Choose a random, long, string ")
      info.length = int(input("How long do you want your password to be? "))
      info.creation = input("Do you want to write your own password? [y/n] ")
  
      if info.creation == "y":
          info.user_pwd = input("What password do you want? ")
      else:
          info.user_pwd = 0
  
  
  if __name__ == "__main__":
      info()
```
2. Here I did some hashing magic that I didn't understood fully, or at all, felt very covert and sub-rosa, and quickly abandoned it for other subjects. But to be true to the effort of documentation, what I thought was this. All passwords will be built from two main pieces, a random, long string that can be whatever you want. And the name of service/company that you are creating an account for. We then concatenate these two strings into a huge snake like new train of characters; and it's this monstrosity that is hashed with sha256 encryption. That I heard say is a good thing.  
```python
  @logger.catch  # Decorator for loguru. All errors will go log. Has to be on all functions
  def hash_string():
      """Where all the hashing operations are done"""
  
      string_bt = info.string.encode()
      service_bt = info.service.encode()
      concat = b"".join([string_bt, service_bt])
      h = hashlib.sha256()
      h.update(concat)
      hash_string.hex = h.hexdigest()
  
  
  if __name__ == "__main__":
      hash_string()
```
3. In this function, I mainly concentrated on imposing a lot of transformations to the strings that we started from. With special attention to the use of randomness python libraries.  
As the final password can be built in two different forms, by user, by random processes, I had to find a way for these paths to meet and use the same variable names, although the processes are completely different. For example; the name of the password variable that is imported to the database is defined in two different ways, if the user chose to name it itself, or chose to trust the mechanized route. If you choose the name, the value will be kept in a variable defined in the first function, and then, in the function that deals with inserting the values in the database. There's a loop in the final function, where it verifies if said variable has a value different than '0'. As that is the set value for the variable if the naming choice is done automatically. If it has, the user chose the name and the database insertion variable for the password becomes equal to the variable defined in the first function.  
If it's the other way around, the variable will be granted a formal value of '0', and the password definition will be done in the way we'll see right now.  
The final variable name for the password was named "complex.passwd". Complex from the function where it was created, plus a function attribute, that enables the variable to be transported between the modules freely. It has to be created in this particular module because, in the automatic version of naming, It's here that we reach the password value. So it needs the creation of two opposite instances of the password. If in a version the complex.passwd value is the final number arrived after: turning the hexadigest hash into a string, then into a list of individual characters, then appended with a random number of characters from a mixed alphabet composed of letters, numbers and symbols. As this creates an invariably enormous string, we collect one character in every four, to birth a more manageable string. Although at this time, we are still talking of lists. Finally we join all characters into one sole string, and name it, finally, complex.passwd.  
But this is what happens when the process is automatic, what of the other option? The complex.passwd variable must assume some value, so as not to complain that it doesn't exist. To remedy this, in the beginning of the 'complex' function, we define complex.passwd as a string space. This is enough to silence the linters, and can be changed later. So, all in all, this variable has three different definition moments, dependent on the optics of the user.  
```python
  @logger.catch
  def complex():
      complex.passwd = " "
      hex = str(hash_string.hex)
      hex_list = [char for char in hex]
      alpha = [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6",
          "7",
          "8",
          "9",
          "0",
          "A",
          "a",
          "B",
          "b",
          "C",
          "c",
          "D",
          "d",
          "E",
          "e",
          "F",
          "f",
          "G",
          "g",
          "H",
          "h",
          "I",
          "i",
          "J",
          "j",
          "K",
          "k",
          "L",
          "l",
          "M",
          "m",
          "N",
          "n",
          "O",
          "o",
          "P",
          "p",
          "Q",
          "q",
          "R",
          "r",
          "S",
          "s",
          "T",
          "t",
          "U",
          "u",
          "V",
          "v",
          "W",
          "w",
          "X",
          "x",
          "Y",
          "y",
          "Z",
          "z",
          "|",
          "!",
          '"',
          "#",
          "$",
          "%",
          "&",
          "/",
          "(",
          ")",
          "=",
          "«",
          "^",
          "<",
          ">",
          "[",
          "}",
          "+",
          "*",
          "ç",
          "`",
          "~",
          "_",
          "-",
          ".",
          ";",
          "|",
      ]
  
      add = random.sample(alpha, info.length)
      for i in add:
          hex_list.append(i)
      cull = hex_list[::4]
      pwd = ""
      complex.passwd = pwd.join(cull)
      print(complex.passwd)
  
  
  if __name__ == "__main__":
      complex()
```
4. Finally we reach the end of the voyage, where all that is left to do, is to insert the values into the database. I created a simple SQLite database, wholly appropriate for a project that probably will never go much farther than this. But it was fun to build, and I would do it again.  
```python
  @logger.catch
  def updt_database():
      """Updates the database"""
  
      try:
          conn = sqlite3.connect("new_pwd.db")
          cur = conn.cursor()
          if info.user_pwd != 0:
              complex.passwd = info.user_pwd
          answers = [info.service, info.username, info.string, complex.passwd]
          query = """INSERT INTO new_pwd (service, username, string, password) VALUES (?, ?, ?, ?)"""
          cur.execute(query, answers)
          conn.commit()
      except sqlite3.Error as e:
          print("Error while connecting to db", e)
      finally:
          if conn:
              conn.close()
  
  
  if __name__ == "__main__":
      updt_database()
```

As always the full power of the blessed code.
```python
  """A rethink of my password app. Added hashes to the mix"""
  import random
  from loguru import logger
  import hashlib
  import sqlite3
  
  fmt = "{time} - {name} - {level} - {message}"
  logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
  logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)
  
  
  @logger.catch
  def info():
      """All information but the password"""
  
      info.service = input("What is the service? ")
      info.username = input("What is the email/username? ")
      info.string = input("Choose a random, long, string ")
      info.length = int(input("How long do you want your password to be? "))
      info.creation = input("Do you want to write your own password? [y/n] ")
  
      if info.creation == "y":
          info.user_pwd = input("What password do you want? ")
      else:
          info.user_pwd = 0
  
  
  if __name__ == "__main__":
      info()
  
  
  @logger.catch  # Decorator for loguru. All errors will go log. Has to be on all functions
  def hash_string():
      """Where all the hashing operations are done"""
  
      string_bt = info.string.encode()
      service_bt = info.service.encode()
      concat = b"".join([string_bt, service_bt])
      h = hashlib.sha256()
      h.update(concat)
      hash_string.hex = h.hexdigest()
  
  
  if __name__ == "__main__":
      hash_string()
  
  
  @logger.catch
  def complex():
      complex.passwd = " "
      hex = str(hash_string.hex)
      hex_list = [char for char in hex]
      alpha = [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6",
          "7",
          "8",
          "9",
          "0",
          "A",
          "a",
          "B",
          "b",
          "C",
          "c",
          "D",
          "d",
          "E",
          "e",
          "F",
          "f",
          "G",
          "g",
          "H",
          "h",
          "I",
          "i",
          "J",
          "j",
          "K",
          "k",
          "L",
          "l",
          "M",
          "m",
          "N",
          "n",
          "O",
          "o",
          "P",
          "p",
          "Q",
          "q",
          "R",
          "r",
          "S",
          "s",
          "T",
          "t",
          "U",
          "u",
          "V",
          "v",
          "W",
          "w",
          "X",
          "x",
          "Y",
          "y",
          "Z",
          "z",
          "|",
          "!",
          '"',
          "#",
          "$",
          "%",
          "&",
          "/",
          "(",
          ")",
          "=",
          "«",
          "^",
          "<",
          ">",
          "[",
          "}",
          "+",
          "*",
          "ç",
          "`",
          "~",
          "_",
          "-",
          ".",
          ";",
          "|",
      ]
  
      add = random.sample(alpha, info.length)
      for i in add:
          hex_list.append(i)
      cull = hex_list[::4]
      pwd = ""
      complex.passwd = pwd.join(cull)
      print(complex.passwd)
  
  
  if __name__ == "__main__":
      complex()
  
  
  @logger.catch
  def updt_database():
      """Updates the database"""
  
      try:
          conn = sqlite3.connect("new_pwd.db")
          cur = conn.cursor()
          if info.user_pwd != 0:
              complex.passwd = info.user_pwd
          answers = [info.service, info.username, info.string, complex.passwd]
          query = """INSERT INTO new_pwd (service, username, string, password) VALUES (?, ?, ?, ?)"""
          cur.execute(query, answers)
          conn.commit()
      except sqlite3.Error as e:
          print("Error while connecting to db", e)
      finally:
          if conn:
              conn.close()
  
  
  if __name__ == "__main__":
      updt_database()
```
