---
title: the_notes_project
date: 2021-08-29 21:26:45
tags: notes, web, python
---

Lately I returned to a project that had always some interesting challenges, my notes app. Because I already have something like two hundred and change notes, there is really no option but to mechanize all the steps. Doing it by hand, as I always do, is out of the question.  
My objective is replicate my cli note taking app in a web setting. I already did this project, but the results were not very satisfactory, despite achieving everything I set out to do.  
In broad strokes, to convert the app I need to:

1. Take the notes from the database,
2. Convert them to markdown,
3. Do any changes needed to the content,
4. Convert them to html,
5. Put them in the app,
6. Update the database with new content URLs.
7. Make changes to the current functionalities, to accommodate the alterations.

Unfortunately I didn't do this documenting exercise when all was fresh in my mind, so, this all will be a archaeological in nature. Let's hope we stay near the truth.  
Although the project is not finished, it has a tendency to be more labour intensive than expected, and this list may change. I leave here a list of important project files, where they're being used and what they do.
 
 <br>

 | Files                    | Sub-project       | Objective                                                                 |
 | ------------------------ | ----------------- | ------------------------------------------------------------------------- |
 | html_converter.py        | file_conversion   | Converts markdown files to html.                                          | 
 | md_converter.py          | file_conversion   | Converts database entries into markdown.                                  |
 | build_csv.py             | csv_file_creation | Creates a list with the id of the notes and their URLs.                   |
 | link_lst                 | csv_file_creation | File created by 'build_csv.py'. Internal use.                             |
 | id_lst                   | csv_file_creation | File created by 'build_csv.py'. Internal use.                             |
 | id_links.csv             | csv_file_creation | File created by 'build_csv.py'. Internal use.                             |
 | csv_cleanup.py           | csv_file_creation | Cleans the csv created automatically. Generates two lists: id's and URLs. |
 | build_csv.py             | csv_file_creation | Writes a csv file with the two lists and uploads it to the database.      |
 | chg_wordcloud.py         | wordcloud_tags    | Several activities needed to insert our data in the svg file.             |
 | beautsoup2.txt           | wordcloud_tags    | File created by 'chg_wordcloud.py'. Internal use.                         |
 | complete_lines.txt       | wordcloud_tags    | File created by 'chg_wordcloud.py'. Internal use.                         |
 | comprehension_output     | wordcloud_tags    | File created by 'chg_wordcloud.py'. Internal use.                         |
 | lines_tags1.txt          | wordcloud_tags    | File created by 'chg_wordcloud.py'. Internal use.                         |
 | text_tags_order.txt      | wordcloud_tags    | File created by 'chg_wordcloud.py'. Internal use.                         |
 | wordcloud_linenumbers.py | wordcloud_tags    | Defines what lines are to be edited in the svg file.                      |
 | all_tags.txt             | content_tags      | Contains all ocurrences of tags. Regardless if they're repeated or not.   |
 | sorted list.txt          | content_tags      | List of tags with no repeats.                                             |


<br>

I'll start by what is, more or less, the real beginning, a trove of notes, already in markdown, that I found inside a folder I use for archives.  
At first I thought that I found a lot of notes that weren't part of the current database. Because of this a lot of work went into preparing them and comparing them to the database content, to understand if they were, indeed, lost content. Turns out they weren't and much of this work was in vain.  Not completely because, what was learned in this stage, was used after in other places. So, silver linings.  
I imagine that the best beginning will be the file conversions. The seminal moment has to arrive when, in this second effort, we decide to let go of the files that we found, and focus only on converting the database's content. Where, in the end, everything could be found.  

### UPDATE
This has much changed since I wrote it. It is now significantly shorter. Mainly because I understood that much of what they were doing, or trying to do, was either wrong or a dead end.  
See the larger update at the bottom of this post.

<br>
<br>

----------------------------

### 1 - md_converter.py
This file dumps the database, does some alterations to it, adds metadata fields, and writes the note content beneath.  
1. Connects to the database:

~~~python
   try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT * FROM notes"
        cur.execute(
            query,
        )
        records = cur.fetchall()
~~~

2. Gets the title value from the first row of returned values, puts a dash instead of empty spaces in it, deletes the slashes, and from these changes creates a new title, ended in '.md':

