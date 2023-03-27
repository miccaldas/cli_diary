"""
Edits an existing post.
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
def edit():
    """
    Shows db contents, user chooses post, we open it
    on vim. After the editing process, we delete the
    old html file and replace it with a new one.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "SELECT id, title FROM cli_diary"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(click.style(f"  {row[0]} - ", fg="bright_green", bold=True), click.style(row[1], fg="bright_white", bold=True))
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e

    print("\n")
    choi = input(click.style("[*] - What is the id of the post you want to edit? ", fg="bright_green", bold=True))
    choice = int(choi)

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        answers = [choice]
        query = "SELECT title FROM cli_diary WHERE id = %s"
        cur.execute(query, (choice,))
        record = cur.fetchone()
        title_str = " "
        title = title_str.join(record)
        filename_html = f"{title}.html"
        filename_md = f"{title}.md"
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, e
    cmd = f"vim {filename_md}"
    subprocess.run(cmd, cwd="md_posts", shell=True)

    os.remove(f"html_posts/{filename_html}")

    cmd1 = f"pandoc --highlight-style=zenburn -s -o html_posts/{filename_html} md_posts/{filename_md}"
    subprocess.run(cmd1, shell=True)


if __name__ == "__main__":
    edit()
