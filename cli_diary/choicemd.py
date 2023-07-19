"""
Like the 'View' module, but for Markdown.
The 'sys' import and next call, is there
to silence the publication of error messages.
"""
import sys

sys.tracebacklimit = 0

import os
import pickle
import subprocess
from datetime import datetime

# import snoop
from mysql.connector import Error, connect
from pynput import keyboard
from rich.console import Console

# from snoop import pp


# def type_watch(source, value):
#     return f"type({source})", type(value)


# snoop.install(watch_extras=[type_watch])


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


# @snoop
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
    code. Another consequence of using 'Pynput' is
    that it's keyboard code interpretation is done
    character by character, which doesn't let us id
    the entries as we would normally do, with a
    simple count of entries. Instead we used the
    alphabet, uppercase and lowercase, and some
    numbers to get us to our goal of 54 entries.
    And this is the reason for the cumbersome but
    practicaL 'alphanumbers' list.
    """
    query = "SELECT title, k1, k2, time FROM cli_diary"
    data = dbdata(query, "fetch")

    idxs = [i + (keyboard.KeyCode(char=f"{t}"),) for t, i in zip(alphanumbers, data)]

    with open("idxs.bin", "wb") as f:
        pickle.dump(idxs, f)


# @snoop
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

        console = Console()
        console.print(f" [bold #7C9D96]{id}[/] [bold #E9B384]{title}[/] [bold #FE0000]@[/][bold #F4E0B9]{k1}[/],[bold #FE0000]@[/][bold #F4E0B9]{k2}[/] [bold #A1CCD1]{time}[/]")

    console.print("\n\n  [bold #BBD6B8]\[*] - TYPE THE ID OF AN ENTRY TO READ THE POST![/]")


if __name__ == "__main__":
    postlist()


# @snoop
def execute(filename):
    """
    Where we wait for someone to be chosen.
    We call 'mdless', like 'mdcat', but uses
    a pager, to read the post chosen by the user.
    We chose to constrain the output to 90 columns.
    """
    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"
    path = f"{mdfolder}/{filename}.md"
    cmd = f"mdless --columns=90 {path}"
    subprocess.run(cmd, shell=True)


# @snoop
def on_press(entry):
    """
    Function the waits for user keyboard input. The list of
    tuples that concentrated all information for this module,
    had an 'id' field a little different than usual. We used
    id's of just one character, to identify the posts. This
    was done so we could use the Pynput library. The fact that
    it responds immediately to keyboard input, is a much more
    interactive way to choose content. Akin, in a way, to
    clicking on a html file and opening it. I wanted some of
    that closeness, but for markdown. It awaits for user
    input, to see if it matches the id of one of its posts. If
    so, it starts another function that uses a cli markdown
    reader to show its content.
    """
    with open("idxs.bin", "rb") as f:
        idxs = pickle.load(f)

    for idx in idxs:
        if entry == idx[4]:
            execute(idx[0])
            raise SystemExit


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