~~~python
    for row in records:
        title = str(row[1])
        change_tit = title.replace(" ", "_")
        change_tit1 = change_tit.replace("/", "")
        filename = change_tit1 + ".md"
        logger.info(filename)
        writepath = "/srv/http/notes/pages/markdown/" + filename
        logger.info(writepath)
~~~

3. Now it's created the front-matter fields. They are:
   - ID,
   - Title,
   - Time,
   - Tags.

~~~python
            with open(writepath, "w+") as file:
                file.write("---\n")
                file.write("id: ")
                file.write(str(row[0]))
                file.write("\n")
                file.write("title: ")
                file.write(str(row[1]))
                file.write("\n")
                file.write("time: ")
                file.write(str(row[7]))
                file.write("\n")
                file.write("tags: ")
                file.write(str(row[2]))
                file.write(", ")
                file.write(str(row[3]))
                file.write(", ")
                file.write(str(row[4]))
                file.write("\n---\n")
                file.write("\n")
                file.write("~~~python\n")
                file.write(str(row[5]))
                file.write("\n")
                file.write("~~~")
~~~

The full text:

~~~python
"""Although some of the notes were already converted to markdown,
   there is more content in the app database that can be used."""
import os
import subprocess
from loguru import logger
from mysql.connector import connect, Error

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch  # Decorator for loguru. All errors will go into a log. Has to be on all functions.
def app_converter():
    """We'll dump the db and then iterate through it,
    turning every entry in a md file."""

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT * FROM notes"
        cur.execute(
            query,
        )
        records = cur.fetchall()

        for row in records:
            title = str(row[1])
            change_tit = title.replace(" ", "_")
            change_tit1 = change_tit.replace("/", "")
            filename = change_tit1 + ".md"
            logger.info(filename)
            writepath = "/srv/http/notes/pages/markdown/" + filename
            logger.info(writepath)
            with open(writepath, "w+") as file:
                file.write("---\n")
                file.write("id: ")
                file.write(str(row[0]))
                file.write("\n")
                file.write("title: ")
                file.write(str(row[1]))
                file.write("\n")
                file.write("time: ")
                file.write(str(row[7]))
                file.write("\n")
                file.write("tags: ")
                file.write(str(row[2]))
                file.write(", ")
                file.write(str(row[3]))
                file.write(", ")
                file.write(str(row[4]))
                file.write("\n---\n")
                file.write("\n")
                file.write("~~~python\n")
                file.write(str(row[5]))
                file.write("\n")
                file.write("~~~")
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app_converter()
~~~
<br>
<br>

----------------------------------------------

### 2 - html_converter.py
The module converts the markdown files just created to html ones. Because it's easier, I used [Pandoc](https://pandoc.org) instead of relying in Python tools.

1. If a filename is in the markdown folder, and is a markdown file, add its full path to a list.

~~~python
    folder = "/srv/http/notes/pages/markdown/"
    paths = []
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            paths.append(os.path.join(folder, filename))
        else:
            continue
~~~

2. For each of these full paths we collected, get just the filename part, take out the three last characters from it, add to them '.html', and use them in Pandoc as objective files for the markdown files.  

~~~python
    for path in paths:
        filename = os.path.basename(path)
        html_url = filename[:-3] + ".html"
        logger.info(html_url)
        cmd = "pandoc --highlight-style=zenburn -s " + filename + " -o" + html_url
        logger.info(cmd)
        subprocess.run(cmd, cwd=folder, shell=True)
~~~

3. Finally, pass all html files to their own folder.  

~~~python
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            cmd = "mv " + folder + "/" + filename + " /srv/http/notes/pages/html/"
            subprocess.run(cmd, shell=True)
~~~

Full text:

~~~python
"""Module that will convert all md files into html, using pandoc"""
import os
import subprocess
from loguru import logger

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch  # Decorator for loguru. All errors will go into a log. Has to be on all functions.
def convert():
    """I'll be using pandoc as shell command as it is easier than programming it"""
    folder = "/srv/http/notes/pages/markdown/"
    paths = []
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            paths.append(os.path.join(folder, filename))
        else:
            continue

    for path in paths:
        filename = os.path.basename(path)
        html_url = filename[:-3] + ".html"
        logger.info(html_url)
        cmd = "pandoc --highlight-style=zenburn -s " + filename + " -o" + html_url
        logger.info(cmd)
        subprocess.run(cmd, cwd=folder, shell=True)

    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            cmd = "mv " + folder + "/" + filename + " /srv/http/notes/pages/html/"
            subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    convert()
