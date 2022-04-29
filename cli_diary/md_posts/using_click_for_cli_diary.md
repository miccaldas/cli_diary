---
title: "Using Click for cli_diary"
mainfont: Iosevka
---

Another experiment done with 'cli_diary' was, to use the Click tool to build a
command line app. A more traditional one.  
As I can't be bothered to remember commands, I usually create apps with
dropdowns with all the available commands. If this comfortable enough, it
creates an added step, that makes its use slower.  
For this, and also to learn something new, I tried to build cli_diary in this
format. And if in the end, I didn't use it, important lessons were learned and I
would like to keep a record of them.  
Click uses a lot of decorators to interact with the code. In this particular
case we had:
```python
 @click.command()
```
That defines the function as command line command.  

After it are defined the options, arguments or sub-commands. Again, in this
case:
```python
 @click.option("-t", "--title", default=datetime.today().strftime("%d-%m-%Y"))
```
defines a command line option that has a short version `-t` and a long one
`--title`. This one serves to input the title of the post. If nothing is
entered a default value is used. In this case the present date.  

Some more option commands. Now without default values:
```python
 @click.option("--k1")
 @click.option("--k2")
```

These commands should be repeated as function arguments, like so:
```python
 def new(title, k1, k2):
```

Here is the full code for context:
```python
 #!/usr/bin/python3
 """
 We use here for the first time the Click cli system.
 In order to try something new, It was put here all
 management functions that do not need to visualize
 the database content. That will be treated in another
 module, hopefully, in a new manner.
 """
 from datetime import datetime

 import click
 import isort
 import snoop
 from loguru import logger
 from mysql.connector import Error, connect
 from snoop import pp

 fmt = "{time} - {name} - {level} - {message}"
 logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
 logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501


 def type_watch(source, value):
     return "type({})".format(source), type(value)


 snoop.install(watch_extras=[type_watch])


 @logger.catch
 @click.command()
 @click.option("-t", "--title", default=datetime.today().strftime("%d-%m-%Y"))
 @click.option("--k1")
 @click.option("--k2")
 @snoop
 def new(title, k1, k2):
     """
     Collects the options values, adds the
     entry value and send them to the db.
     """
     entry = click.edit().rstrip()

     try:
         conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
         cur = conn.cursor()
         query = "INSERT INTO cli_diary (title, entry, k1, k2) VALUES (%s, %s, %s, %s)"
         answers = [title, entry, k1, k2]
         cur.execute(query, answers)
         conn.commit()
     except Error as e:
         print("Error while connecting to db", e)
     finally:
         if conn:
             conn.close()


 if __name__ == "__main__":
    new()


 @logger.catch
 @click.command()
 @click.option("--id")
 @snoop
 def delete(id):
    """
    Deletes entries from the db.
    """
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "DELETE FROM cli_diary WHERE id = %s"
        answers = [id]
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


 if __name__ == "__main__":
    delete()


 @logger.catch
 @click.command()
 @click.option("--id")
 @snoop
 def update(id):
    """
    Updates values in the db.
    The reason why 'column' is
    an input field and not a
    command line option is that
    strings in options get quotes
    around them, and MySQL doesn't
    like that.
    """

    column = input(click.style("What column do you want to update? ", fg="bright_white", bold=True))
    updt = click.edit().rstrip()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        answer = [column, updt, id]
        query = "UPDATE cli_diary SET %s = %s WHERE id = %s"
        cur.execute(query, answer)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


 if __name__ == "__main__":
    update()
```

But what is more interesting is using setuptools as a way to integrate the
commands.  
In this case we created a setup.py file in the folder above the app code,
with the following information:

```python
 from setuptools import find_packages, setup

 setup(
    name="cli_diary",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "newdiary = cli_diary.manage:new",
            "deldiary = cli_diary.manage:delete",
            "updtdiary = cli_diary.manage:update",
            "seediary = cli_diary.visualization:see",
        ],
    },
 )
```
What is important to retain here is the 'entry_points' entry. In it we define
commands that will be able to use anywhere in the computer, writing just the
command name.  
Inside 'console_scripts' we define them this way:  
1. First the name of the command. To use the first one as an example, the name
   is 'newdiary'. This is how we'll invoke the command.  
2. Then we define what is the package name. In this case, 'cli_diary'.  
3. After we write the module name. As this came from 'manage.py', the name is
   'manage'.  
4. Finally we write the name of the function. In this case 'new'.  
In the same place, we give order to pip to install the package:
```python
 pip install --editable
```
After that I should be able to use the command directly. For example:
```bash
 newdiary -t 'This is the Title' --k1 tag1 --k2 tag2
```


