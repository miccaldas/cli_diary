"""
We present a list of posts to the user, one is chosen
and we open it in the browser.
"""
import os
import webbrowser

import click
import isort
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def index():
    """
    We call the id's and titles of the db's entries, show them
    their values. The user can open an entry by inputing the
    corresponding id. With the id we retrieve its title, attach
    '.html' to it and open it through 'webbrowser'.
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
        print("Error while connecting to db", e)

    print("\n")
    choi = input(click.style("[*] - What is the id of the post you want to see? ", fg="bright_green", bold=True))
    choice = int(choi)
    return choice


# @snoop
def show():
    """
    Using the choice done in the last function,
    t's created a temporary html file, that
    is opened in Lynx, and is deleted ensuing the
    the closure of the browser session.
    """

    choice = index()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        answers = [choice]
        query = "SELECT title FROM cli_diary WHERE id = %s"
        cur.execute(query, (choice,))
        record = cur.fetchone()
        title_str = " "
        title = title_str.join(record)
        filename = f"{title}.html"
        conn.close()
    except Error as e:
        print("Error while connecting to db", e)

    os.chdir("html_posts")
    webbrowser.open_new_tab(f"{filename}")


if __name__ == "__main__":
    show()
