---
title: The 'db.py' File
date: 29-07-2023 07:30
mainfont: Iosevka
fontsize: 13pt
---


For my simple needs, there's no greater example of boilerplate code than a
database call.  
Apart from the *database* and the *query* everything is repeated from a call to
another, making it a prime candidate for automation.  
My latest effort was to create a file that has only one function, with only
three arguments, that caters to all my use cases.  
You just define a query, if you want to get information or upload it
and, optionally, if you want to use *%s* markers, the values for it.  
This is the code:  
  
```python
def dbdata(query, data, answers=None):
    """
    Collects list of posts on the db.
    We'll use this function as a template,
    letting the functions that call on it
    to define its structure. That being
    the query and if using .fetchall()
    or .commit()
    This permits writing just one db function
    per module.
    """
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="cli_apps",
        )
        cur = conn.cursor()
        if answers:
            cur.execute(query, answers)
        else:
            cur.execute(query)
        if data == "fetch":
            data = cur.fetchall()
        if data == "commit":
            data = conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data
```
  
As you can see, it defines *conn*, in this case with the *cli_apps* database and
*cur*, which is equal every time.  
*answers* is the name of the list that'll house the values to feed the *%s*
markers.  
You have a `cur.execute` command with and without `answers` because, as I defined it with
a default value of `None`, not only it's discretional, as allows you to put
nothing at all, as the default is *None*.  
I created a variable called *data* that has two possible values:  
  
1. **fetch** - That writes a `cur.fetchall()` command, for when you want to get
   information.  
2. **commit** - Inputs `conn.commit()`, For when you want to upload it.  
  
I'm in awe of how a simple little code can streamline my output.  
I'm very happy with it, and intend to add it to older projects, so I can use it
when I'm updating them.
