---
title: "Making Sense of a RSS App"
date: 2021-02-16T02:18:29Z
tags: python, RSS
---

I revisited today the RSS app I changed some months ago. As, unfortunately, I start to expect from myself, nothing was documented, and I had to do some archaeology to understand what was going on.  
I will immortalize that effort in blog entry form, so as to not disappear into the yawning mouth of time.  
------------------------------------------------------------------------------------------------------------

## rss.py

This is the main file. For reasons known only to Miguel from the past, this module is not called main.py. Oh well.  
1. I imported unicode literals from future to satisfy a need from [questionary](https://questionary.readthedocs.io/en/stable/), which I also imported. Imported [sys](https://docs.python.org/3/library/sys.html) to create a exit option in the prompt options, and imported all the other modules, one for each functionality,
```python
from __future__ import unicode_literals
import sys
import questionary
from search_db import search
from show_rss import show_rss
from sources_search import sources
from append_rss import append_rss
from insert_db import delete_old, get_rss
from delete_rss import read_rss, delete_rss
```
2. created a function to house def rss():
```python
def rss():
    question = questionary.select(
        'What do you want to do?',
        choices=[
                'See Hacker News',
                'See OSNews',
                'See Reddit Commandline',
                'See Reddit Linux',
                'See Reddit Europe',
                'See The Geek Stuff',
                'See Roots of Progress',
                'See Slashdot',
                'See Slate Star Codex',
                'See Ars Technica',
                'See OSTechNix',
                '--------------------',
                'Add a feed',
                'Delete a feed',
                'Search the db',
                'Refresh db',
                'See db',
                '--------------------',
                'Exit',
                ],
    )
    answer = question.ask()
    print(answer)
```
3. and connected questions to respective modules.
```python
    if answer == 'See Hacker News':
        # 1
        sources('Hacker News')
    if answer == 'See Hackaday':
        sources('hackaday')
    if answer == 'See OSNews':
        sources('osnews')
    if answer == 'See Reddit Commandline':
        sources('commandline')
    if answer == 'See Reddit Linux':
        sources('linux')
    if answer == 'See Reddit Europe':
        sources('europe')
    if answer == 'See Roots of Progress':
        sources('rootsofprogress')
    if answer == 'See Slashdot':
        sources('slashdot')
    if answer == 'See Slate Star Codex':
        sources('slatestarcodex')
    if answer == 'See Ars Technica':
        sources('arstechnica')
    if answer == 'See Slashdot':
        sources('Slashdot: Linux')
    if answer == "See It's FOSS":
        sources("It's FOSS")
    if answer == 'See OSTechNix':
        sources('OSTechnNix')
    if answer == ('Add a feed'):
        append_rss()
    if answer == ('Delete a feed'):
        read_rss()
        delete_rss()
    if answer == 'Search the db':
        search()
    if answer == 'Refresh db':
        delete_old()
        get_rss()
    if answer == 'See db':
        show_rss()
    if answer == 'Exit':
        sys.exit()
```

4. All the code:
```python
from __future__ import unicode_literals
import sys
import questionary
from search_db import search
from show_rss import show_rss
from sources_search import sources
from append_rss import append_rss
from insert_db import delete_old, get_rss
from delete_rss import read_rss, delete_rss


def rss():
    question = questionary.select(
        'What do you want to do?',
        choices=[
                'See Hacker News',
                'See OSNews',
                'See Reddit Commandline',
                'See Reddit Linux',
                'See Reddit Europe',
                'See The Geek Stuff',
                'See Roots of Progress',
                'See Slashdot',
                'See Slate Star Codex',
                'See Ars Technica',
                'See OSTechNix',
                '--------------------',
                'Add a feed',
                'Delete a feed',
                'Search the db',
                'Refresh db',
                'See db',
                '--------------------',
                'Exit',
                ],
    )
    answer = question.ask()
    print(answer)

    if answer == 'See Hacker News':
        # 1
        sources('Hacker News')
    if answer == 'See Hackaday':
        sources('hackaday')
    if answer == 'See OSNews':
        sources('osnews')
    if answer == 'See Reddit Commandline':
        sources('commandline')
    if answer == 'See Reddit Linux':
        sources('linux')
    if answer == 'See Reddit Europe':
        sources('europe')
    if answer == 'See Roots of Progress':
        sources('rootsofprogress')
    if answer == 'See Slashdot':
        sources('slashdot')
    if answer == 'See Slate Star Codex':
        sources('slatestarcodex')
    if answer == 'See Ars Technica':
        sources('arstechnica')
    if answer == 'See Slashdot':
        sources('Slashdot: Linux')
    if answer == "See It's FOSS":
        sources("It's FOSS")
    if answer == 'See OSTechNix':
        sources('OSTechnNix')
    if answer == ('Add a feed'):
        append_rss()
    if answer == ('Delete a feed'):
        read_rss()
        delete_rss()
    if answer == 'Search the db':
        search()
    if answer == 'Refresh db':
        delete_old()
        get_rss()
    if answer == 'See db':
        show_rss()
    if answer == 'Exit':
        sys.exit()


rss()
```
--------------------------------------------------------------------------------------------

## sources_search.py

This module pertains to all searches that were generated in the main module.  
1. Imported [click](https://click.palletsprojects.com) and [SQLite](https://www.sqlitetutorial.net/sqlite-python/). One for beautification, the other to connect to the database. Everything tells me to change this to MySQL but until it breaks, as it most probably will, the code is protected by the 'if is not broken, don't fix it.', clause.  
```python
import click
import sqlite3
```
2. Because I needed to create a function attribute to carry the user's choice in the last file, I needed to declare it before the beginning of the function. I imagine that this must not be the correct way to do this, but, at the moment, this is all I know. I would change it, but I don't even know why or if it's wrong.  
```python
source = ''
```
3. Getting its query from rss.py, the function calls the db, and asks for rss_fts table, which has free text search enabled.
```python
def sources(source):
    with sqlite3.connect('rss.db') as db:
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

4. Full code:
```python
"""This module pertains to all searches that were generated in the main module"""
import click
import sqlite3

source = ''


def sources(source):
    """Getting its query from rss.py, the function calls the db, and asks for rss_fts
       table, which has free text search enabled."""
    with sqlite3.connect('rss.db') as db:
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


if __name__ == "__main__":
    sources(source)
```


