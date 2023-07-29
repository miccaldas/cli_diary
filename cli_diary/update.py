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

    # This query is here to change the files names. It gets the current name
    # and uses it to replace it by the new one in 'md_posts' and 'html_posts'
    # folders. This is used in the 'files_update' function, that is right below.
    if column == "title":
        title_query = "SELECT title FROM cli_diary WHERE id = %s"
        old_tit = dbdata(title_query, "fetch", [updt_id])
        old_title = old_tit[0][0]
        files_update(old_title, value, updt_id)
    else:
        query = f"UPDATE cli_diary SET {column} = %s WHERE id = %s"
        dbdata(query, "commit", [f"{value}", f"{updt_id}"])


if __name__ == "__main__":
    update()


# @snoop
def files_update(old_title, value, updt_id):
    """
    If the title was updated, this function
    updates the HTML and md files.
    """
    cwd = os.getcwd()
    mdfolder = f"{cwd}/md_posts"
    htmlfolder = f"{cwd}/html_posts"
    mdfiles = os.listdir(f"{mdfolder}")
    htmlfiles = os.listdir(f"{htmlfolder}")

    for i in [(".html", f"{htmlfolder}"), (".md", f"{mdfolder}")]:
        cmd = f"mv '{old_title}{i[0]}' {value}{i[0]}"
        subprocess.run(cmd, cwd=f"{i[1]}", shell=True)
