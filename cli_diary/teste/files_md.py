"""

"""
import os

import snoop
from pynput.mouse import Button, Controller

# import subprocess
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def fun():
    """"""
    mouse = Controller()

    mdfolder = "/home/mic/python/cli_diary/cli_diary/md_posts"
    mdfiles = os.listdir(mdfolder)

    coords = (2, 2)
    mouse.press(Button.left)
    print(len(mdfiles))


if __name__ == "__main__":
    fun()
