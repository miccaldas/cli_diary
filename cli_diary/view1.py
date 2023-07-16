"""
Opens a tree like view of the post files that can
can be accessed by clicking them.
"""
import os
import subprocess
from datetime import datetime

import snoop
from mysql.connector import Error, connect
from rich import print
from rich.text import Text
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def dbdata(query, data):
    """
    Collects list of posts on the db.
    We'll use this function as a template,
    letting the functions that call on it
    to define its structure. That being
    the query and if using .fetchall()
    or .commit()
    This permits writing just one db function
    per module.
    """
    try:
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="cli_diary",
        )
        cur = conn.cursor()
        cur.execute(query)
        if data == "fetch":
            data = cur.fetchall()
        if data == "commit":
            data = conn.commit()
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()
    for d in data:
        print(d)

    return data


# @snoop
def view():
    """ """
    query = "SELECT id, title, time FROM cli_diary ORDER BY time"
    orderedposts = dbdata(query, "fetch")
    # for post in orderedposts:
    #     print(post[0])
    #     print(post[1])
    #     print(post[2])
    htmlfolder = f"{os.getcwd()}/html_posts"
    htmlfiles = os.listdir(htmlfolder)
    for post in orderedposts:
        titspaces = post[1].replace("_", " ")
        date = f"  {post[2].strftime('%d-%m-%Y, %H:%M')} "
        capitalize = f"  {titspaces.title()}"
        print(
            f"[bold #5E8B7E]{date}[/][bold #B2B8A3][link=file://{htmlfolder}/{post[1]}.html]{capitalize}[/link]"
        )


if __name__ == "__main__":
    view()
