---
title: quick_and_easy-part-3
mainfont: Iosevka
---

These things grow organically.  
When I say "these things", I'm talking about projects from tinkerers such as myself. As we don't know what we don't know, it's very difficult to plan ahead in development.  
One recurring and perennial consequence, is the inability of doing things twice the same way.  
This last project is no exception.  
When I started thinking in automating the creation a web page every time a new note is inserted via cli, I realized that I didn't had, in web page form, some of the notes that existed in the database; and were accessible through the cli app.  
So, this is what i did:
1. These are my imports. I'll just leave them here. Their role will be clearer later on.  
```python
from mysql.connector import connect, Error
import shutil
from low_range import low_range
from high_range import high_range
from medium_range import medium_range
from datetime import datetime
```
2. Created a function that'll house too much of the code of the creation of the web pages.  
I should've broken this is 2 or 3 functions, probably created a class, but I was lazy, and did it all in one function.  
```python
def auto():
```
3. Remember when I said that one my best design decisions was to separate the web and cli databases? Well, turns out it wasn't. It was a good decision while I thought on how I was going to structure the app. I didn't want to mess up what I already had running and this solution minimized risks. But when I started thinking on the daily care of both the cli and web app it soon became apparent that this was no solution.  
My first step was to ascertain what notes were exclusively in the cli database.  
```python
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
```
4. I created a list, asked what notes didn't have a URL and stored them in the list.  
```python
        null_list = []
        query = "SELECT * FROM notes WHERE url is NULL"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            null_list.append(row)
```
5. Turned the list of tuples supplied, to a list of strings.  
```python
null_list = [[str(x) for x in tup] for tup in null_list]
```
6. Replaced the dashes I use in the cli version as separators, to spaces.
```python
null_list = [[x.replace('-', '') for x in i] for i in null_list]
```
7. Replaced the new line symbol by a break tag, that would be honored when I turned it to a php file.  
```python
null_list = [[x.replace('\n', '<br>') for x in i] for i in null_list]
```
8. Created a list with only the id's.  
```python
    new_id_list = []
    for lst in null_list:
        new_id_list.append(lst[0])
```
9. Created a empty URL list,  
```python
new_url_list = []
```
10. To create the new files, I used a template I called "source". Defined both the location on the server and on the folder structure.  
```python
    for lst in null_list:
        source = '/srv/http/notes/pages/styled_notes/index.php'
        destination = '/srv/http/notes/pages/styled_notes/' + str(lst[0]) + '-page.php'
        url = 'http://localhost/notes/pages/styled_notes/' + str(lst[0]) + '-page.php'
```
11. Now that I had the URLs, I could fill my list.  
```python
new_url_list.append(url)
```
12. Copied the source file into the new files.  
```python
shutil.copyfile(source, destination)
```
13. Opened all new notes pages,  
```python
with open(destination, 'r') as f:
            lines = f.readlines()
```
14. Inserted the text of the note at the line 19.  
```python
        lines[19] = str(lst[5])
        with open(destination, 'w') as f:
            f.writelines(lines)
```
15. To help me dimension the boxes that encircle the notes, I counted the lines they occupied.  
```python
    line_count = []
    for lst in null_list:
        line_count.append(lst[5].count('<br>'))
```
16. Gathered the line count, id, URL lists into one sole list. This is needed to write ``list(result)``, because zip is a byte object, and it only is accessible this way.
```python
    result = zip(line_count, new_id_list, new_url_list)
    result = (list(result))
```
17. For row in the database, if the line count value is higher or equal to 11 but smaller than 18, it opens a file that writes to index.css a CSS description of the note box, tailored for content that is a bit larger than the default. There is also an alteration in the html, so the new note box name in the CSS, is mirrored in the html.  
```python
    for i in result:
        if i[0] >= 11 and i[0] <= 18:
            low_range(i[1])
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "r") as f:
                lines = f.readlines()
                lines[15] = "<div class='box-" + i[1] + "'><i class='fas fa-quote-left fa2'></i><div class='text'><i class='fas fa-quote-right fa1'></i><div>"
            with open('/srv/http/notes/pages/styled_notes/' + i[1] + '-page.php', 'w') as f:
                f.writelines(lines)
                print('low  range')
```
18. If the line count is between 18 and 36, there is another CSS profile.  
```python
        if i[0] > 18 and i[0] <= 36:
            medium_range(i[1])
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "r") as f:
                lines = f.readlines()
                lines[15] = "<div class='box-" + i[1] + "'><i class='fas fa-quote-left fa2'></i><div class='text'><i class='fas fa-quote-right fa1'></i><div>"
            with open('/srv/http/notes/pages/styled_notes/' + i[1] + '-page.php', 'w') as f:
                f.writelines(lines)
```
19. And if it's bigger, another.  
```python
        if i[0] > 36:
            high_range(i[1])
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "r") as f:
                lines = f.readlines()
                lines[15] = "<div class='box-" + i[1] + "'><i class='fas fa-quote-left fa2'></i><div class='text'><i class='fas fa-quote-right fa1'></i><div>"
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "w") as f:
                f.writelines(lines)
                print('high range')
```
20. Finally, I connect again to the database, now just one database, and write the URL paths in the lines that don't have values.
```python
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        for i in result:
            print('url - ', str(i[2]))
            print('id - ', str(i[1]))
            query = "UPDATE notes SET url = '" + str(i[2]) + "' WHERE ntid = " + str(i[1])
            print(query)
            cur.execute(query)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
```

