"""
Updates database entries and file names, if needed.
"""
import os
import subprocess

import click

# import snoop
from mysql.connector import Error, connect
from snoop import pp

from db import dbdata

# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def update():
    """
    Asks for column and id to make update.
    """

    column = input(click.style(" [X] - What is the column name? ", fg="bright_green", bold=True))
    value = input(click.style(" [X] - What is the alteration? ", fg="bright_green", bold=True))
    updt_id = int(input(click.style(" [X] - What is the id? ", fg="bright_green", bold=True)))

    # This is a function call to, besides the db values, alter the names of the markdown and
    # html files. It gets the old name, to identify the files and change their names.
    if column == "title":
        try:
            title_update(value, updt_id)
        except (Error, FileNotFoundError) as e:
            print(click.style(f"  title_update() failed with error: {e}", fg="red", bold=True))
            raise SystemExit

    query = f"UPDATE cli_diary SET {column} = %s WHERE id = %s"
    dbdata(query, "commit", [f"{value}", f"{updt_id}"])


if __name__ == "__main__":
    update()


# @snoop
def title_update(value, updt_id):
    """
    Before the title is updated on the db,
    this function updates the HTML and md files.
    """
    cwd = "/home/mic/python/cli_diary/cli_diary"
    mdfolder = f"{cwd}/md_posts"
    htmlfolder = f"{cwd}/html_posts"

    title_query = "SELECT title FROM cli_diary WHERE id = %s"
    old_tit = dbdata(title_query, "fetch", [updt_id])
    old_title = old_tit[0][0]

    for i in [(".html", f"{htmlfolder}"), (".md", f"{mdfolder}")]:
        cmd = f"mv {old_title}{i[0]} {value}{i[0]}"
        subprocess.run(cmd, cwd=f"{i[1]}", shell=True)
