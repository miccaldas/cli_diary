"""Searches the database data and enables opening results."""
import os
import webbrowser

import click
import isort
import questionary
import snoop
from mysql.connector import Error, connect
from questionary import Style
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def search():
    """
    Uses MySQL queries with fulltext to search the database.
    Asks user if he wants to open any of the results. If yes
    it opens the post, if not, exits the process.
    """

    custom_style_diary = Style(
        [
            ("qmark", "fg:#FF6363 bold"),
            ("question", "fg:#069A8E bold"),
            ("answer", "fg:#A1E3D8"),
            ("pointer", "fg:#F8B400 bold"),
            ("highlighted", "fg:#F7FF93 bold"),
            ("selected", "fg:#FAF5E4 bold"),
            ("separator", "fg:#069A8E"),
            ("instruction", "fg:#A1E3D8"),
            ("text", "fg:#FAF5E4 bold"),
        ]
    )

    try:
        ask = input(click.style(" [*] - What do you want to search? ", fg="bright_green", bold=True))

        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = f"SELECT id, title FROM cli_diary WHERE MATCH(title, k1, k2) AGAINST ('{ask}')"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(click.style(f" {row[0]} - ", fg="bright_green", bold=True), click.style(row[1], fg="bright_white", bold=True))
        conn.close()
    except Error as e:
        print("Error while connecting to db", e)

    print("\n")
    cont = questionary.confirm(
        "Do you want to open a result?",
        qmark=" [X]",
        default=True,
        style=custom_style_diary,
    ).ask()

    if cont:
        choi = input(click.style(" [*] - What is the id of the post you want to see? ", fg="bright_green", bold=True))
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
            filename = f"{title}.html"
            conn.close()
        except Error as e:
            print("Error while connecting to db", e)

        os.chdir("html_posts")
        webbrowser.open_new_tab(f"{filename}")


if __name__ == "__main__":
    search()
