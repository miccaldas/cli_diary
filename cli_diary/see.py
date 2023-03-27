"""
Shows content of the database and opens chosen
markdown file in less.
"""
import os
import subprocess
import sys
import click

import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

# @snoop
def see():
    """
    Shows all post's id, title, tags and timestamp.
    We use the rich-cli command line app instead of
    just rich, because the latter doesn't have all
    the options of the former. The rich command asks
    for the file to be opened by a pager, with a width
    of 120 px, 2px of padding and using the nord
    colorscheme.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "SELECT id, title, k1, k2, time from cli_diary"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(
                click.style(f"  {row[0]} - ", fg="bright_green", bold=True),
                click.style(row[1], fg="bright_white", bold=True),
                click.style(f" #{row[2]}/#{row[3]} ", fg="bright_red", bold=True),
                click.style(row[4], fg="bright_yellow", bold=True),
            )
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e
    finally:
        if conn:
            conn.close()

    print("\n")
    choice = input(click.style("  What post do you want to read? ", fg="bright_white", bold=True))

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = f"SELECT title FROM cli_diary WHERE id = {choice}"
        cur.execute(query)
        records = cur.fetchall()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e
    for row in records:
        path = f"/home/mic/python/cli_diary/cli_diary/md_posts/{row[0]}.md"
        cmd = f"rich {path} --pager -w 120 -d 2 --theme nord"
        subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    see()
