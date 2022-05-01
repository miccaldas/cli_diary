"""
Searches db for query. Presents results.
"""
import os
import pathlib
import sys

import click
import isort
import snoop
from mysql.connector import Error, connect
from rich import print
from rich.text import Text


# @snoop
def search():
    """
    Uses MySQL queries with fulltext to search the database.
    Uses Rich library to allow for clickable links on the posts.
    """

    path = "/home/mic/python/cli_diary/cli_diary/html_posts"
    ask = input(click.style(" [*] - What do you want to search? ", fg="bright_green", bold=True))

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = f"SELECT title, title FROM cli_diary WHERE MATCH(title, k1, k2) AGAINST ('{ask}')"
        cur.execute(query)
        records = cur.fetchall()
        conn.close()
    except Error as e:
        print("Error while connecting to db", e)

    tupfiles = []
    for i in records:
        tupfile = (i[0], i[1] + ".html")
        tupfiles.append(tupfile)

    roads = []
    for t in tupfiles:
        road = (t[0], f"{path}/{t[1]}")
        roads.append(road)

    for road in roads:
        print(f"[bold #B2B8A3] (**) - [link=file:///{road[1]}]{road[0]}[/link][/]")


if __name__ == "__main__":
    search()
