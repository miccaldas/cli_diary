"""
Sometimes this app has content that's added but not through
the 'new post' command. Which means that it doesn't get
put in the db and doesn't show in the 'search' and 'see'
commands. This module will run twice monthly to check what
files are in the 'md_posts' folder, if there's something
new, it'll be added to the db.
"""
import os
import pickle
import subprocess

import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def db_updates():
    """"""
    cwd = os.getcwd()
    mdpth = f"{cwd}/md_posts"
    updts = f"{cwd}/updatedata"
    mdlist = os.listdir(mdpth)

    with open(f"{updts}/new_updt.bin", "wb") as f:
        pickle.dump(mdlist, f)

    # print(mdlist)


if __name__ == "__main__":
    db_updates()
