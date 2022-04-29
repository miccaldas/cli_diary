---
title: bookmark_prompt_toolkit
mainfont: Iosevka
---

I was making some updates on the bookmarks app, Urwid version, when it came to me that a change of UI provider was in order.  
All the examples in Urwid work under the premise that every time you make a choice in a menu or prompt, there's always another step that reiterates that you have, indeed, made that choice, and your choice value is kept not as the choice, but as the equal confirmation value. I think this will be clearer with an example:

In the 'Simple Menu' example of the [Urwid tutorial](http://urwid.org/tutorial/index.html), you select an option from choices ``choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()``, and instead of using the direct value ``choice``, it's created a button that, when printed the ``choice`` value, clicks OK, and ends the choice process. In short instead of having a choice and a ``enter`` key-press, we have that plus clicking on a button that the only thing it does is confirm what you have just done.  

If you're doing an UI that has few interactions with the user, this is not very taxing. But if you need to concatenate one or more commands in sequence, these confirmations start to feel as stumbling blocks.  
I did some research and all the examples I saw followed this blueprint. So much so that I now am convinced that this is a feature of how Urwid functions.  
Obviously I might be wrong and there is indeed a way to circumvent the confirmations, but I wasn't able to figure it out.  
Add to this the fact that you can only make one request by function, and I started to think that, even if prompt_toolkit is hard to grasp, it couldn't be as hard as this. And I was right.  
Prompt_toolkit has some ready to use dialog boxes that if not very flexible, are extremely simple and quick to implement.  

This build had two very nice bonuses, that solved two problems that I was trying to resolve for some time:
1. How to create a class where all information is added by user input,
2. How to instantiate a class without instantiation values.

I see now that the solutions were obvious and not very difficult to reach. But difficult, for me, it was. And I'm happy I solved it.  

In this case all information needed to run the methods is specific to one method only. There aren't any variables that are needed by more than one method. This enabled me to not use a \_\_init\_\_ method and thus avoided having to inject values when instantiating the class. So I was free to insert on the methods the input queries for each functionality.  

1. I created an add a bookmark method:
```python
    def add_bkmk(self):
        title = input_dialog(title="Title", text="What is the title? ").run()
        comment = input_dialog(title="Comment", text="What is your comment? ").run()
        link = input_dialog(title="Link", text="What is the link? ").run()
        k1 = input_dialog(title="K1", text="Choose a keyword ").run()
        k2 = input_dialog(title="K2", text="Choose another... ").run()
        k3 = input_dialog(title="K3", text="And another...").run()

        answers = [title, comment, link, k1, k2, k3]
        logger.info(answers)

        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = """INSERT INTO bkmks (title, comment, link, k1, k2, k3) VALUES (%s, %s, %s, %s, %s, %s)"""
            logger.info(query)
            cur.execute(query, answers)
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
```
2. A delete a bookmark method:
```python
    def delete(self):
        """We must use 'ident', not 'id' in choosing the variable name, as the latter is a reserved word"""
        ident = input_dialog(title="Delete Entry", text="What is the ID? ").run()
        logger.info(ident)

        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = " DELETE FROM bkmks WHERE id = " + ident
            logger.info(query)
            cur.execute(query)
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
```
3. A see all bookmarks method:
```python
    def see(self):
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = """ SELECT * FROM bkmks """
            logger.info(query)
            cur.execute(query)
            records = cur.fetchall()
            for row in records:
                print(color(" [*] ID » ", fore="#928b7f"), color(str(row[0]), fore="#ffffff"))  # 1
                print(color(" [*] TITLE » ", fore="#928b7f"), color(str(row[1]), fore="#ffffff"))
                print(color(" [*] COMMENT » ", fore="#928b7f"), color(str(row[2]), fore="#ffffff"))
                print(color(" [*] LINK ? ", fore="#928b7f"), color(str(row[3]), fore="#a2cff0"))
                print(color(" [*] KEYWORD 1 » ", fore="#928b7f"), color(str(row[4]), fore="#ffffff"))
                print(color(" [*] KEYWORD 2 » ", fore="#928b7f"), color(str(row[5]), fore="#ffffff"))
                print(color(" [*] KEYWORD 3 » ", fore="#928b7f"), color(str(row[6]), fore="#ffffff"))
                print(color(" [*] TIME » ", fore="#928b7f"), color(str(row[7]), fore="#ffffff"))
                print("\n")
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
```
4. A search the bookmarks method:
```python
    def search(self):
        try:
            busca = input_dialog(title="Search Bookmarks", text="What are you searching for? ").run()
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = (
                " SELECT * FROM bkmks WHERE MATCH(title, comment, link, k1, k2, k3) AGAINST ('"
                + busca
                + "' IN NATURAL LANGUAGE MODE)"
            )
            logger.info(query)
            cur.execute(query)
            records = cur.fetchall()
            for row in records:
                print(color(" [*] ID » ", fore="#928b7f"), color(str(row[0]), fore="#ffffff"))
                print(color(" [*] TITLE » ", fore="#928b7f"), color(str(row[1]), fore="#ffffff"))
                print(color(" [*] COMMENT » ", fore="#928b7f"), color(str(row[2]), fore="#ffffff"))
                print(color(" [*] LINK ? ", fore="#928b7f"), color(str(row[3]), fore="#ffffff"))
                print(color(" [*] KEYWORD 1 » ", fore="#928b7f"), color(str(row[4]), fore="#ffffff"))
                print(color(" [*] KEYWORD 2 » ", fore="#928b7f"), color(str(row[5]), fore="#ffffff"))
                print(color(" [*] KEYWORD 3 » ", fore="#928b7f"), color(str(row[6]), fore="#ffffff"))
                print(color(" [*] TIME » ", fore="#928b7f"), color(str(row[7]), fore="#ffffff"))
                print("\n")
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
```
5. And an update a bookmark method:
```python
    def update(self):
        coluna = input_dialog(title="Update Column", text="Column? ").run()
        ident = input_dialog(title="Entry ID", text="ID? ").run()
        update = input_dialog(title="Update Text", text="Write your update.").run()

        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = "UPDATE bkmks SET " + coluna + " = '" + update + "' WHERE id = " + ident
            logger.info(query)
            cur.execute(
                query,
            )
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
```

This is the whole class:
```python
from loguru import logger
from prompt_toolkit.shortcuts import input_dialog
from mysql.connector import connect, Error
from colr import color

################################################################################
# @author      : mclds
# @file        : add
# @created     : 21/08/2021
# @email       : mclds@protonmail.com
# @description : Bookmark manager app. Adds, deletes, updates, searches, sees
# the bookmark database. The UI is done in Prompt_Toolkit
################################################################################

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


class Add:
    """This file is organized as a class just because the functions can be organized under the app umbrella. But in reality
    there's no __init__ variables as there are no variables that are needed by more than one method. As user input is the
    base of all methods, we are working without __init__ method, that would force us to have pre-determined values to
    instantiate the class. This way we can instantiate the class, empty of attributes."""

    @logger.catch
    def add_bkmk(self):
        title = input_dialog(title="Title", text="What is the title? ").run()
        comment = input_dialog(title="Comment", text="What is your comment? ").run()
        link = input_dialog(title="Link", text="What is the link? ").run()
        k1 = input_dialog(title="K1", text="Choose a keyword ").run()
        k2 = input_dialog(title="K2", text="Choose another... ").run()
        k3 = input_dialog(title="K3", text="And another...").run()

        answers = [title, comment, link, k1, k2, k3]
        logger.info(answers)

        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = """INSERT INTO bkmks (title, comment, link, k1, k2, k3) VALUES (%s, %s, %s, %s, %s, %s)"""
            logger.info(query)
            cur.execute(query, answers)
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    @logger.catch
    def delete(self):
        """We must use 'ident', not 'id' in choosing the variable name, as the latter is a reserved word"""
        ident = input_dialog(title="Delete Entry", text="What is the ID? ").run()
        logger.info(ident)

        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = " DELETE FROM bkmks WHERE id = " + ident
            logger.info(query)
            cur.execute(query)
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    @logger.catch
    def see(self):
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = """ SELECT * FROM bkmks """
            logger.info(query)
            cur.execute(query)
            records = cur.fetchall()
            for row in records:
                print(color(" [*] ID » ", fore="#928b7f"), color(str(row[0]), fore="#ffffff"))  # 1
                print(color(" [*] TITLE » ", fore="#928b7f"), color(str(row[1]), fore="#ffffff"))
                print(color(" [*] COMMENT » ", fore="#928b7f"), color(str(row[2]), fore="#ffffff"))
                print(color(" [*] LINK ? ", fore="#928b7f"), color(str(row[3]), fore="#a2cff0"))
                print(color(" [*] KEYWORD 1 » ", fore="#928b7f"), color(str(row[4]), fore="#ffffff"))
                print(color(" [*] KEYWORD 2 » ", fore="#928b7f"), color(str(row[5]), fore="#ffffff"))
                print(color(" [*] KEYWORD 3 » ", fore="#928b7f"), color(str(row[6]), fore="#ffffff"))
                print(color(" [*] TIME » ", fore="#928b7f"), color(str(row[7]), fore="#ffffff"))
                print("\n")
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    @logger.catch
    def search(self):
        try:
            busca = input_dialog(title="Search Bookmarks", text="What are you searching for? ").run()
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = (
                " SELECT * FROM bkmks WHERE MATCH(title, comment, link, k1, k2, k3) AGAINST ('"
                + busca
                + "' IN NATURAL LANGUAGE MODE)"
            )
            logger.info(query)
            cur.execute(query)
            records = cur.fetchall()
            for row in records:
                print(color(" [*] ID » ", fore="#928b7f"), color(str(row[0]), fore="#ffffff"))
                print(color(" [*] TITLE » ", fore="#928b7f"), color(str(row[1]), fore="#ffffff"))
                print(color(" [*] COMMENT » ", fore="#928b7f"), color(str(row[2]), fore="#ffffff"))
                print(color(" [*] LINK ? ", fore="#928b7f"), color(str(row[3]), fore="#ffffff"))
                print(color(" [*] KEYWORD 1 » ", fore="#928b7f"), color(str(row[4]), fore="#ffffff"))
                print(color(" [*] KEYWORD 2 » ", fore="#928b7f"), color(str(row[5]), fore="#ffffff"))
                print(color(" [*] KEYWORD 3 » ", fore="#928b7f"), color(str(row[6]), fore="#ffffff"))
                print(color(" [*] TIME » ", fore="#928b7f"), color(str(row[7]), fore="#ffffff"))
                print("\n")
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    @logger.catch
    def update(self):
        coluna = input_dialog(title="Update Column", text="Column? ").run()
        ident = input_dialog(title="Entry ID", text="ID? ").run()
        update = input_dialog(title="Update Text", text="Write your update.").run()

        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = "UPDATE bkmks SET " + coluna + " = '" + update + "' WHERE id = " + ident
            logger.info(query)
            cur.execute(
                query,
            )
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
```
----------------------------------------------------------------------------

## Main File
I created a main file where I concentrated the access to the functionalities through a menu, where the user can choose what is going to do with the app.
The user choice variable is kept in the 'result' variable. So as to access it when instantiating the class, I used the convention that variables named with the function name, 'main', and a variable name, are accessible outside the function:
```python
def main():
    """Inside the function we build the radio button questionnaire. Outside the function,
    and necessarily so, we declare the instantiation of the imported class.
    Finally we connect each radio button option to a specific method, mediated by the
    instance"""
    main.result = radiolist_dialog(
        title="Main",
        text="What Do You Want To Do?",
        values=[
            ("add", "Add a Bookmark"),
            ("delete", "Delete a Bookmark"),
            ("see", "See All Bookmarks"),
            ("search", "Search the Bookmarks"),
            ("update", "Update a Bookmark"),
        ],
    ).run()


main()
```

Outside the main function I instantiated the Add class that I imported to this file:
```python
sum = Add()
```
Note that 'Add' is empty and it will accept whatever values the input objects will create inside the methods.  
Now is just the case of connecting the menu alternatives to their corresponding methods:
```python
if main.result == "add":
    sum.add_bkmk()
if main.result == "delete":
    sum.delete()
if main.result == "see":
    sum.see()
if main.result == "search":
    sum.search()
if main.result == "update":
    sum.update()
```

The whole main file:
```python
from loguru import logger
from prompt_toolkit.shortcuts import radiolist_dialog
from bkmk_class import Add

################################################################################
# @author      : mclds
# @file        : main
# @created     : 21/08/2021
# @email       : mclds@protonmail.com
# @description : Main file where all functionalities are concentrated and
# accessed.
################################################################################

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch  # Decorator for loguru. All errors will go log. Has to be on all functions
def main():
    """Inside the function we build the radio button questionnaire. Outside the function,
    and necessarily so, we declare the instantiation of the imported class.
    Finally we connect each radio button option to a specific method, mediated by the
    instance"""
    main.result = radiolist_dialog(
        title="Main",
        text="What Do You Want To Do?",
        values=[
            ("add", "Add a Bookmark"),
            ("delete", "Delete a Bookmark"),
            ("see", "See All Bookmarks"),
            ("search", "Search the Bookmarks"),
            ("update", "Update a Bookmark"),
        ],
    ).run()


main()


sum = Add()
if main.result == "add":
    sum.add_bkmk()
if main.result == "delete":
    sum.delete()
if main.result == "see":
    sum.see()
if main.result == "search":
    sum.search()
if main.result == "update":
    sum.update()
```
