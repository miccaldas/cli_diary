"""
Shows content of the database.
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
def see():
    """
    Shows all post's id's and titles.
    """

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        query = "SELECT id, title from cli_diary"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(click.style(f"  {row[0]} - ", fg="bright_green", bold=True), click.style(row[1], fg="bright_white", bold=True))
        conn.close()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    see()