~~~
<br>
<br>

----------------------------------------------

### 3 - id_url_list.py
This module creates a list with the id and URL of each note. This will serve to insert the URLs in the database.  
The code is heavily commented, so I won't say another word and publish the full version right now.

~~~python
"""Module to get a list with the id of the notes and their urls"""
import os
import sys
import csv
import markdown
from loguru import logger
from pathlib import Path

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def id_url_list():
    """Create a file with the id and url of each note.
    This will be fed to the database."""

    md_page = "/srv/http/notes/pages/markdown/"  # This is needed to extract metadata values from the notes.
    db_html_page = (
        "http://localhost/notes/pages/html/"  # Format changes as this is how Nginx will look for the pages in the site.
    )

    notes = []

    for filename in os.listdir(md_page):  # For file in this folder:
        notes.append(md_page + filename)  # Creating the path for the markdown files
    logger.info(notes)

    id_list = []  # The appending list must be outside of the loop. Took me forever to get this one.
    title_list = []
    for note in notes:
        if note[-3:] == ".md":  # There were python files in the folder, it was needed to specify only 'md'.
            data = Path(note).read_text(
                encoding="utf-8"
            )  # Formulation from the libpath library. I think it enables reaching info tied to a path.
            md = markdown.Markdown(extensions=["meta"])  # Defines the meta.information extension.
            md.convert(data)
            str_id = list(md.Meta.items())[0][
                1
            ]  # Extract id value from metadata, by its position in the result dictionary.
            id_list.extend(str_id)  # The extend() method adds all the elements of an iterable to the end of a list.
            str_title = list(md.Meta.items())[1][1]  # Extract title metadata value.
            title_list.extend(str_title)

    titles = []
    for titsy in title_list:
        tits = titsy.replace(" ", "_")  # Many titles were phrases, it was needed to connect them.
        # tit = tits.lower()  # Pass them all to lowercase.
        title = db_html_page + tits + ".html"  # Add the html file identifier.
        titles.append(title)

    id_title_dict = {id_list[i]: titles[i] for i in range(len(id_list))}  # Converts two lists into a dictionary.

    # Let's create a items list, so we can send two values when we are writing the csv.
    # https://www.delftstack.com/howto/python/python-dictionary-index/
    itms = list(id_title_dict.items())

    # Here will be passing the new dictionary into a csv file that can be understood by the database.
    with open("id_links.csv", "w", newline="") as write_file:
        writer = csv.writer(write_file, delimiter="|")
        writer.writerow(["ntid", "link"])
        for item in itms:
            writer.writerow({item})


if __name__ == "__main__":
    id_url_list()
~~~
<br>
<br>

-------------------------------------------------------------------

### 4 - csv_cleanup.py
The csv produced by the Python library was far from OK. A case of garbage in, garbage out. Some cleaning was in order.  
This file is mainly a series of text manipulations, with the objective of making the csv look more with a real csv.  
As was the case with the last one, this file is also very commented, so I'll post the complete version right now:  

~~~python
"""The csv produced by the csv library is defective. To solve that
    we're going to clean it up after the fact. We'll turn the id
    and urls in two lists, and used them to build the csv manually."""
