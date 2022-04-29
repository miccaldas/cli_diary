---
title: "I Have a Problem - Epilogue"
mainfont: Iosevka
---

I might be a little hasty, but I would say that I got the automating of the SQLite database table sorted.  
I tried it a bunch of times and everything seems to be in order. I would be euphoric if it wasn't this sinking feeling that I might've overlooked something.  
But I think that this is more the result of being so involved in solving this. This one took a toll on me.  
I was greatly misinformed _vis a vis_ the relaxing qualities of pursuing an hobby.  
Maybe it's just me that haven't learned to relax yet. It'll probably take another 48 years.  
So, if you remember or read the last post, I had two major problems, creating variables dynamically and finding the correct string manipulations that create a passable SQL query.  
In the end, I sidestepped the former and solved the latter.  
I was very ill at ease regarding the creation of dynamic variables. Everything and everyone that I found online said how bad an idea it is. And if it's
still not clear for me why this is worse than spitting on soup (a Portuguese saying to describe something that is morally wrong), but it was enough for me to spend some effort in finding a solution that wouldn't go through that road. What I found is that I didn't need to. Which corroborates the myriad of people that I found in
Stack Overflow and its ilk, saying that one of the reasons for not doing it, was that there is always better solutions. I think I found one.  
Let me show you what I've done:  

1. Here are my imports. I have [collections](https://docs.python.org/3/library/collections.html) to create the ordered dict, [sqlite3](https://docs.python.org/3/library/sqlite3.html) to make the calls to the database, [colr](https://pypi.org/project/Colr/) because is very cool library to colorize terminal output, [icecream](https://github.com/gruns/icecream) is just the sweetest thing and I love it, [re](https://docs.python.org/3/library/re.html) is there for reasons that will become clear ahead.
```python
import collections
import sqlite3
from colr import color
from icecream import ic
import re
```
2. Asking for the names of the database and its table:
```python
db_name = input(color('What name do you want for the database? ', fore='#585a47'))
table_name = input(color('What name do you want for the table? ', fore='#585a47'))
```
3. Creating the database. Printing some strings just for peace of mind:
```python
try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    ic("Database created and Successfully Connected to SQLite")
    sqlite_select_Query = "select sqlite_version();"
    cur.execute(sqlite_select_Query)
    record = cur.fetchall()
    ic("SQLite Database Version is: ", record)
    conn.commit()
except sqlite3.Error as e:
    ic("Error while connecting to db", e)
finally:
    if(conn):
        conn.close()
```
4. Here, just as a refresher, is the code that collects the information about table structure from the users:
```python
    a = collections.OrderedDict()
    col_num = int(input(color('How many columns will you need? ', fore='#ff6f69')))
    for y in range(col_num):
        col_name = input(color('What is the name of your column? ', fore='#ff6f69'))
        key = col_name
        a.setdefault(key, [])
        att_num = int(input(color('How many attributes will you need? ', fore='#ff6f69')))
        for x in range(att_num):
            att_name = input(color('What is the name of your attribute? ', fore='#ff6f69'))
            a[key].append(att_name)
```
5. Creating an empty list,
```python
new = []
```
6. Opening a loop through the list that houses the answers to the questions of the last code block.
```python
for i in a:
```
7. Separating the column name and its associates attributes into a specific list:
``` python
b = (i, a[i])
```
8. Aggregating the information separated by columns and respective attributes into a list of lists:
```python
c = list(b)
```
9. Appending the columns name to a new list, as a string. The transformation to string is to have them prepared for the manipulations we'll do briefly.
```python
new.append(str(c[0]))
```
10. Isolating the attributes part of the list as string.
```python
d = str(c[1])
```
11. Replacing the comma between the attributes by a space.
```python
e = d.replace(',', '')
```
12. Aggregating the _commaless_ attributes to the 'new' list.
```python
new.append(e)
```
13. Transforming the list where you kept the column names and their attributes, after manipulation, into a string. 'Corda' in Portuguese, can mean 'string'.
```python
corda = str(new)
```
14. We now create a new string but without the '[]""'}' characters in it.
```python
cor1 = corda.translate({ord(i): None for i in '[]""'})
```
15. Another pass, to remove the apostrophes.
```python
cor2 = cor1.translate({ord(i): None for i in "'"})
```
16. Now we have the old problem, explained in detail in the last post, of what to do with the commas in the output. First we isolate the character in a variable.
```python
sub = ','
```
17. Then we look for matches of commas in our clean string
```python
matches = re.finditer(sub, cor2)
```
18. We identify their indices, and keep them in a list.
```python
matches_positions = [match.start() for match in matches]
oc = matches_positions
```
19. We noticed the following regularity in the distribution of the commas at this point. The first occurrence is there to separate the column name from its attributes, and we want to erase that one, the other is there to separate the list of attributes from the next key. And that we want to keep. So it's necessary to delete commas, skipping one value and starting from 0. Because strings are immutable it is necessary to create another string that will house the indices to be replaced.
For that, we use the following command:
```python
oc1 = oc[0::2]
```
20. We turn the string with the clean query into a list, so as to iterate through it.
```python
cor3 = list(cor2)
```
21. We open a iterator, setting as condition the indices on the list of the ones to replace.
```python
for idx in oc1:
```
22. Replacing the indices on the list of the query, with spaces, on the indexes that were marked in oc1.
```python
cor3[idx] = ''
```
23. Since we turned a string into a list, it separated all characters into different items. It's needed to join them back again.
```python
cor4 = ''.join(cor3)
```
24. Finally we define the structure of the query. This is what is going to be sent.
```python
query = 'CREATE TABLE ' + table_name + '(' + cor4 + ')'
```
25. And, at last, we send it to the database::
```python
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

    except sqlite3.Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()
```
This is what I've done. I believe that there's still room for improvement. Many of these steps were separated so I could have a clearer understanding of what I was doing, as people who think as they go along tend to do.  
But that will be work for another time.  
One where I'll be less scared of changing something and ruining it all.  
I'll leave you with the complete code:

