"""Inserts a space at the beginning of every line."""
import os
import subprocess

import isort
import snoop
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def insert_space():
    """"""
    files = os.listdir("md_posts")

    for i in files:
        cmd = "sed '/```python/,/```/{/```python/n;/```/!{s/^/  /g}}' md_posts/" + i + " > space_files/" + i
        print(cmd)
        subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    insert_space()