from loguru import logger

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def csv_cleanup():
    """Several list and string manipulation commands will be used
    until we achieve desired results."""

    with open("id_links.csv", "r") as f:
        outpt = f.read()

    chng_chars0 = []  # This kind of processes imply always a sequence of intermediate steps that have no
    chng_chars1 = []  # personality themselves, but are necessary for completing the task, Out of sheer
    chng_chars2 = []  # despair, I numerated the changes. I could've been able to use the same name, but it
    chng_chars3 = []  # wouldn't have been as helpfull when debugging.
    chng_chars3_id = []
    chng_chars4_id = []
    chng_chars4 = []
    link_list = []
    split_list = outpt.split("\n")

    for i in split_list:  # The entries had superfluous "('')" characters. We eliminate them.
        chng_chars0.append(i[2:-2])
    logger.info(chng_chars0)

    for i in chng_chars0:  # There was also excessive '"' characters. That was erased too.
        chng_chars1.append(i.replace('"', ""))
    logger.info(chng_chars1)

    for i in chng_chars1:
        chng_chars2.append(i.split(","))  # As the document was a string and didn't had the concept of first
    logger.info(chng_chars2)  # and second bits of information; it was needed to divide the entries,
    chng_chars2 = chng_chars2[1:-1]  # with a comma as delimiter. Creates small lists of two elements.

    for i in range(len(chng_chars2)):  # Separated the first element of the lists into a id list, and the
        chng_chars3.append(chng_chars2[i][1])  # second to a link list.
        chng_chars3_id.append(chng_chars2[i][0])
    logger.info(chng_chars3)
    logger.info(chng_chars3_id)

    for i in chng_chars3:  # There was, still, too much punctuation. Erased extraneous "'".
        chng_chars4.append(i.replace("'", ""))
    logger.info(chng_chars4)

    for i in chng_chars3_id:  # There were, still, some left.
        chng_chars4_id.append(i.replace("'", ""))
    logger.info(chng_chars4_id)

    for i in chng_chars4:  # Did away with superfluous leading white space.
        link_list.append(i.lstrip())
    logger.info(link_list)

    with open("link_lst", "w") as f:  # Wrote a list with urls for all html pages.
        f.write(str(link_list))

    with open("id_lst", "w") as id:  # Wrote a list of database ids to go with urls.
        id.write(str(chng_chars4_id))


if __name__ == "__main__":
    csv_cleanup()
~~~
<br>
<br>

------------------------------------------------

### 5 - build_csv.py
This module starts from the two files produced by 'id_url_list.py', and inserted them into a csv file.  
This file, as others in this project, is very commented, so no comments from me are necessary.  

~~~python
"""Module That will send the info to the database and build the csv file as an alternative"""
from loguru import logger
from mysql.connector import connect, Error

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def csv_build():
    """We'll start with the two files and write them to
    a csv file manually."""

    with open(
        "id_lst", "r"
    ) as idlst:  # We open the file produced by the last module and turn its content into a object that we
        id_src = idlst.read()  # can work with. Opening the id list.

    id_lt = id_src.split(
        ","
    )  # The read() function returns a string. To be able to have a concept of discrete elements,
    csv_build.id_lt = id_lt[
        1:-1
    ]  # needed to run it to a list by spliting the string by a delimiter. The comma in this case.
    print(csv_build.id_lt[0])  # Elements came with superfluous ')' characters in the beginning and end.

    with open("link_lst", "r") as lnklst:  # Opening the link list.
        lnk_src = lnklst.read()

    lnk_lt = lnk_src.split()  # Splitting the strings, for the same reasons explained above.
    lnk_l = []
    for i in lnk_lt:
        lnk_l.append(i[:-1])  # Erasing the last character in each element. I forget why.
    csv_build.lnk_lt = lnk_l[
        1:-1
    ]  # Erased "[]" characters from list, as they were being considered as part of the first and last
    print(csv_build.lnk_lt[0])  # link elements.

    with open("final.csv", "w") as f:  # Creating the csv to be used to upload to the database.

        for id, lnk in zip(
            id_lt, lnk_lt
        ):  # Zip function permits to iterate between two functions, without one being first or second, but
            f.write(id + "|" + lnk)  # on equal footing. Useful when we needed to pair lists elements with each other.
            f.write("\n")


if __name__ == "__main__":
    csv_build()


@logger.catch
def db_send():
    """Send the results to the db with update commands."""

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        for id, lnk in zip(csv_build.id_lt, csv_build.lnk_lt):
            query = "UPDATE notes SET url = " + lnk + " WHERE ntid = " + id
            logger.info(query)
            cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    db_send()
~~~
<br>
<br>

--------------------------------------------------------------------------------

### 6 - chg_wordcloud.py
This module is completely filled with preparatory work to insert the html links of the notes in the svg image.  
This haas proved to be more complicated than expected. Every time I think I'm near, there appears another preparatory work that must be done, and I'm again mired in a swamp of preliminary work.  
I'm starting to feel that I'm probably loosing focus and letting myself get mired in all this preparative steps. That there's a simple and clearer way of doing things. I just have to find it.  

