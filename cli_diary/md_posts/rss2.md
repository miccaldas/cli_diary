---
title: more tales about RSS
date: 2021-06-23 08:34:12
tags: python, RSS
---


I just realized I didn't finish my post on the RSS feed app.  
It was my intention to document and comment all the RSS app's modules in a blog post.  
So the code doesn't end up looking as if it was found in a museum with a tag saying: "Unknown Origin. Age: Undetermined. Usage: Some sort of chamber pot, or possibly a drinking vessel. Maybe both."  
I meant to do it, but then I changed my approach to the blog, and this was tossed into the "to do when you're not thinking about anything.", pile.  
As I currently am, very actively, not thinking in anything, this must be an auspicious moment to resume this endeavor.  
------------------------------------------------------------------------------------------------------------------------

## append_rss.py

This module is needed because, in insert_db.py, the line `fp = feedparser.parse(url)`, wouldn't accept a function object, which is what happens if you import the outcome of this module directly. So, it was necessary to assure that the URL would be formatted as a string. Hence the passage to a text file. This has the added advantage of creating a record of all feeds in use.  
```python
import click

    def append_rss():
        new_rss = input(click.style(' What is the url you want to add? ', fg='magenta', bold=True))
        envio = open('url_list.txt', 'a')
        envio.write(new_rss)
        envio.close()

    if __name__ == "__main__":
    append_rss()
```
----------------------------------------------------------------------------------------------

## delete_rss.py

Since a text file was created in the last module with a list of the URLs of the
feeds in use by the app, it stands to reason that, if wanted, we would edit this
file to delete a feed. - We first show the user the available feeds in file 'lista':
```python
def read_rss():
    with open('url_list.txt') as f:
        lista = f.read()
        print(lista)
```
Then we create another function to house the deletion command.
```python
def delete_rss():
```
You need to open the file and read its contents in memory, then open the file again write the
line to it but without the line you wish to omit.
```python
delete_rss = input(click.style(' What is the url you want to delete? ', fg='magenta', bold=True))
with open('url_list.txt', 'r') as f:
    lines = f.readlines()
with open('url_list.txt', 'w') as f:
    for line in lines:
        if line.strip('\n') != delete_rss:
            f.write(line)


if __name__ == "__main__":
    delete_rss()
```
-----------------------------------------------------------------------------------------------------

## insert_db.py

In order to keep our database clean and up to date we'll first delete old entries in the database,
and create new ones. - From [Dateutil](https://dateutil.readthedocs.io/en/stable/index.html), a library for date manipulations, we'll import parse. We also need SQLite for db access and [Feedparser](https://pythonhosted.org/feedparser/#) for the RSS.
```python
from dateutil.parser import parse
import sqlite3
import feedparser
```
Open a SQLite connector and erase all entries in the table,
```python
def delete_old():
    with sqlite3.connect('rss.db') as db:
        cur = db.cursor()
        inserir = 'DELETE FROM rss;'
        cur.execute(inserir,),
        db.commit()
```
Define a function containing the URL of the RSS.
Define what elements of the feed we are going to use. 
```python
def get_rss():
```
Read the file into a list of lines,
 ```python
with open('url_list.txt') as f:
	urls = f.read().splitlines()
``` 
define 0 as the start of our index,
 ```python
index = 0
```
connect to the db,
 ```python
with open('url_list.txt') as f:
	urls = f.read().splitlines()
```
create feedparser object for each publication in the file list,
 ```python
for url in urls:
	fp = feedparser.parse(url)
	nome = fp['feed']['title']
	print(nome)
```
for each unique number that defines each content piece, we take out the ones that have a item named 'title' and 'link' and turn them to strings. As not all publications had the 'published' item, it was necessary to place its extraction inside a 'try/except' element, or the module would stop with key and attribute errors. Also, as it is a time element, the date format imported by the feed is not valid in SQLite3. So it was necessary to change it to something more acceptable.  
 ```python
for index in range(len(fp.entries)):
	try:
		titulo = fp.entries[index].title
		titulo = str(titulo)
		linque = fp.entries[index].link
		linque = str(linque)
		publi = fp.entries[index].published
		publi = str(publi)
		pub = parse(publi)
		tempo = pub.strftime('%y/%m/%d')
	                    except KeyError:
                        pass
                    except AttributeError:
                        pass
                    try:
                        fp.entries[index].pubDate
                        publi = fp.entries[index].pubDate
                        publi = str(publi)
                        pub = parse(publi)
                        tempo = pub.strftime('%y/%m/%d')
                    except KeyError:
                        pass
                    except AttributeError:
                        pass
                except AttributeError:
                    try:
                        fp.entries[index].updated
                        publi = fp.entries[index].updated
                        publi = str(publi)
                        pub = parse(publi)
                        tempo = pub.strftime('%y/%m/%d')
                    except KeyError:
                        pass
                    except AttributeError:
                        pass
                    try:
                        # 6
                        fp.entries[index].pubDate
                        publi = fp.entries[index].pubDate
                        publi = str(publi)
                        pub = parse(publi)
                        tempo = pub.strftime('%y/%m/%d')
                    except KeyError:
                        pass
                    except AttributeError:
                        pass

                inserir = 'INSERT INTO rss (name, title, link, date) VALUES (?, ?, ? , ?)'
                cur.execute(inserir, (nome, titulo, linque, tempo)),
                db.commit()
```
-----------------------------------------------------------------------------------------------------

## show_rss.py

This module shows the content of the db.  
Turned it to a module, so I can separate changing the db and seeing it.  
In essence, you just open the db and embellish the output.  
```python
with sqlite3.connect('rss.db') as db:
        cur = db.cursor()
        cur.execute('SELECT * FROM rss ORDER BY strftime(date) ASC')  # 1
        rows = cur.fetchall()
        for row in rows:
            print(click.style('Ж - ', fg='bright_blue', bold=True), click.style(str(row[1]), fg='bright_blue', bold=True))
            print(click.style('Щ - ', fg='bright_cyan', bold=True), click.style(str(row[2]), fg='bright_cyan', bold=True))
            print(click.style('Ÿ - ', fg='bright_blue', bold=True), click.style(str(row[3]), fg='bright_blue', bold=True))
            print(click.style('Ʞ -', fg='bright_cyan', bold=True), click.style(str(row[4]), fg='bright_cyan', bold=True))
            print('\n')
```
-------------------------------------------------------------------------------------------------------

## sources_search.py

Internal function that calls the db by publication. Called from the main module.
```python
ith sqlite3.connect('rss.db') as db:
        cur = db.cursor()
        expression = 'SELECT * FROM rss_fts WHERE rss_fts MATCH ? ORDER BY date DESC'
        cur.execute(expression, (source,))
        record = cur.fetchall()
        for row in record:
            print(click.style(' 𝝵 ', fg='bright_magenta', bold=True),
                  (click.style(str(row[1]), fg='bright_magenta', bold=True)))
            print(click.style(' 𝞇 ', fg='bright_magenta', bold=True),
                  (click.style(str(row[2]), fg='bright_blue', bold=True)))
            print(click.style(' 𝝮 ', fg='bright_magenta', bold=True),
                  (click.style(str(row[3]), fg='bright_white', bold=True)))
            print('\n')
```


