"""
Like the 'View' module, but for Markdown.
"""
# import sys

# sys.tracebacklimit = 0
# The 'sys' import and call are there to silence the publication of error messages.

import os
import pickle
import subprocess
from datetime import datetime

import snoop
from mysql.connector import Error, connect
from pynput import keyboard
from rich.console import Console
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


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
        conn = connect(host="localhost", user="mic", password="xxxx", database="cli_diary")
        cur = conn.cursor()
        cur.execute(query)
        if data == "fetch":
            data = cur.fetchall()
        if data == "commit":
            data = conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    return data


alphanumbers = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "1",
    "2",
    "3",
]


@snoop
def dbcall():
    """
    We'll colect some data from the database.
    When we use a listener to monitor the
    keyboard, it transforms the keys from strings
    to 'Pynput' objects. This means that the id's
    of the post entries will never match with the
    user input, for one is a string and the other
    is an object. To remedy this, we build a list
    that stores the ID values as 'Pynput' objects
    That is the objective of the 'keyboard.KeyCode'
    code.
    """
    query = "SELECT title, k1, k2, time FROM cli_diary"
    data = dbdata(query, "fetch")

    idxs = [i + (keyboard.KeyCode(char=f"{t}"),) for t, i in zip(alphanumbers, data)]

    with open("idxs.bin", "wb") as f:
        pickle.dump(idxs, f)


if __name__ == "__main__":
    dbcall()


@snoop
def postlist():
    """
    Creates a posts list, so users can choose
    what they want to read.
    """
    with open("idxs.bin", "rb") as f:
        idxs = pickle.load(f)

    for idx in idxs:
        id = idx[4]
        title = idx[0].replace("_", " ").title()
        k1 = idx[1].lower()
        k2 = idx[2].lower()
        time = f"{idx[3].strftime('%Y-%m-%d %H:%M')}"

        # We broke the Rich text formatting in chunks, so as not to write a overlong line.
        cid = f"[bold #7C9D96]{id}[/]"
        ctitle = f"[bold #E9B384]{title}[/]"
        campersand = "[bold #FE0000]@[/]"
        ck1 = f"[bold #F4E0B9]{k1}[/],"
        ck2 = f"[bold #F4E0B9]{k2}[/] "
        ctime = f"[bold #A1CCD1]{time}[/]"

        console = Console()
        # The keyword values don't have spaces between them.
        console.print(cid, ctitle, f"{campersand}{ck1}{campersand}{ck2}", ctime)

    console.print("\n\n  [bold #BBD6B8]\[*] - TYPE THE ID OF AN ENTRY TO READ THE POST![/]")


if __name__ == "__main__":
    postlist()


@snoop
def execute(filename):
    """
    Where we wait for someone to be chosen.
    We call 'mdless', like 'mdcat', but uses
    a pager, to read its chosen post.
    We constrain the output to 90 columns.
    """
    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"
    path = f"{mdfolder}/{filename}.md"
    cmd = f"mdless --columns=90 {path}"
    subprocess.run(cmd, shell=True)


@snoop
def on_press(entry):
    """
    Function that waits for user keyboard input.
    """
    with open("idxs.bin", "rb") as f:
        idxs = pickle.load(f)

    for idx in idxs:
        if entry == idx[4]:
            execute(idx[0])
            raise SystemExit


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