1. The first function I just called 'prep-work', and it contains various small tasks that, in itself, don't amount to much, but prepare the way for other things.  

~~~python
@logger.catch
def prep_work():
    """We create a path containing object, turned wordcloud file into a list of lines,
    created a file with the final lines that will house the a tag, enumerated the list
    wordcloud. All prep-work necessary, we hope, to make the changes."""
    with open("path_lst.txt", "r") as path:
        path = path.read()
    path = [path]
    for i in path:
        path = i.split("\n")

    with open("wordcloud2.svg", "r") as wordcloud:
        wordcloud = wordcloud.read()
    wordcloud = [wordcloud]
    # print(type(wordcloud))
    for i in wordcloud:
        wordcloud = i.split("\n")

    subs = "transform"

    res = [i for i in wordcloud if subs in i]

    complete_lines = []
    for x, y in zip(res, path):
        complete_lines.append(x + y)
    prep_work.complete_lines = complete_lines[:-2]

    with open("complete_lines.txt", "w") as f:
        for line in complete_lines:
            f.write(line)
            f.write("\n")

    wordcloud = enumerate(wordcloud)
    prep_work.wordcloud = list(wordcloud)


if __name__ == "__main__":
    prep_work()
~~~

2. Here we connect the URLs to their corresponding tags.

~~~python
@logger.catch
def numbered_tags():
    """In order to put the URLS to their corresponding text tag, we created a list
    that has line numbers and tag names. This is to be used when we insert the
    the lines from 'complete_lines', as a marker of where to put them in the
    document."""

    text_tags = []  # Here I was trying to extract a substring from between two other substrings.
    left_side = 'alphabetic">'  # I half failed as, if I did get what I wanted, I also collected a lot of shit
    right_side = "</text>"  # that I don't know where it came from.
    for (
        num,
        line,
    ) in prep_work.wordcloud:  # This is not the best praxis, but I'll leave this here, for now, as it got me
        idx_left_side = line.find(left_side) + len(
            left_side
        )  # nearer to where I want to get, and it's late and I'm not nearly finished.
        idx_right_side = line.find(right_side)
        text_tags.append((num, line[idx_left_side:idx_right_side]))
    for num, line in text_tags:  # From here onwards things start to make sense again.
        if line == " ":
            del line
    text_tags = text_tags[8:-4]
    numbered_tags.text_tags = list(filter(lambda t: "" not in t, text_tags))  # https://tinyurl.com/yeqxxgrf
    numbered_tags.text_tags = numbered_tags.text_tags[::2]


if __name__ == "__main__":
    numbered_tags()
~~~

3. Here the objective was to create a list with the tags and the lines of text, with original text and our own, already done. This proved too difficult in Python, so I used various shell tools, that are documented in the body of the function.

~~~python
@logger.catch
def lines_tags():
    """Function to create a list with tags and complete lines"""

    # num_tag = numbered_tags.text_tags
    # Because I had a lot of difficulty doing this kind of operations in Python, I turned for Bash,
    # for help, specifcally Sed.
    # I added separated tag values to the complete lines file with this expression:
    # sed -e "s/tag= \(.*\)\">/\1/" complete_lines.txt
    # More here - https://tinyurl.com/yfrayu96
    # But Sed put the tag immediately after the url. So I'll use this function to create a list of
    # tuples.
    # UPDATE
    # I couldn't acomplish even that.
    # So, the day was saved with this Sed expression:
    # sed 's/php?/&, /' lines_tags.txt
    # It adds a comma and a space after 'php?'
    # It was also needed to add ' characters around the entries.
    # To add one in the beginning of the line, I used this expression:
    # sed -ne "s/.*/\'&/p" lines_tags.txt
    # To add another at the end of the line, I used:
    # It was needed to put one in the end of the first element:
    # sed "s/php?/&'/" lines_tags.txt
    # and at the start of the second.
    # sed "s/, /&'/" lines_tags.txt
    # I used Awk to add a tag field to the file. The script is this:
    # With all this we have a file that is more evolved than what I had before.
    # I'm going to import it, and try to finish in Python.

    with open("lines_tags1.txt", "r") as f:
        lt = f.read()
    lt = [lt]
    for i in lt:
        lt = i.split("\n")
    del lt[1]
    new_lt = []
    for i in lt:
        new_lt.append(i.split(", "))
    del new_lt[-1]

    for i in new_lt:
        i[0] = i[0][:-3] + i[1] + i[0][-2]
    lines_tags.new_lt = new_lt