```python
""" This module creates a SQLite database and defines and uploads a new table for said database"""
import collections
import sqlite3
from colr import color
from icecream import ic
import re

db_name = input(color('What name do you want for the database? ', fore='#585a47'))
table_name = input(color('What name do you want for the table? ', fore='#585a47'))

try:
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    ic("Database created and Successfully Connected to SQLite")
    sqlite_select_Query = "select sqlite_version();"
    cur.execute(sqlite_select_Query)
    record = cur.fetchall()
    ic("SQLite Database Version is: ", record)
    conn.commit()
except sqlite3.Error as e:
    ic("Error while connecting to db", e)
finally:
    if(conn):
        conn.close()


def collect_data():
    """ Here we ask the user the information needed to create a table, then we process the output until is fit to be a SQL query, and uploaded it to the db"""

    a = collections.OrderedDict()
    col_num = int(input(color('How many columns will you need? ', fore='#ff6f69')))
    for y in range(col_num):
        col_name = input(color('What is the name of your column? ', fore='#ff6f69'))
        key = col_name
        a.setdefault(key, [])
        att_num = int(input(color('How many attributes will you need? ', fore='#ff6f69')))
        for x in range(att_num):
            att_name = input(color('What is the name of your attribute? ', fore='#ff6f69'))
            a[key].append(att_name)

    new = []
    for i in a:
        b = (i, a[i])
        print(b)
        c = list(b)
        print(c)
        new.append(str(c[0]))
        print(new)
        d = str(c[1])
        print(d)
        e = d.replace(',', '')
        print(e)
        new.append(e)
    print(new)
    corda = str(new)
    cor1 = corda.translate({ord(i): None for i in '[]""'})
    cor2 = cor1.translate({ord(i): None for i in "'"})
    sub = ','
    matches = re.finditer(sub, cor2)
    matches_positions = [match.start() for match in matches]
    oc = matches_positions
    oc1 = oc[0::2]
    print('oc1 = ', oc1)
    cor3 = list(cor2)
    for idx in oc1:
        cor3[idx] = ''
    cor4 = ''.join(cor3)
    query = 'CREATE TABLE ' + table_name + '(' + cor4 + ')'

    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

    except sqlite3.Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    collect_data()
```
