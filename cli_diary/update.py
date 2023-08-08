"""
Updates database entries and file names, if needed.
"""
import subprocess

import click
import snoop
from mysql.connector import Error, connect
from snoop import pp

from db import dbdata
from edit import edit


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def title_update(value, updt_id):
    """
    Before the title is updated on the db,
    this function updates the HTML and md files.
    """
    cwd = "/home/mic/python/cli_diary/cli_diary"
    mdfolder = f"{cwd}/md_posts"
    htmlfolder = f"{cwd}/html_posts"

    # Getting the old name, before we change it, so we know what
    # are the names of the files.
    title_query = "SELECT title FROM cli_diary WHERE id = %s"
    old_tit = dbdata(title_query, "fetch", [updt_id])
    old_title = old_tit[0][0]

    # Slugifying the new title.
    low = value.lower()
    ndots = low.replace(".", "")
    ndash = ndots.replace("-", "_")
    slug = ndash.replace(" ", "_")

    # This changes the files. It needs to be all spelled out like this
    # because if the commands were in a list, there's no guarantee that
    # the order would be maintained. If copying the files fails, the
    # function stops. If trashing files fails, a warning is sent.
    cmd = f"cp {htmlfolder}/{old_title}.html {htmlfolder}/{slug}.html"
    try:
        subprocess.check_output(cmd, cwd=cwd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Unable to copy the html filename to the new one.", e.output)
        raise SystemExit

    cmd0 = f"cp {mdfolder}/{old_title}.md {mdfolder}/{slug}.md"
    try:
        subprocess.check_output(cmd0, cwd=cwd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Unable to copy the md filename to the new one.", e.output)
        raise SystemExit

    cmd1 = f"/usr/bin/trash-put {htmlfolder}/{old_title}.html"
    print(cmd1)
    try:
        subprocess.check_output(cmd1, cwd=cwd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Unable to trash the old html file.", e.output)

    cmd2 = f"/usr/bin/trash-put {mdfolder}/{old_title}.md"
    print(cmd2)
    try:
        subprocess.check_output(cmd2, cwd=cwd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Unable to trash the old md file.", e.output)

    # This changes the database.
    query = "UPDATE cli_diary SET title = %s WHERE id = %s"
    dbdata(query, "commit", [f"{slug}", f"{updt_id}"])

    # You still need to change the title in the body of the md file.
    # We'll open edit() to do it.
    print(click.style(" [X] - Edit the file to change the title", fg="bright_green", bold=True))
    edit()


@snoop
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
        title_update(value, updt_id)
    else:
        query = f"UPDATE cli_diary SET {column} = %s WHERE id = %s"
        dbdata(query, "commit", [f"{value}", f"{updt_id}"])


if __name__ == "__main__":
    update()