if __name__ == "__main__":
    lines_tags()
~~~

4. The svg file already has an order that the tags must obey, when being inserted into the body of the code. I analyzed the svg code with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), to connect correctly our tags with the image's.  

~~~python
@logger.catch
def beautsoup():
    """We'll use BeautifullSoup, a HTML interpreter to read the svg file and get the
    value of each tag in the text, so as to connect it to right tag in the a tag."""

    with open("wordcloud.svg", "r") as fp:
        soup = BeautifulSoup(fp, "xml", from_encoding="utf-8")
    beautsoup.texts = soup.find_all("text")
    beautsoup.new = []
    for text in beautsoup.texts:
        beautsoup.new.append(text.get_text())
    for i in beautsoup.new:
        i = "'" + i + "'"
    with open("beautsoup.txt", "w") as f:
        f.write(str(beautsoup.new))


if __name__ == "__main__":
    beautsoup()
~~~

5. Sorting the URLS in the same order as the tags.  

~~~python
@logger.catch
def taglines_sorting():
    """We'll sort the urls in the same order as the tags. We'll look for
    occurrences of the tags in the text in the urls. When found,
    it'll create a order that will be, we hope, easy to do."""

    lt = lines_tags.new_lt

    with open("beautsoup2.txt", "r") as f:
        lines = f.readline()
    lines.split("\n")  # Objects coming from files are very large strings, who are good for nothing. These steps were an
    lines = lines.split()  # effort at making it mnore elastic.
    lines1 = []
    for i in lines:
        lines1.append(i.replace(",", ""))

    it_line = []
    flat_lt = []
    for i, line in zip(range(len(lines1)), lines1):  # I use zip when I want to simultaneously open two iterables.
        it_line.append((str(i), line))
    for element in it_line:  # The list had another list inside. We simplified it.
        if type(element) is list:
            for item in element:
                flat_lt.append(item)
        else:
            flat_lt.append(element)
    flat_lt[0] = ("0", "python")  # These two entries had supirous charcters inside. We clean them
    flat_lt[-1] = ("283", "array")  # with these commands

    for i in range(0, len(flat_lt)):
        line = flat_lt[i][1]
        print(
            [x for x in lt if line in x]
        )  # List comprehension to ascertain if substring is contained inside a string.
        time.sleep(0.1)


if __name__ == "__main__":
    taglines_sorting()
~~~

The full text:

