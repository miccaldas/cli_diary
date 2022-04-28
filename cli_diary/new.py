"""
Creates a markdown file for the user to write a post,
converts it to html and registers it in the database.
"""
import os
import subprocess

import click
import isort
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def new():
    """
    Open a vim file through subprocess,
    converts it to html with pandoc and
    puts it on the 'html_posts' folder.
    Updates database with new entry.
    """
    title = input(click.style(" [X] - What is the title of your post? ", fg="bright_green", bold=True))
    k1 = input(click.style(" [X] - Choose a keyword. ", fg="bright_green", bold=True))
    k2 = input(click.style(" [X] - Choose another. ", fg="bright_green", bold=True))
    answers = [title, k1, k2]
    md_file = f"{title}.md"

    cmd = f"vim {md_file}"
    subprocess.run(cmd, cwd="md_posts", shell=True)

    cmd1 = f"pandoc --highlight-style=zenburn -s -o html_posts/{title}.html md_posts/{md_file}"
    subprocess.run(cmd1, shell=True)

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "INSERT INTO cli_diary (title, k1, k2) VALUES (%s, %s, %s)"
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    new()
