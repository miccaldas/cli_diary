"""
Module Docstring
"""
import os

# import subprocess
import pickle
from pynput.mouse import Button, Controller
import snoop
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def files_md():
    """"""
    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"
    mdfiles = os.listdir(mdfolder)

    mouse = Controller()


if __name__ == "__main__":
    files_md()
