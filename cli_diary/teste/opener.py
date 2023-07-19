"""
Module Docstring
"""
import os
import subprocess
import sys
from contextlib import suppress

import snoop
from pynput import mouse
from snoop import pp

sys.tracebacklimit = 0


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def opener():
    """"""
    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"
    mdfiles = os.listdir(mdfolder)
    allpaths = [(f"{mdfolder}/{i}]", i) for i in mdfiles]


if __name__ == "__main__":
    opener()