~~~python
"""Module To insert in the Wordcloud file, the urls of the notes"""
from loguru import logger
import subprocess
from bs4 import BeautifulSoup
import time

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("tag_order.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def prep_work():
    """We create a path containing object, turned wordcloud file into a list of lines,
    created a file with the final lines that will house the a tag, enumerated the list
    wordcloud. All prep-work necessary, we hope, to make the changes."""
    with open("path_lst.txt", "r") as path:
        path = path.read()
    path = [path]
    for i in path:
        path = i.split("\n")

    with open("wordcloud2.svg", "r") as wordcloud:
        wordcloud = wordcloud.read()
    wordcloud = [wordcloud]
    # print(type(wordcloud))
    for i in wordcloud:
        wordcloud = i.split("\n")

    subs = "transform"

    res = [i for i in wordcloud if subs in i]

    complete_lines = []
    for x, y in zip(res, path):
        complete_lines.append(x + y)
    prep_work.complete_lines = complete_lines[:-2]

    with open("complete_lines.txt", "w") as f:
        for line in complete_lines:
            f.write(line)
            f.write("\n")

    wordcloud = enumerate(wordcloud)
    prep_work.wordcloud = list(wordcloud)


if __name__ == "__main__":
    prep_work()


@logger.catch
def numbered_tags():
    """In order to put the URLS to their corresponding text tag, we created a list
    that has line numbers and tag names. This is to be used when we insert the
    the lines from 'complete_lines', as a marker of where to put them in the
    document."""

    text_tags = []  # Here I was trying to extract a substring from between two other substrings.
    left_side = 'alphabetic">'  # I half failed as, if I did get what I wanted, I also collected a lot of shit
    right_side = "</text>"  # that I don't know where it came from.
    for (
        num,
        line,
    ) in prep_work.wordcloud:  # This is not the best praxis, but I'll leave this here, for now, as it got me
        idx_left_side = line.find(left_side) + len(
            left_side
        )  # nearer to where I want to get, and it's late and I'm not nearly finished.
        idx_right_side = line.find(right_side)
        text_tags.append((num, line[idx_left_side:idx_right_side]))
    for num, line in text_tags:  # From here onwards things start to make sense again.
        if line == " ":
            del line
    text_tags = text_tags[8:-4]
    numbered_tags.text_tags = list(filter(lambda t: "" not in t, text_tags))  # https://tinyurl.com/yeqxxgrf
    numbered_tags.text_tags = numbered_tags.text_tags[::2]


if __name__ == "__main__":
    numbered_tags()


@logger.catch
def lines_tags():
    """Function to create a list with tags and complete lines"""

    # num_tag = numbered_tags.text_tags
    # Because I had a lot of difficulty doing this kind of operations in Python, I turned for Bash,
    # for help, specifcally Sed.
    # I added separated tag values to the complete lines file with this expression:
    # sed -e "s/tag= \(.*\)\">/\1/" complete_lines.txt
    # More here - https://tinyurl.com/yfrayu96
    # But Sed put the tag immediately after the url. So I'll use this function to create a list of
    # tuples.
    # UPDATE
    # I couldn't acomplish even that.
    # So, the day was saved with this Sed expression:
    # sed 's/php?/&, /' lines_tags.txt
    # It adds a comma and a space after 'php?'
    # It was also needed to add ' characters around the entries.
    # To add one in the beginning of the line, I used this expression:
    # sed -ne "s/.*/\'&/p" lines_tags.txt
    # To add another at the end of the line, I used:
    # It was needed to put one in the end of the first element:
    # sed "s/php?/&'/" lines_tags.txt
    # and at the start of the second.
    # sed "s/, /&'/" lines_tags.txt
    # I used Awk to add a tag field to the file. The script is this:
    # With all this we have a file that is more evolved than what I had before.
    # I'm going to import it, and try to finish in Python.

    with open("lines_tags1.txt", "r") as f:
        lt = f.read()
    lt = [lt]
    for i in lt:
        lt = i.split("\n")
    del lt[1]
    new_lt = []
    for i in lt:
        new_lt.append(i.split(", "))
    del new_lt[-1]

    for i in new_lt:
        i[0] = i[0][:-3] + i[1] + i[0][-2]
    lines_tags.new_lt = new_lt


if __name__ == "__main__":
    lines_tags()


@logger.catch
def beautsoup():
    """We'll use BeautifullSoup, a HTML interpreter to read the svg file and get the
    value of each tag in the text, so as to connect it to right tag in the a tag."""

    with open("wordcloud.svg", "r") as fp:
        soup = BeautifulSoup(fp, "xml", from_encoding="utf-8")
    beautsoup.texts = soup.find_all("text")
    beautsoup.new = []
    for text in beautsoup.texts:
        beautsoup.new.append(text.get_text())
    for i in beautsoup.new:
        i = "'" + i + "'"
    with open("beautsoup.txt", "w") as f:
        f.write(str(beautsoup.new))


if __name__ == "__main__":
    beautsoup()


@logger.catch
def taglines_sorting():
    """We'll sort the urls in the same order as the tags. We'll look for
    occurrences of the tags in the text in the urls. When found,
    it'll create a order that will be, we hope, easy to do."""

    lt = lines_tags.new_lt

    with open("beautsoup2.txt", "r") as f:
        lines = f.readline()
    lines.split("\n")  # Objects coming from files are very large strings, who are good for nothing. These steps were an
    lines = lines.split()  # effort at making it mnore elastic.
    lines1 = []
    for i in lines:
        lines1.append(i.replace(",", ""))

    it_line = []
    flat_lt = []
    for i, line in zip(range(len(lines1)), lines1):  # I use zip when I want to simultaneously open two iterables.
        it_line.append((str(i), line))
    for element in it_line:  # The list had another list inside. We simplified it.
        if type(element) is list:
            for item in element:
                flat_lt.append(item)
        else:
            flat_lt.append(element)
    flat_lt[0] = ("0", "python")  # These two entries had supirous charcters inside. We clean them
    flat_lt[-1] = ("283", "array")  # with these commands

    for i in range(0, len(flat_lt)):
        line = flat_lt[i][1]
        print(
            [x for x in lt if line in x]
        )  # List comprehension to ascertain if substring is contained inside a string.
        time.sleep(0.1)


if __name__ == "__main__":
    taglines_sorting()
~~~

# UPDATE

Well, on the bright side, I finished what I set out to do, to set up the svg image with new links. On not so brighter note, I did almost all important work by hand or through the shell, and, in the end, this was nothing that I really wanted. Not really.  
I had had, I thought, a simple task ahead of me: To insert into a file, lines that should be 3 lines apart between themselves.  
I couldn't do it. I stumbled on the problem of needing two iterators running at the same time, one giving the lines to insert, another for the line numbers, and, one, couldn't solve it, and, two, couldn't think of something else.  
In the end I went with a solution who got me what I wanted, but it also produced a mountain of spurious data.  
What I've done was this:  
1. Created a list with the numbers I was going to need. Already skipping 3 numbers by iteration, already starting at the line number that the command I wanted to replace, first appears.  

~~~python
sel = [i for i in range(0, len(word), 3)]
~~~

2. Set a loop through the list of the lines to insert, created a variable to:
    - Define the number of the line that was going to be erased. In order for the new one to be inserted,
    - define, in the same manner, the line number for the insertion operation,
    - be the base for a variable that will write to file.  
        The reason for the ***variable + 1***, came from a need I had when building this solution, to see the evolution of the loops and how much were they covering the text-tags list. It's there just so I can get my head around the problem.  

~~~python
    for url in urls:
        pos = int(sel[0])
        word.pop(pos)
        word.insert(pos, url)
        posi = pos + 1
~~~

3. And, finally, sent everything to a file. Because I couldn't figure out how to keep in the same variable, the lines I didn't want to change, and the ones I did.  
Everything I tried, ended with a variable with only the changed lines or with the unchanged list. At least in this way, I could access what I wanted during the running of the loop. In the end it was just a case of separating the wheat from the chaff, which was simple, but didn't alleviate the feeling that I was, both, an idiot and a cheat.  
Here's the full code:

~~~python
"""Module to append the completed lines to the text tags."""
import time
from pprint import pprint
import subprocess
from loguru import logger

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def url_appending():
    """
    Although this produces far too much output that I need, the fact is
    it does produce what I'm looking for. As this is a one-time project,
    I'm just going to cut what I need, put it in a file, and do any
    cleaning I need with sed, awk and things of that ilk.
    """

    with open("wordcloud1.svg", "r") as f:
        word = f.readlines()
    with open("line_complete.svg", "r") as f:
        urls = f.readlines()

    sel = [i for i in range(0, len(word), 3)]
    for i in sel:
        print(i)

    for url in urls:
        pos = int(sel[0])
        word.pop(pos)
        word.insert(pos, url)
        posi = pos + 1
        with open("final.svg", "w") as f:
            f.write(str(word[:posi]))
            f.write("\n")
            pprint(word[:posi])
        sel.pop(0)


if __name__ == "__main__":
    url_appending()
~~~

After this, I still had much to do, using Sed and Awk to clean the files to the shape it was needed. In that respect, this effort was not in vain. I come out of this with a much clearer understanding of both these tools. But that was not my original intention.  
It was happily fortuitous.  
My intention was learn more about python with a project heavy on file manipulation. And it seemed I couldn't understand it, so I used other means.  
On top of all this, there's the fact that, in the end, I decided I didn't want the word cloud anymore. I am to build something from just the links that, if not so polished, it won't so trite.  
This project left me with an unfinished feeling. I know that are python solutions for the problem I was facing, and I imagine they won't metaphysically complex, I just have to dig deeper. 
