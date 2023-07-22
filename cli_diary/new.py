"""
Creates a markdown file for the user to write a post,
converts it to html and registers it in the database.
"""
import os
import pickle
import subprocess
from datetime import datetime

import click

# import snoop
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


def dbdata(query, data):
    """
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
            host="localhost", user="mic", password="xxxx", database="cli_diary"
        )
        cur = conn.cursor()
        cur.execute(query)
        if data == "fetch":
            data = cur.fetchall()
        if data == "commit":
            data = conn.commit()
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


# @snoop
def titlename():
    """
    Defines title name. As several functions will need
    the string with the actual title of the post, as well
    as a version to be used as file name, we'll define
    them both here and make them available in a pickle file.
    """
    title = input(
        click.style(
            " [X] - What is the title of your post? ", fg="bright_green", bold=True
        )
    )
    low = title.lower()
    unders = low.replace(" ", "_")
    titles = [title, unders]

    with open("titles.bin", "wb") as f:
        pickle.dump(titles, f)


# @snoop
def mdfile():
    """
    Creates a markdown file and populates
    its metadata.
    """
    with open("titles.bin", "rb") as f:
        titles = pickle.load(f)

    title = titles[0]
    unders = titles[1]
    cwd = "/home/mic/python/cli_diary/cli_diary/"
    md_file = f"{unders}.md"
    flpth = f"{cwd}md_posts/{md_file}"

    # Creates a datetime object to put in the metadata and in the post's body.
    now = datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M")

    with open(flpth, "w") as g:
        g.write("---\n")
        g.write(f"title: {title}\n")
        g.write(f"date: {now}\n")
        g.write("mainfont: Iosevka\n")
        g.write("fontsize: 15pt\n")
        g.write("---\n\n\n\n")

    cmd = f"vim {flpth}"
    subprocess.run(cmd, shell=True)


# @snoop
def htmlfile():
    """
    Creates the html file, using Pandoc.
    Adds line height definition to html.
    """
    with open("titles.bin", "rb") as f:
        titles = pickle.load(f)

    unders = titles[1]

    cmd = f"pandoc --highlight-style=breezedark -s -o html_posts/{unders}.html md_posts/{unders}.md"
    subprocess.run(cmd, shell=True)

    # Reads the html file.
    with open(f"html_posts/{unders}.html", "r") as f:
        content = f.readlines()
    # As 'readlines()' creates a list object, we can use list functions to manipulate it.
    # So, we can put an element in any index position, and all the other elements are
    # preserved. Here we add, in line 13, a css definition of line-hright.
    content.insert(13, "      line-height: 1.5;\n")
    content.insert(17, "        max-width: 45em;\n")
    # To rewrite the file with the added line, we use 'writelines()', that writes list objects
    # to a file.
    with open(f"html_posts/{unders}.html", "w") as g:
        g.writelines(content)


# @snoop
def kwdcreator():
    """
    Since it's only two keywords, we'll let the user decide.
    """
    k1 = input(click.style(" Choose a keyword » ", fg="bright_green", bold=True))
    k2 = input(click.style(" Choose another... » ", fg="bright_green", bold=True))

    kwds = [k1, k2]

    return kwds


# @snoop
def dbcall():
    """
    Updates the db with the new entry.
    """
    with open("titles.bin", "rb") as f:
        titles = pickle.load(f)

    unders = titles[1]

    kwds = kwdcreator()

    query = f"INSERT INTO cli_diary (title, k1, k2) VALUES ('{unders}', '{kwds[0]}', '{kwds[1]}')"
    dbdata(query, "commit")


# @snoop
def new_main():
    """
    Calls all functions on the module.
    """
    titlename()
    mdfile()
    htmlfile()
    dbcall()

    os.remove("titles.bin")


if __name__ == "__main__":
    new_main()
