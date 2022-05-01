"""
Opens a tree like view of the post files that can
can be accessed by clicking them.
"""
import os
import subprocess

import isort
import snoop
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def view():
    """
    We use the 'tree' module to see and open
    the posts.
    """

    lst = os.listdir("html_posts")

    cmd = "ntree html_posts"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    view()
