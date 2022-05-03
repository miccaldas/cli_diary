---
title: "Setting Cli Diary With Clickable Links"
date: 01/05/2022
mainfont: Iosevka
---

I realized that I could use the hyperlinks function in [Rich](https://rich.readthedocs.io/en/stable), to output links in my apps.  
I tested this in cli_diary and I'm very happy with the results.  
This is how I've done it:

First you ask the user what query he want to make, and search for it in the
database. You'll notice that I searched twice for the column 'title'; that
is to ensure that I'll have a tuple with the repeated title. One will be used as
the title proper, the other one will be modified to create the corresponding
file url. It was also created a variable with path to the html files.  

```python
      path = "/home/mic/python/cli_diary/cli_diary/html_posts"
      ask = input(click.style(" [*] - What do you want to search? ", fg="bright_green", bold=True))
  
      try:
          conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
          cur = conn.cursor()
          query = f"SELECT title, title FROM cli_diary WHERE MATCH(title, k1, k2) AGAINST ('{ask}')"
          cur.execute(query)
          records = cur.fetchall()
          conn.close()
      except Error as e:
          print("Error while connecting to db", e)
```

We then take the list of tuples that was created and add '.html' to one of the
title's entries, so as to produce the file name:

```python
      tupfiles = []
      for i in records:
          tupfile = (i[0], i[1] + ".html")
          tupfiles.append(tupfile)
```

We then create the complete urls. These two steps might've been summarized in
one, but I wanted to be sure of the steps I was going to take and where problems
could appear, so I opted to break the constructions in parts.  

```python
      roads = []
      for t in tupfiles:
          road = (t[0], f"{path}/{t[1]}")
          roads.append(road)
```

Finally, is just a question of creating a Rich text instance, with the some
formatting, for prettiness sake.  

```python
      for road in roads:
          print(f"[bold #B2B8A3] (**) - [link=file:///{road[1]}]{road[0]}[/link][/]")
```

Here's the full code:

```python
  """
  Searches db for query. Presents results.
  """
  import os
  import pathlib
  import sys
  
  import click
  import isort
  import snoop
  from mysql.connector import Error, connect
  from rich import print
  from rich.filesize import decimal
  from rich.markup import escape
  from rich.text import Text
  from rich.tree import Tree
  
  
  # @snoop
  def search():
      """
      Uses MySQL queries with fulltext to search the database.
      Uses Rich library to allow for clickable links on the posts.
      """
  
      path = "/home/mic/python/cli_diary/cli_diary/html_posts"
      ask = input(click.style(" [*] - What do you want to search? ", fg="bright_green", bold=True))
  
      try:
          conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
          cur = conn.cursor()
          query = f"SELECT title, title FROM cli_diary WHERE MATCH(title, k1, k2) AGAINST ('{ask}')"
          cur.execute(query)
          records = cur.fetchall()
          conn.close()
      except Error as e:
          print("Error while connecting to db", e)
  
      tupfiles = []
      for i in records:
          tupfile = (i[0], i[1] + ".html")
          tupfiles.append(tupfile)
  
      roads = []
      for t in tupfiles:
          road = (t[0], f"{path}/{t[1]}")
          roads.append(road)
  
      for road in roads:
          print(f"[bold #B2B8A3] (**) - [link=file:///{road[1]}]{road[0]}[/link][/]")
  
  
  if __name__ == "__main__":
      search()
```