The whole file:
```python
#!/usr/bin/env python3.9

######################################################################
# @author      : mic (mic@$HOSTNAME)
# @file        : auto_notes.sh
# @created     : Saturday Jun 26, 2021 03:52:05 WEST
#
# @description : Publish notes inserted on cli on the website
######################################################################


from mysql.connector import connect, Error
import shutil
from low_range import low_range
from high_range import high_range
from medium_range import medium_range
from datetime import datetime


def auto():
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        null_list = []
        query = "SELECT * FROM notes WHERE url is NULL"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            null_list.append(row)
        null_list = [[str(x) for x in tup] for tup in null_list]
        # print(null_list)
    except Error as e:
        print("Error while connecting to db", e)

    null_list = [[x.replace('-', '') for x in i] for i in null_list]
    null_list = [[x.replace('\n', '<br>') for x in i] for i in null_list]

    new_id_list = []
    for lst in null_list:
        new_id_list.append(lst[0])

    new_url_list = []
    for lst in null_list:
        source = '/srv/http/notes/pages/styled_notes/index.php'
        destination = '/srv/http/notes/pages/styled_notes/' + str(lst[0]) + '-page.php'
        url = 'http://localhost/notes/pages/styled_notes/' + str(lst[0]) + '-page.php'
        new_url_list.append(url)
        shutil.copyfile(source, destination)
        with open(destination, 'r') as f:
            lines = f.readlines()
        lines[19] = str(lst[5])
        with open(destination, 'w') as f:
            f.writelines(lines)

    line_count = []
    for lst in null_list:
        line_count.append(lst[5].count('<br>'))

    result = zip(line_count, new_id_list, new_url_list)
    result = (list(result))
    for i in result:
        if i[0] >= 11 and i[0] <= 18:
            low_range(i[1])
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "r") as f:
                lines = f.readlines()
                lines[15] = "<div class='box-" + i[1] + "'><i class='fas fa-quote-left fa2'></i><div class='text'><i class='fas fa-quote-right fa1'></i><div>"
            with open('/srv/http/notes/pages/styled_notes/' + i[1] + '-page.php', 'w') as f:
                f.writelines(lines)
                print('low  range')
        if i[0] > 18 and i[0] <= 36:
            medium_range(i[1])
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "r") as f:
                lines = f.readlines()
                lines[15] = "<div class='box-" + i[1] + "'><i class='fas fa-quote-left fa2'></i><div class='text'><i class='fas fa-quote-right fa1'></i><div>"
            with open('/srv/http/notes/pages/styled_notes/' + i[1] + '-page.php', 'w') as f:
                f.writelines(lines)
        if i[0] > 36:
            high_range(i[1])
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "r") as f:
                lines = f.readlines()
                lines[15] = "<div class='box-" + i[1] + "'><i class='fas fa-quote-left fa2'></i><div class='text'><i class='fas fa-quote-right fa1'></i><div>"
            with open("/srv/http/notes/pages/styled_notes/" + i[1] + "-page.php", "w") as f:
                f.writelines(lines)
                print('high range')

    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        for i in result:
            print('url - ', str(i[2]))
            print('id - ', str(i[1]))
            query = "UPDATE notes SET url = '" + str(i[2]) + "' WHERE ntid = " + str(i[1])
            print(query)
            cur.execute(query)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)

    print(datetime.now)


if __name__ == "__main__":
    auto()
```
