---
title: notes_project_part_three
date: 2021-09-29 08:57:08
tags: python, web, notes
---

I've been fiddling with my notes app so as to get a bit more information and control regarding the keywords. I've noticed that there are some poor examples of tagging. Tags that I didn't gave much thought and now signify nothing, tags that are only marginally diferent and report to the same thing and and use of singular and plural forms of the same word. Many times this is the best way to guarantee that the tag will be useful. If I put both versions of the word in the tags, I'm much more likely to find it at first try.  
Off course, and this is what I intend to do henceforth, with just a smidge of
discipline, I could just use the plural form, and that will be enough.
I wrote some comments on a file, during the beginning of the project, just to be
sure that I wouldn't loose my aim for the note app changes. That, as expected,
had mixed results. I couldn't do all that I set out to do, mainly because some
of the ideas were stupid, or too contrived or just simply too verbose to be of
any real use.  
After a few days, I got back to this problem and was able to reduce the
complexity of the code.
Although most of it it's pretty self-explanatory, or at least it seems that way
when everything is still fresh on my head, there is two or three comments I
would like to make.  
To add all the output of the keyword columns, I used this MySQL expression:
```python
"SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
```
If I just could remind myself what I had did just some hours ago, I would have
saved myself a lot of trouble; as you can in the "stats" post I wrote after this
one.
I think it's important to mention how I used the fuzzy searcher because, even if
I believe it's an easy library and all is clear for now. In two weeks or less
this code will become *terra incognita*.  
To do this we created a list with the three keyword values, and for each one,
Thefuzz would run all the tags records in comparison, and output only the
highest similarity value found.  
```python
self.keywords = [self.k1, self.k2, self.k3]
        for k in self.keywords:
            value = process.extractOne(k, self.records)
```
Then a funny problem appeared. I had set the similarity threshold in everything
above 80. If it was that high, it would trigger a message asking the user if he
wanted to change the tag. The problem I didn't foresaw was that old, repeated
tags would have a value of 100, and because of this the app was asking the user
if he wanted to exchange its tag by the exactly same tag!  
This was easily resolved by defining a new interval where the upper tier would
be below 100.
```python
if (
    80 < value[1] < 100
    ):
 chg_tag_decision = input(
                    click.style(
                        f"We have noticed that you inputed the word {k}, that is very similar to the word {value[0]}, that we already have as a keyword. Won't you use it instead? [y/n] ",
                        fg="magenta",
                        bold=True,
                    )
                )
```

Here it is the full code:

```python
"""Collects user input, checks keywords for similarity, if they're new and their frequency.
Sends information to the database and creates the md and html pages."""
import time
import subprocess
import click
from loguru import logger
from thefuzz import fuzz
from thefuzz import process
from colr import color
from mysql.connector import connect, Error

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


class Add:
    """The class starts with user input and a list with all tags in a string list.
    Having them separated will simplify processes. With this information collected,
    first we'll ask the keywords questions and run its processes, one by one.
    After this is done we'll send the information to the database and create the
    md and html files."""

    @logger.catch
    def input_data(self):
        """All the user inputs needed to create a new entry are located here."""
        self.title = input(click.style(" Title? » ", fg="magenta", bold=True))
        self.k1 = input(click.style(" Choose a keyword » ", fg="magenta", bold=True))
        self.k2 = input(click.style(" Choose another... » ", fg="magenta", bold=True))
        self.k3 = input(click.style(" And another... » ", fg="magenta", bold=True))
        print(click.style(" Write a note.", fg="magenta", bold=True))
        time.sleep(0.2)
        self.note = click.edit().rstrip()

    if __name__ == "__main__":
        input_data()

    @logger.catch
    def taglst(self):
        """Union allows to combine two or more sets of results into one, but,
        the number and order of columns that appear in the SELECT statement
        must be the same, and the data types must be equal or compatible.
        Union removes duplicates.
        """
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
            logger.info(query)
            cur.execute(query)
            records = cur.fetchall()  # Results come as one-element tuples. It's needed to turn it to list.
            self.records = [i for t in records for i in t]
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    if __name__ == "__main__":
        taglst()

    @logger.catch
    def issimilar(self):
        """Uses Thefuzz library to compare keyword strings. If similarity is above 80%,
        it prints a mesage asking if the user wants to change it."""
        self.keywords = [self.k1, self.k2, self.k3]
        for k in self.keywords:
            value = process.extractOne(k, self.records)
            if value[1] > 80:
                chg_tag_decision = input(
                    f"We have noticed that you inputed the word {k}, that is very similar to the word {value[0]}, that we already have as a keyword. Won't you use it instead? [y/n] "
                )
                if chg_tag_decision == "y":
                    if k == self.k1:
                        self.k1 = value[0]
                    if k == self.k2:
                        self.k2 = value[0]
                    if k == self.k3:
                        self.k3 = value[0]
            else:
                pass

    if __name__ == "__main__":
        issimilar()

    @logger.catch
    def add_to_db(self):
        """Creates the urls for pages and sends the data to the database"""
        self.pg_tit = self.title.replace(" ", "_").replace("'", "")
        self.md_path = "/srv/http/notes/pages/markdown/" + self.pg_tit + ".md"
        self.url = "http://localhost/notes/pages/html/" + self.pg_tit + ".html"
        answers = [self.title, self.k1, self.k2, self.k3, self.note, self.url]
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = "INSERT INTO notes (title, k1, k2, k3, note, url) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(query, answers)
            conn.commit()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()
        print(color(f"[*] - The entry named: {self.title}, was added to the database.", fore="#acac87"))

    if __name__ == "__main__":
        add_to_db()

    @logger.catch
    def add_md_page(self):
        """We create a new markdown file in its folder and write to it, the content
        of the meta-data, and the note."""
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = "select * from notes order by ntid desc limit 1"
            cur.execute(
                query,
            )
            records = cur.fetchall()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

        for row in records:
            id = row[0]
            titulo = row[1]
            time = row[7]
            k1 = row[2]
            k2 = row[3]
            k3 = row[4]
            nota = row[5]

        with open(self.md_path, "w") as f:
            f.write("---")
            f.write("\n")
            f.write("id: " + str(id))
            f.write("\n")
            f.write("title: " + titulo)
            f.write("\n")
            f.write("author: mclds")
            f.write("\n")
            f.write("time: " + str(time))
            f.write("\n")
            f.write("tags: " + k1 + ", " + k2 + ", " + k3)
            f.write("\n")
            f.write("---")
            f.write("\n")
            f.write(nota)
        print(color(f"[*] - It was created the markdown file named, {self.md_path}.", fore="#acac87"))

    if __name__ == "__main__":
        add_md_page()

    @logger.catch
    def add_html_page(self):
        """Where we create a html version of the markdown file.
        We just convert the md file into an html one, and
        put it in the html folder."""
        html_path = "/srv/http/notes/pages/html/" + self.pg_tit + ".html"
        cmd = "touch " + html_path
        subprocess.run(cmd, shell=True)
        cmd = (
            "pandoc --highlight-style=zenburn --metadata title='"
            + self.title
            + "' -s '"
            + self.md_path
            + "' -o '"
            + html_path
            + "'"
        )
        subprocess.run(cmd, shell=True)
        print(color(f"[*] - It was created the html file named, {self.url}.", fore="#acac87"))

    if __name__ == "__main__":
        add_html_page()
```
