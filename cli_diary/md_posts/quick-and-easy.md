---
title: quick_and_easy
date: 2021-07-14 21:22:00
tags: python, automation 
---

I just had a disconcertingly pleasurable experience with python.  
I was expecting toils and tribulations, but everything worked beautifully at the first try, and now I'm charged with a warrior mindset that  
has no outlet for its intensity.  
So I think I'll just write a post about it.  
I am now, for no weighty reason, trying to create web presences of my cli apps. It's a way for me to learn a bit more of PHP, CSS, HTML and, eventually, and probably kicking and screaming; JavaScript.  
I'm trying to replicate their functionalities in a web environment. Up until now it has been fun. PHP is a delight to learn, and web design is extremely tactile.  
You have almost immediately a, if not physical, visible result to your efforts.  
Until now I've been avoiding frameworks and such like, with the objective of having to use the core building blocks of web design. What is lost in sophistication,
is returned by creating a sound knowledge base. Or so we hope.  
One of the apps that I use more frequently is my notes app.  
It writes the note in a temporary vim file and stores it in a MySQL database. So all my notes are in txt files, written with syntax appropriated to that environment.
For example; here's a note that looks very much like all the others:
```
 To open a port for a application in linux,
 do the following:
 -----------------------------------------------
 iptables -A INPUT -p tcp --dport 4000 -j ACCEPT
 sudo systemctl restart iptables
 ------------------------------------------------
 To test it, do this:
 ------------------------------------------------
 ls | nc -l -p 4000
 ------------------------------------------------
 and now in another terminal:
 ------------------------------------------------
 telnet localhost <port number>
 ------------------------------------------------
  https://tinyurl.com/yjjk4n8v
  ```
As you can see, I use dashes to separate code from comments and generally make it look less boring. I never gave it much thought as it seemed to me to be a perfectly reasonable way to write notes. And since they are to be used by only by  me, this didn't bothered me at all. Or, at least, until I tried to convert the notes to HTML.  
The lines occupied all of the screen, stretched for several lines and generally destroyed the layout.  
So I needed to remove the dashes from around 130 database entries and create clean, legible HTML versions, to use in a putative notes site.  
When I was rummaging through MySQL documentation, explaining to me how to store the result of a SQL query into a file, (a process that seemed complicated and really not what I needed), I remembered that every time I used the cli app in "see_all" mode, I was in fact downloading all the database. All that was needed was to go from the database to files.  
In the end, I ended doing this:  
1. I connected to the database and selected everything:
```python
def notes():
    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes")
        cur = conn.cursor()
        query = 'SELECT * FROM notes'
        cur.execute(query,)
        records = cur.fetchall()
```
2. created a value in the array:
```python
for row in records:
```
3. created a string with the ID field of the database concatenated with '.txt'. In the end you end up with files like '299.txt'.  
```python
file = str(row[0]) + '.txt'
```
4. opened a file to write this string as a title,
```python
f = open(file, 'w')
```
5. and wrote in it the notes field, that is the sixth field in the database.
```python
f.write(str(row[5]))
```
I was expecting that what I was doing was programming wishful thinking. That the opened db would never interact with files, or some other typical impediment I face when trying to do things I haven't really studied or understood deeply.  
But this time it was immediate. When I saw all the files that it created, I couldn't believe that had been so easy.  
Thank God for little blessings.  
Then I had to run the script through a hundred and change files, to clean them. But this seemed, and was, much easier.  
This is what I did:  
1. First I created the function that would do the replacement:
```python
def replace(filepath):
```
2. Then I defined that the file to be cleaned would be called filepath, as it will be needed later on to find the files.  
```python
input = open(filepath, 'rt')
```
3. Decided that the output files would have still the id's of the database, appending it a '_clean' suffix.  
```python
new_file = filepath + '_clean'
output = open(new_file, 'wt')
```
4. Here I replace the dashes by spaces and close the files.  
```python
for line in input:
    output.write(line.replace('-', ' '))
input.close()
output.close()
```
5. This is the directory where all the files to be cleaned are located:  
```python
dir = '/srv/http/notes/before'
```
6. Here starts the loop that states that, for every file found in said directory:  
```python
for filename in os.listdir(dir):
```
7. create a URL joining the path of the directory plus the name of the file:  
```python
filepath = os.path.join(dir, filename)
```
8. and finally use the function defined above on this new path object:  
```python
replace(filepath)
```

And that is it. I hope this may be of some use to anyone. For me it was a pleasant surprise.  
I'll leave you with the whole code of the files:  

```python
""" This module will download all note entries in notes db and put them in files """
from mysql.connector import connect, Error


def notes():
    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes")
        cur = conn.cursor()
        query = 'SELECT * FROM notes'
        cur.execute(query,)
        records = cur.fetchall()
        for row in records:
            file = str(row[0]) + '.txt'
            f = open(file, 'w')
            f.write(str(row[5]))
            f.close()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    notes()
```

And the function that cleaned the files:  
```python
""" Script to erase dashes from db entries and replace them with spaces. """
import os


def replace(filepath):
    input = open(filepath, 'rt')
    new_file = filepath + '_clean'
    output = open(new_file, 'wt')

    for line in input:
        output.write(line.replace('-', ' '))
    input.close()
    output.close()


dir = '/srv/http/notes/before'
for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    replace(filepath)


if __name__ == "__main__":
    replace(filepath)
```
---------------------------------------------------------------------------------

## UPDATE
For completeness sake, I returned to this post to add the file that converts text files to HTML. I used a very nifty app called [txt2html](http://txt2html.sourceforge.net/txt2html.html#files) that did much of the work. As it is an app not a library, I had to use Python's subprocess to run it. But, all in all, easy peasy.  
1. Define the subprocess command. Here we call txt2html, defining as the original files the ones set by filepath, and define the output files with the same name plus an html suffix.  
```python
 cmd = 'txt2html --infile ' + filepath + ' --outfile ' + filepath + '.html'
```
2. Next we run the subprocess command with the 'shell=True' flag, that ensures that the behaviour is exactly the same as if running on shell. This is very frowned upon, but in my limited experience, things tend to work with this flag and not to, when it's not used. So, until anyone explains me better why this is so evil, I'll keep using it.  
```python
 subprocess.run(cmd, shell=True)
```
3. The rest of the process is similar to the other file, so there's nothing to add here.  
```python
dir = '/srv/http/notes/clean'
for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    convert(filepath)
```

The full code:  
```python
""" Script to convert text files in html. """
import os
import subprocess


def convert(filepath):
    """ Convert txt files by running them through a loop that converts them to html """
    cmd = 'txt2html --infile ' + filepath + ' --outfile ' + filepath + '.html'
    subprocess.run(cmd, shell=True)


dir = '/srv/http/notes/clean'
for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    convert(filepath)


if __name__ == "__main__":
    convert(filepath)
```
