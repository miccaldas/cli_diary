---
title: quick_and_easy-part-2
mainfont: Iosevka
---

After the last post, the notes web-app has developed considerably and I would like to document the changes I needed to do.  
Due to the large number of notes, everything in this project has to be automated, to be, in the least, time-efficient.  
That has presented me with a lot of opportunities to deepen my Python knowledge, in order to achieve said automation. At times it has been so vexing and frustrating, that I looked for solutions in shell scripting. Something I know very little about, but where I was fairly certain the solutions to my problems were already found.  
In the end it was more instructional than a great furtherance of my objectives. Most of the found solutions were found with Python, with one or two exceptions, I think.  
That said, I would like very much to know more about shell scripting because, although the syntax is eye-watering, there is a lot of work already done there. The solutions are present and real. You just have to enjoy the fruits of past work.  
Another problem was the inevitable need to interact with code structures like [SASS](https://sass-lang.com) and [Pug](https://pugjs.org/api/getting-started.html). Which, even if very enticing, especially Pug, implied that I had to learn a new framework.  
I'm using a lot of pre-built, free-to-use, CSS snippets, made accessible by kind hearted designers, and if that gives me access to better ideas and execution, it makes me also contact with more sophisticated tools.  
In the end, I minimized complexity to the maximum. From SASS I used it exclusively to convert SCSS files, as they were made available, to traditional CSS, which, for now, is what browsers accept.  
I used Pug also to convert a file written in its markup style. But Pug presented a very interesting concept in HTML writing rationalization and simplification. I hope to get back to this, with more time and in more depth.  
For all the work that it created, the Notes Manager app is surprisingly, still, bare-boned. At this moment I'm still ironing out the kinks in site search, and haven't introduced any other functionality.  
This is also because search made me deviate from what I wanted to do in the beginning, _vis a vis_ databases. I didn't understood that there was absolutely no reason to presume a simpler, lighter data structure for the web version. This made me look into content tags, search and db structure. And hence the slowness.  
Add to this the fact that you have to standardize and make alterations in around 140 pages, and the time investment doesn't seem that huge.  
Coming, finally, to the files I created for this project; let's start with 'auto.py', that intends to automate content page creation.  
If you remember, I had exported all note entries in the database to individual text files, to later turn into php or html.  
This, I noticed suitably later, was a mistake.  
I could just as well converted them to php files immediately, which is what I'm using right now, and I would have saved a lot of cumbersome steps.  
I'm using PHP because of its ability to be injected into files, really helps when creating large volume content files. I have seen myself veer away from HTML and head, more and more, to PHP country.  
Some of these design decisions have to do with project structure I created for database oriented, web apps. I intend to do a small post just in that very same subject. Not to get very deeply into this here, I wanted to separate the html part that is viewable to the user, and a php file that would address backend needs.  
I created the pages that would receive php code through a 'require' tag. In the end I would have the specific individual note content in a folder, and in another, the display html pages where they will be seen.  
This is how it was structured:
-----------------------------------------------------------------------------------------------------

## 1 - auto.py
1. Imported [shutil](https://docs.python.org/3/library/shutil.html), to copy files around.  
```python
import shutil
```
2. created a function and determined what and where would be the template file.  
```python
def auto():
    source = '/srv/http/notes/pages/styled_notes/index.php'
```
3. In the beginning, boneheadedly, I thought I would make do only with integer id's and URLs to identify the content. To do that, I completed a list of all the note id's I had uploaded to the site. And that was my base.  
```python
f = open('number_list.txt', 'r')
```
4. I stripped them of newline symbols and organized them in their own rows, and closed the connection to the file.    
```python
numbers = [(line.strip()).split() for line in f]
f.close()
```
5. These id numbers were being outputted by MySQL like this: "'[6]'". It was necessary to strip everything that wasn't the string character from the output.  
```python
for number in numbers:
        numero = str(number)
        numero = numero[2:-2]
```
6. Defined the URL of the display files to be created.  
```python
destination = '/srv/http/notes/pages/styled_notes/' + numero + '-page.php'
```
7. Copied the file.  
```python
shutil.copyfile(source, destination)
```
8. Opened the display pages to read,  
```python
with open(destination, 'r') as f:
    data = f.readlines()
```
9. On line 19 of the file, I inserted a php tag with the note content and its title.  
```python
data[19] = "<?php require 'http://localhost/notes/pages/text1/" + numero + ".php'; ?>"
```
10. and wrote to it.  
```python
with open(destination, 'w') as f:
    f.writelines(data)
```

Full code document:  
```python
import shutil


def auto():
    source = '/srv/http/notes/pages/styled_notes/index.php'
    f = open('number_list.txt', 'r')
    numbers = [(line.strip()).split() for line in f]
    f.close()
    for number in numbers:
        numero = str(number)
        numero = numero[2:-2]
        destination = '/srv/http/notes/pages/styled_notes/' + numero + '-page.php'
        shutil.copyfile(source, destination)
        with open(destination, 'r') as f:
            data = f.readlines()
        data[19] = "<?php require 'http://localhost/notes/pages/text1/" + numero + ".php'; ?>"
        with open(destination, 'w') as f:
            f.writelines(data)


if __name__ == "__main__":
    auto()
```
--------------------------------------------------------------------------------------------

## 2 - html.py
This is a file that has precedence in the process in relation to the last file.  
It's a script to convert text to html. As I said, a step I didn't need to take.  
When I said that had looked, and found, shell solutions to my problems, but kept most of the code as Python; this is what I'm talking about: Subprocess.  
1. Import os and subprocess:  
```python
import os
import subprocess
```
2. Created a python function and used txt2html to convert the files:  
```python
def convert(filepath):
    cmd = 'txt2html --infile ' + filepath + ' --outfile ' + filepath + '.html'
```
3. called the function through subprocess, as txt2html its not a Python app.  
```python
subprocess.run(cmd, shell=True)
```
4. Defined where the text files were, and iterated through them, creating html files.  
```python
dir = '/srv/http/notes/clean'
for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    convert(filepath)
```

Whole code document:
```python
""" Script to convert text files in html. """
import os
import subprocess


def convert(filepath):
    """ First it is defined how to replace the characters and after how to access the files """
    cmd = 'txt2html --infile ' + filepath + ' --outfile ' + filepath + '.html'
    subprocess.run(cmd, shell=True)


dir = '/srv/http/notes/clean'
for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    convert(filepath)


if __name__ == "__main__":
    convert(filepath)
```
------------------------------------------------------------------------------------------------

## 3 - db_upload.py
For some reason I can not remember at this moment, it wasn't easy to translate the cli notes to web form. I had to go back and forth between the db and the site to get all the data.  
This is, summarily, all the work that was done in the next files presented here.  
In this file we uploaded the tags content to the site, in bunches of three tags per note and their respective ids.  
1. Imported mysql to connect to the database and itertools for grouping the entries.  
```python
from mysql.connector import connect, Error
from itertools import zip_longest
```
2. As per last time, I opened a file with the entries and cleaned them a bit:  
```python
with open('tagsaa.csv') as f:
    lines = f.read().splitlines()
```
3. Turn them into a python list:  
```python
string_list = ['8,backblaze,duplicity,backup', '10,flake8,error,ignore', '12,cc,card,credit', '14,backblaze,keys,backups', '15,umount,mount,unmounting', '16,numpy,array,append', '26,openssl,ssl,mail', '28,bind,keys,bindkeys', '30,editor,command line,editing', '32,markdown,line break,notabug', '34,python,delete,file', '38,table,tables,sqlite', '41,dictionary,python,key', '49,rowid,id,sqlite', '51,fulltext,sqlite utils,full text', '55,sqlite-utils,triggers,trigger', '63,strings,string,python', '66,string,skip,strings', '67,dictionary,item,dictionaries', '68,list,skip,remove', '74,cmus,player,music', '78,goaccess,logs,analytics', '86,mysql,columns,generated', '88,mysql,last row,rows', '91,mysql,backup,dump', '92,epub,web,self-hosted', '95,xdg-open,default,xdg', '99,ufw,port,range', '102,zsh-autosuggestions,zsh,oh-my-zsh', '103,sudo,password,script', '108,pip,pip3,python', '110,white house,market,white', '116,vim,clipboard,ssh', '125,user.,group,ps', '129,arch,source,aur', '130,indentation,python,unindent', '133,vim,commentar,comment', '134,php code sniffer,php,linter', '136,css,name,selector', '']
```
4. Cleaned again the content,
```python
newlist = [i for item in string_list for i in item.split(',')]
print(newlist)
```
5. Used the grouper function to chunk the entries together.
```python
def grouper(iterable_obj, count, fillvalue=None):
    args = [iter(iterable_obj)] * count
    return zip_longest(*args, fillvalue=fillvalue)
iterable = newlist
```
6. Created a function to insert the grouper content into the site.  
```python
def insert():

    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes_web")
        cur = conn.cursor()
        for x in grouper(iterable, 4, ''):
            query = 'UPDATE notes_web SET k1 = "' + x[1] + '", k2 = "' + x[2] + '", k3 = "' + x[3] + '" WHERE id = "' + x[0] + '"'
            print(query)
            cur.execute(query)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()
```

The whole content:
```python
from mysql.connector import connect, Error
from itertools import zip_longest

with open('tagsaa.csv') as f:
    lines = f.read().splitlines()


string_list = ['8,backblaze,duplicity,backup', '10,flake8,error,ignore', '12,cc,card,credit', '14,backblaze,keys,backups', '15,umount,mount,unmounting', '16,numpy,array,append', '26,openssl,ssl,mail', '28,bind,keys,bindkeys', '30,editor,command line,editing', '32,markdown,line break,notabug', '34,python,delete,file', '38,table,tables,sqlite', '41,dictionary,python,key', '49,rowid,id,sqlite', '51,fulltext,sqlite utils,full text', '55,sqlite-utils,triggers,trigger', '63,strings,string,python', '66,string,skip,strings', '67,dictionary,item,dictionaries', '68,list,skip,remove', '74,cmus,player,music', '78,goaccess,logs,analytics', '86,mysql,columns,generated', '88,mysql,last row,rows', '91,mysql,backup,dump', '92,epub,web,self-hosted', '95,xdg-open,default,xdg', '99,ufw,port,range', '102,zsh-autosuggestions,zsh,oh-my-zsh', '103,sudo,password,script', '108,pip,pip3,python', '110,white house,market,white', '116,vim,clipboard,ssh', '125,user.,group,ps', '129,arch,source,aur', '130,indentation,python,unindent', '133,vim,commentar,comment', '134,php code sniffer,php,linter', '136,css,name,selector', '']

newlist = [i for item in string_list for i in item.split(',')]
print(newlist)

# https://tinyurl.com/yk472wo3
def grouper(iterable_obj, count, fillvalue=None):
    args = [iter(iterable_obj)] * count
    return zip_longest(*args, fillvalue=fillvalue)


iterable = newlist


def insert():

    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes_web")
        cur = conn.cursor()
        for x in grouper(iterable, 4, ''):
            query = 'UPDATE notes_web SET k1 = "' + x[1] + '", k2 = "' + x[2] + '", k3 = "' + x[3] + '" WHERE id = "' + x[0] + '"'
            print(query)
            cur.execute(query)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == "__main__":
    insert()
```
-----------------------------------------------------------------------------------------

## 4 - titles.py
At some moment in the process, I, finally, understood that the notes titles were a necessity, and I had to import them to this project. This is what I did in this module.  
1. Import MySQL connection to Python.
```python
from mysql.connector import connect, Error
```
2. To compartmentalize and avoid heartbreak, I decided that the cli version and the web version would have their own separate databases, and that was one of my best design decisions to date. I took the entries in the 'title' column of the cli app, put them in a list and closed this connection.  
```python
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        tit_list = []
        title_list = """ SELECT ntid, title from notes """
        cur.execute(title_list)
        records = cur.fetchall()
        for row in records:
            tit_list.append(row)
    except Error as e:
        print("Error while connecting to db", e)
```
3. After that, I started another MySQL connection, now to my web database, to update it with the new/old content.  
```python
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes_web")
        cur = conn.cursor()
        print(tit_list)
        for tit in tit_list:
            answer = [str(tit[1]), int(tit[0])]
            print(answer)
            query = """ UPDATE notes_web SET title = %s WHERE id = %s"""
            cur.execute(query, answer)
            print(query)
            conn.commit()
```

Complete file:  
```python
from mysql.connector import connect, Error


def titles():
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        tit_list = []
        title_list = """ SELECT ntid, title from notes """
        cur.execute(title_list)
        records = cur.fetchall()
        for row in records:
            tit_list.append(row)
    except Error as e:
        print("Error while connecting to db", e)

    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes_web")
        cur = conn.cursor()
        print(tit_list)
        for tit in tit_list:
            answer = [str(tit[1]), int(tit[0])]
            print(answer)
            query = """ UPDATE notes_web SET title = %s WHERE id = %s"""
            cur.execute(query, answer)
            print(query)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    titles()
```
---------------------------------------------------------------------------------------

## 5 - urls.py
This files creates and uploads to the database the notes URLs in the site.  
1. I take the display pages already created, extract the URLs and the id's from their links into two parallel lists, that I posteriorly join into a dictionary, through zip.  
```python
    path = '/srv/http/notes/pages/styled_notes'
    files = os.listdir(path)
    linques = []
    ids = []
    for file in files:
        linques.append('http://localhost/notes/pages/styled_notes/' + file)
        ids.append(file[:-9])
        keys_list = ids
    values_list = linques
    zip_iterator = zip(keys_list, values_list)
    pages = dict(zip_iterator)
```
2. Then I add them to the database.  
```python
    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes_web")
        cur = conn.cursor()
        for key, value in pages.items():
            answers = [int(key), value]
            query = "INSERT IGNORE INTO notes_web (id, url) VALUES(%s, %s)"
            cur.execute(query, answers)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()
```

As always, complete file.
```python
import os
from mysql.connector import connect, Error


def urls():
    path = '/srv/http/notes/pages/styled_notes'
    files = os.listdir(path)
    linques = []
    ids = []
    for file in files:
        linques.append('http://localhost/notes/pages/styled_notes/' + file)
        ids.append(file[:-9])
        keys_list = ids
    values_list = linques
    zip_iterator = zip(keys_list, values_list)
    pages = dict(zip_iterator)
    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes_web")
        cur = conn.cursor()
        for key, value in pages.items():
            answers = [int(key), value]
            query = "INSERT IGNORE INTO notes_web (id, url) VALUES(%s, %s)"
            cur.execute(query, answers)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == "__main__":
    urls()
```
---------------------------------------------------------------------------------------------------

## 6 - update_tags.py
This was a difficult one to get right. For some reason, I wasn't being able to update the notes tags into the already existent rows. MySQL would start new entries with new content. Which is, dare I say it? 'No bueno.'   
But I finally got it right, and this is what I did.  
1. Here we open the old cli app database and go looking for the tag information linked to the notes already present in the web app.  
```python
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        f = open('update_tags.txt', 'r')
        lines = f.readlines()
        for line in lines:
            query = "SELECT ntid, k1, k2, k3 FROM notes.notes WHERE ntid = " + line
            cur.execute(query)
            records = cur.fetchall()
```
2. Then we write the content to a file.  
```python
            for row in records:
                f = open('tags_list.txt', 'a')
                f.write(row[1]),
                f.write('\n')
                f.write(row[2]),
                f.write('\n')
                f.write(row[3]),
                f.write('\n')
                f.write(str(row[0]))
                f.write('\n')
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()
```
3. Then I connect to the web app database, open the aforementioned file, turn it into a python list, clean it and group it in parties of four items. One id and three content tags.  
```python
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes_web")
        cur = conn.cursor()
        with open('tags_list.txt', 'r') as f:
            content_list = f.readlines()
        clean_list = []
        for i in content_list:
            clean_list.append(i.strip())
        n = 4
        final = [clean_list[i * n:(i + 1) * n] for i in range((len(clean_list) + n - 1) // n)]
        print(final)
```
4. Finally we pass the items as variables in a SQL query to the web app database, and everything is OK.  
```python
        for list in final:
            query1 = "UPDATE notes_web SET k1 = '" + list[0] + "', k2 = '" + list[1] + "', k3 = '" + list[2] + "' WHERE id = " + list[3]
            print(query1)
            cur.execute(query1)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()
```

Full Text:
```python
from mysql.connector import connect, Error


def update_tags():
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        f = open('update_tags.txt', 'r')
        lines = f.readlines()
        for line in lines:
            query = "SELECT ntid, k1, k2, k3 FROM notes.notes WHERE ntid = " + line
            cur.execute(query)
            records = cur.fetchall()
            for row in records:
                f = open('tags_list.txt', 'a')
                f.write(row[1]),
                f.write('\n')
                f.write(row[2]),
                f.write('\n')
                f.write(row[3]),
                f.write('\n')
                f.write(str(row[0]))
                f.write('\n')
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes_web")
        cur = conn.cursor()
        with open('tags_list.txt', 'r') as f:
            content_list = f.readlines()
        clean_list = []
        for i in content_list:
            clean_list.append(i.strip())
        n = 4
        final = [clean_list[i * n:(i + 1) * n] for i in range((len(clean_list) + n - 1) // n)]
        # print(final)

        for list in final:
            query1 = "UPDATE notes_web SET k1 = '" + list[0] + "', k2 = '" + list[1] + "', k3 = '" + list[2] + "' WHERE id = " + list[3]
            print(query1)
            cur.execute(query1)
            conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    update_tags()
```
